from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('new/', views.newTransaction , name = 'new-transaction'),
    path('home/activity' , views.activityView , name = 'activity'),
    path('home/friends' , views.friendsView , name = 'friends'),
    path('home/friends/<int:f_id>' , views.gettransdatafriend , name = 'friendsdata'),
    path('home/friends/update/<int:t_id>' , views.updatefriend , name = 'friendsdataupdate'),
    path('home/friends/delete/<int:t_id>' , views.deleteexpense , name = 'deleteexpense'),
    
]
