from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager
from django.urls import reverse


class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('Заполните поле email')
		if not username:
			raise ValueError('Заполните поле логина')

		user = self.model(
				email=self.normalize_email(email),
				username=username,
			)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
				email=self.normalize_email(email),
				password=password,
				username=username,
			)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class Account(AbstractBaseUser):
	email = models.EmailField(verbose_name='email', max_length=60, unique=True)
	username = models.CharField(max_length=30, unique=True)
	date_joined = models.DateTimeField(verbose_name='дата регистрации', auto_now_add=True)
	last_login = models.DateTimeField(verbose_name='последнее посещение', auto_now=True)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	objects = MyAccountManager()

	def __str__(self):
		return self.username

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True


class Profile(models.Model):
	user = models.OneToOneField('CustomUser',on_delete=models.CASCADE, related_name = 'profiles')
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	avatar = models.ImageField(upload_to='avatars/',default='media/default_av.jpg')

	def __str__(self):
		return self.user.username


class CustomUser(AbstractUser):
	age = models.PositiveSmallIntegerField(null=True, blank=True)

	def get_absolute_url(self):
		return reverse('profile', kwargs={'pk':self.profiles.pk})

	