from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .Serializers import RoomSerailizers


@api_view(['GET'])
def getRoute(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id',
    ]
    return Response(routes)


@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serailizer = RoomSerailizers(rooms, many=True)
    return Response(serailizer.data)


@api_view(['GET'])
def getRoom(request,pk):
    rooms = Room.objects.get(id=pk)
    serailizer = RoomSerailizers(rooms, many=False)
    return Response(serailizer.data)
