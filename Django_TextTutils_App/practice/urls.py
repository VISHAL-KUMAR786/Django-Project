from . import view
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', view.index,name="index"),
    path('analyze', view.analyze,name="analyze"),
    path('message', view.message ,name="message")
]
