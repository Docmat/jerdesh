from django.urls import path
from . import views


app_name = 'users'
urlpatterns = [
	path('registration/', views.userRegistration, name='user_registration_url'),
	path('authorization/', views.userAuthorization, name='user_authorization_url'),
	path('logout/', views.userLogout, name='user_logout_url'),
]
