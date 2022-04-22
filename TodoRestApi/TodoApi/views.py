from turtle import title
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import *

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskSerializer
from TodoApi import serializers

# Create your views here.


@api_view(['GET'])
def taskApi(request):
    api_urls = {
        'List': '/task-list/',
        'Detail View': '/task-detail/<str:pk>',
        'Create': '/task-create/',
        'Update': '/task-update/<str:pk>/',
        'Delete': '/task-delete/<str:pk>',
    }
    return Response(api_urls)
    # return JsonResponse("Api urls here",safe=False)


@api_view(['GET'])
def taskList(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def taskDetail(request, pk):
    tasks = Task.objects.get(title=pk)
    serializer = TaskSerializer(tasks, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def taskCreate(request):
    # title = request.POST['title']
    # completed = request.POST['completed']
    # tasks = Task(title=title,completed=completed)
    # serializer = TaskSerializer(tasks, many=False)

    serializer = TaskSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['POST'])
def taskUpdate(request, pk):
    task = Task.objects.get(title=pk)

    serializer = TaskSerializer(instance=task, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def taskDelete(request, pk):
    task = Task.objects.get(id=pk).delete()

    return Response("Item Deleted Successfully !")
