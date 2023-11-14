from django.urls import path
from users import views


urlpatterns = [
    path('', views.profiles, name='profiles'),
    path('userProfie/<str:pk>/', views.userProfie, name='userProfie'),
    path('account', views.useraccount, name='account'),


    path('editaccount', views.editaccount, name='editaccount'),


    path('createskill', views.createskill, name='createskill'),
    path('update-skill/<str:pk>/', views.updateskill, name='update-skill'),
    path('deleteskills/<str:pk>/', views.deleteskills, name='deleteskills'),


    path('login', views.loginuser, name='login'),
    path('logout', views.logoutuser, name='logout'),
    path('register', views.registeruser, name='register'),


    path('inbox', views.inbox, name='inbox'),
    path('viewmessage/<str:pk>', views.viewmessage, name='viewmessage'),
    path('createmessage/<str:pk>', views.createmessage, name='createmessage'),
    
]