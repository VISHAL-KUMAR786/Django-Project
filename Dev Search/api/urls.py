from django.urls import path , include
from . import views

app_name = 'api'

from rest_framework_simplejwt.views import (
    TokenObtainPairView, #generate json web token
    TokenRefreshView,#generate refresh web token
)

urlpatterns = [
    path('user/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', views.getRoutes),
    path('project/', views.getProjects),
    path('project/<str:pk>/', views.getProject),
    path('project/<str:pk>/vote/', views.projectVote),

    path('remove-tag/', views.removeTag),
]