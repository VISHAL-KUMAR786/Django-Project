from django.contrib import admin
from django.urls import path , include
from . import views


urlpatterns = [
    path('', views.index ,name="task-home"),
    path('update_tasks/<str:pk>/', views.updateTask ,name="task-update"),
    path('delete/<str:pk>/', views.deleteTask ,name="task-delete"),
]
