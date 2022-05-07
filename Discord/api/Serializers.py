from rest_framework.serializers import ModelSerializer
from base.models import Room 

class RoomSerailizers(ModelSerializer):
    class Meta:
        model = Room 
        fields ='__all__'
    pass 