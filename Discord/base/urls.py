from django.contrib import admin
from django.urls import path
from . import views

app_name = 'base'

urlpatterns = [
    path('', views.index , name="Home"),
    path('room/<str:pk>/', views.room , name="room"),
]
