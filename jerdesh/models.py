from django.db import models
from django.conf import settings
from django.shortcuts import reverse

User = settings.AUTH_USER_MODEL


class Category(models.Model):
    category_text = models.CharField(max_length=100)

    def __str__(self):
        return self.category_text


class City(models.Model):
    city_text = models.CharField(max_length=200)

    def __str__(self):
        return self.city_text


class Ad(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    slug = models.SlugField(max_length=250, unique_for_date='pub_date')
    ad_title = models.CharField(max_length=200, verbose_name='Название')
    ad_text = models.TextField(verbose_name='Описание')
    img = models.ImageField(upload_to='images', blank=True)
    pub_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ad_text

    def get_absolute_url(self):
        return reverse('jerdesh:ad_details_url', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['-pub_date']


class Comment(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=255)
    text = models.TextField()
    post = models.ForeignKey(Ad, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} --- {self.post}"
