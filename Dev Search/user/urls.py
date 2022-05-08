from django.urls import path , include
from . import views 

app_name = 'user'

urlpatterns = [
    path('', views.index , name="Home"),
    path('login/', views.loginUser , name="login"),
    path('logout/', views.logoutUser , name="logout"),
    path('register/', views.registerUser , name="register"),
    path('account/', views.userAccount , name="account"),
    path('editProfile/', views.editProfile , name="edit-profile"),
    path('createSkill/', views.createSkill , name="create-skill"),
    path('inbox/', views.inbox , name="inbox"),
    path('viewMessage/<str:pk>/', views.viewMessage , name="viewMessage"),
    path('createMessage/<str:pk>/', views.createMessage , name="createMessage"),
    path('deleteSkill/<str:pk>/', views.deleteSkill , name="delete-skill"),
    path('updateSkill/<str:pk>/', views.updateSkill , name="update-skill"),
    path('profile/<str:pk>/', views.profile , name="Profile"),
]