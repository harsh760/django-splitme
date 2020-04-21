from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('new/', views.newTransaction , name = 'new-transaction'),
    path('home/activity' , views.activityView , name = 'activity'),
    path('' , views.friendsView , name = 'friends'),
    path('home/friends/<int:f_id>' , views.gettransdatafriend , name = 'friendsdata'),
    path('home/friends/update/<int:t_id>' , views.updatefriend , name = 'friendsdataupdate'),
    path('home/friends/delete/<int:t_id>' , views.deleteexpense , name = 'deleteexpense'),
    path('showallgroups/' , views.showgroups , name = 'show-groups'),
    path('newgroup/' , views.addnewgroup , name = 'addgroup'),
    path('newgroup/addfriend/<int:g_id>', views.addfriendsingroup , name ='addfriendsingroup'),
    path('newgroup/removefriends/<int:u_id>', views.removefriends , name ='removefriend'),
]
