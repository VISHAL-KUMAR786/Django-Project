from django.http import HttpResponse
from django.shortcuts import render
from .models import Room


def index(request):
    rooms = Room.objects.all()
    content = {'rooms': rooms}
    return render(request, 'base/home.html', content)


def room(request, pk):
    room = None
    # for i in rooms:
    #     if i['id'] == int(pk):
    #         room = i
    room = Room.objects.get(id=pk)
    content = {'room': room}
    return render(request, 'base/room.html', content)
