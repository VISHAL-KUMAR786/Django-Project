from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Room, Topic
from .form import RoomForm


def index(request):
    q = request.GET.get('q') if request.GET.get('q')!= None else ''
    rooms = Room.objects.filter(topic__name__icontains=q)

    topics = Topic.objects.all()
    content = {'rooms': rooms,'topics':topics}
    return render(request, 'base/home.html', content)


def room(request, pk):
    room = None
    # for i in rooms:
    #     if i['id'] == int(pk):
    #         room = i
    room = Room.objects.get(id=pk)
    content = {'room': room}
    return render(request, 'base/room.html', content)

def createRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('base:Home')
        pass 

    content = {'form':form}
    return render(request,'base/room_form.html',content)

def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('base:Home')

    content = {'form':form}
    return render(request,'base/room_form.html',content)

def deleteRoom(request,pk):
    obj = Room.objects.get(id=pk)

    if request.method == 'POST':
        obj.delete()
        return redirect('base:Home')

    content = {'obj': obj}
    return render(request,'base/delete_room.html',content)