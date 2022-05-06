from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Room, Topic, Message
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm  # registration
from .form import RoomForm
from django.db.models import Q


def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('base:Home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username does'nt exits.")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('base:Home')
        else:
            messages.error(request, 'Username or Password does not exits .')

    content = {'page': page}
    return render(request, 'base/login_register.html', content)


def logoutUser(request):
    logout(request)
    return redirect('base:Home')


def registerUser(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('base:Home')
        else:
            messages.error(request, 'An Error occur during registeration.')

    content = {'form': form}
    return render(request, 'base/login_register.html', content)


def index(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # do pagination at this
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q)
    )[:3]

    content = {'rooms': rooms, 'topics': topics,
               'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', content)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()  # many to many no need of _set

    if request.method == 'POST':
        if request.POST.get('body') == '':
            messages.error(request, 'Empty comment are not allowed')
            return redirect('base:room', pk=room.id)

        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )

        room.participants.add(request.user)
        return redirect('base:room', pk=room.id)

    content = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    return render(request, 'base/room.html', content)


def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    content = {'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request, 'base/profile.html', content)


@login_required(login_url='base:login')
def createRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('base:Home')
        pass

    content = {'form': form}
    return render(request, 'base/room_form.html', content)


@login_required(login_url='base:login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    # we are able to update our own room
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('base:Home')

    content = {'form': form}
    return render(request, 'base/room_form.html', content)


@login_required(login_url='base:login')
def deleteRoom(request, pk):
    obj = Room.objects.get(id=pk)

    # we are able to update our own room
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        obj.delete()
        return redirect('base:Home')

    content = {'obj': obj}
    return render(request, 'base/delete_room.html', content)


@login_required(login_url='base:login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('base:Home')  # update to that particular page

    content = {'obj': message}
    return render(request, 'base/delete_room.html', content)
