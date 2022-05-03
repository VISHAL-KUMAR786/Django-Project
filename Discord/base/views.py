from django.http import HttpResponse
from django.shortcuts import render

rooms = [
    {'id': 1, 'name': 'Lets Learn Python!'},
    {'id': 2, 'name': 'Design with me'},
    {'id': 3, 'name': 'frontend developers'},
]


def index(request):
    content = {'rooms':rooms}
    return render(request, 'base/home.html',content)


def room(request,pk):
    content = {'pk':pk}
    return render(request, 'base/room.html',content)
