from django.shortcuts import render,get_object_or_404
from globalchat.models import PublicChatRoom,PublicRoomChatMessage
from django.http import JsonResponse

# Create your views here.

def Public_chat(request):
    gp_data=PublicChatRoom.objects.all()

    context={'groups':gp_data,'current_user': request.user}
    return render(request,'public_chats2.html',context)


def chat_room(request, room_name):
    try:
        # Fetch the chat room by title
        room = PublicChatRoom.objects.get(title=room_name)
    except PublicChatRoom.DoesNotExist:
        return JsonResponse({'error': 'Room not found'}, status=404)

    # Fetch the last 50 messages in the chat room
    messages = PublicRoomChatMessage.objects.filter(room=room).order_by('timestamp')[:50]
    
    # Create a list of message dictionaries to return as JSON
    message_list = [
        {
            'user_name': message.user.username,
            'content': message.content,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
        for message in messages
    ]

    # Return the room title and the messages in JSON format
    response_data = {
        'room': room.title,
        'messages': message_list,
        'current_user': request.user.username,
    }

    return JsonResponse(response_data)