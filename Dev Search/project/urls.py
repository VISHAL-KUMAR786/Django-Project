from django.contrib import admin
from django.urls import path
from . import views 

app_name = 'project'

urlpatterns = [
    path('', views.index , name="Home"),
    path('createproject/', views.createProject , name="Create"),
    path('updateproject/<str:pk>/', views.updateProject , name="Update"),
    path('deleteproject/<str:pk>/', views.deleteProject , name="Delete"),
    path('<str:pk>/', views.about , name="About"),
]
