from django.shortcuts import render

# Create your views here.

def base(request,roomName):
    context={}
    print('r------',roomName)
    context['room_name']=roomName
    context['curent_user']=request.user.username
    print('context---------',context)

    return render(request,'video/base.html',context)



def add_user(request):

    return render(request,'video/add_user.html')





#API View

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Room
from .serializers import RoomSerializer

class RoomCreateAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        data['created_by'] = request.user.email  # Automatically set the logged-in user's email
        serializer = RoomSerializer(data=data)
        if serializer.is_valid():
            room = serializer.save()
            return Response({
                'message': 'Room created successfully!',
                'room': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)