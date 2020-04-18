from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('new/', views.newTransaction , name = 'new-transaction'),
    path('home/activity' , views.activityView , name = 'activity'),
]
