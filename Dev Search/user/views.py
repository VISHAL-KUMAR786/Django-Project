import re
import django
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from project.models import Project, Tag
from .models import Profile, Skill, Message
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import CustomUserCreationForm, CustomProfileForm, skillForm, MessageForm
from django.contrib import messages
from django.db.models import Q
from .utils import searchProjects, paginateProfiles
from django.contrib.auth.decorators import login_required
# Create your views here.


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('user:Profile')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User name does not exit")
            return redirect('user:login')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.info(request, "Login Successfully")
            return redirect(request.GET['next'] if 'next' in request.GET else 'user:account')
        else:
            messages.error(request, "User or Password does not match")
            return redirect('user:login')

    return render(request, 'user/login_register.html')


def logoutUser(request):
    logout(request)
    messages.info(request, "Logout Successfully")
    return redirect('user:Home')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            # messages.success(request,'Register successfully')
            login(request, user)
            return redirect('user:edit-profile')  # redirect to profile
        else:
            messages.error(request, 'Some Error Occured During Registeration')

    content = {'page': page, 'form': form}
    return render(request, 'user/login_register.html', content)


def index(request):
    profiles, search_query = searchProjects(request)
    paginator, custom_range, profiles = paginateProfiles(request, profiles, 12)

    content = {'profiles': profiles, 'search_query': search_query,
               'paginator': paginator, 'custom_range': custom_range}
    return render(request, 'user/index.html', content)


def profile(request, pk):
    profile = Profile.objects.get(id=pk)

    majorSkill = profile.skill_set.exclude(desc="")
    minorSkill = profile.skill_set.filter(desc="")

    projects = profile.project_set.all()
    paginator, custom_range, projects = paginateProfiles(request, projects, 4)

    content = {'profile': profile, 'paginator': paginator, 'custom_range': custom_range,
               'majorSkill': majorSkill, 'minorSkill': minorSkill,'projects':projects}
    return render(request, 'user/profile.html', content) 


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile

    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    paginator1, custom_range1, skills = paginateProfiles(
        request, skills, 4)  # setting up for skill
    paginator, custom_range, projects = paginateProfiles(
        request, projects, 4)  # setting up for project

    content = {'profile': profile, 'skills': skills, 'projects': projects, 'paginator': paginator,
               'custom_range': custom_range, 'paginator1': paginator1, 'custom_range1': custom_range1}
    return render(request, 'user/account.html', content)


@login_required(login_url='login')
def editProfile(request):
    profile = request.user.profile
    form = CustomProfileForm(instance=profile)

    if request.method == 'POST':
        form = CustomProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user:account')

    content = {'form': form}
    return render(request, 'user/profile_form.html', content)


@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = skillForm()

    if request.method == 'POST':
        form = skillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, "Skill was created !")
            return redirect('user:account')

    content = {'form': form}
    return render(request, 'user/skill_form.html', content)


@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = skillForm(instance=skill)

    if request.method == 'POST':
        form = skillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill was updated !")
            return redirect('user:account')

    content = {'form': form}
    return render(request, 'user/skill_form.html', content)


@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == 'POST':
        skill.delete()
        messages.info(request, "Skill have been removed !")
        return redirect('user:account')

    content = {'skill': skill}
    return render(request, 'user/skill_delete.html', content)


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageReq = profile.messages.all()
    unReadCount = messageReq.filter(is_read=False).count()
    content = {'message': messageReq, 'unReadCount': unReadCount}
    return render(request, 'user/inbox.html', content)


@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    messageReq = profile.messages.get(id=pk)
    if messageReq.is_read == False:
        messageReq.is_read = True
        messageReq.save()
    content = {'messageReq': messageReq}
    return render(request, 'user/message.html', content)

# @login_required(login_url='login')


def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()
            messages.success(request, "Your Message was successfull send !")
            return redirect('user:Profile', pk=recipient.id)

    content = {'recipient': recipient, 'form': form}
    return render(request, 'user/message-form.html', content)
