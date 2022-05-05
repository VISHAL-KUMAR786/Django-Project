from django.contrib import admin
from django.urls import path
from . import views

app_name = 'base'

urlpatterns = [
    path("login/", views.loginPage, name="login"), 
    path("logout/", views.logoutUser, name="logout"), 
    path("register/", views.registerUser, name="register"), 

    path('', views.index , name="Home"),
    path('create-room/', views.createRoom , name="createRoom"),
    path('room/<str:pk>/', views.room , name="room"),
    path('delete-room/<str:pk>/', views.deleteRoom , name="deleteRoom"),
    path('update-room/<str:pk>/', views.updateRoom , name="updateRoom"),
]
