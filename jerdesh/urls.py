from django.urls import path, include
from . import views


app_name = 'jerdesh'
urlpatterns = [
	path('', views.IndexPage.as_view(), name='index_url'),
	path('ads/', views.AdList.as_view(), name='ads_list_url'),
	path('ad/create/', views.AdCreate.as_view(), name='ad_create_url'),
	path('ad/<str:slug>/', views.AdDetails.as_view(), name='ad_details_url'),
	path('comment/<int:pk>/', views.AddComment.as_view(), name='add_comment'),
]
