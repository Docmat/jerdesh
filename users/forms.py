from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Account


class UserRegistrationForm(UserCreationForm):

	class Meta:
		model = Account
		fields = ('email', 'username', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(UserRegistrationForm, self).__init__(*args, **kwargs)

		self.fields['email'].widget.attrs['class'] 			= 'input-text'
		self.fields['email'].widget.attrs['id'] 			= 'your-email'
		self.fields['email'].widget.attrs['placeholder'] 	= 'Ваш email'

		self.fields['username'].widget.attrs['class'] 		= 'input-text'
		self.fields['username'].widget.attrs['id'] 			= 'full-name'
		self.fields['username'].widget.attrs['placeholder'] = 'Логин'

		self.fields['password1'].widget.attrs['class'] 			= 'input-text'
		self.fields['password1'].widget.attrs['id'] 			= 'password'
		self.fields['password1'].widget.attrs['placeholder'] 	= 'Пароль'

		self.fields['password2'].widget.attrs['class'] 			= 'input-text'
		self.fields['password2'].widget.attrs['id'] 			= 'comfirm-password'
		self.fields['password2'].widget.attrs['placeholder'] 	= 'Повторите пароль'
