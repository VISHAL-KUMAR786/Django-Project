from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('', views.getRoute), 
    path('rooms/', views.getRooms), 
    path('rooms/<str:pk>/', views.getRoom), 
]