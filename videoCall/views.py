from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.db import models
from Notification.models import Notification
from useraccount.models import CustomUser
from privatechat.models import PrivateChatRoom
from .models import Room, Call

def _build_room_name(user_a: CustomUser, user_b: CustomUser) -> str:
    """Create a deterministic room name for a user pair."""
    sorted_ids = sorted([user_a.id, user_b.id])
    return f"video_{sorted_ids[0]}_{sorted_ids[1]}"


@login_required
def base(request, roomName):
    room = get_object_or_404(Room, name=roomName)

    if request.user not in room.participants.all():
        room.participants.add(request.user)

    active_call = Call.objects.filter(room=room, is_active=True).order_by('-started_at').first()

    call_id = request.GET.get('call')
    if call_id:
        active_call = Call.objects.filter(room=room, id=call_id).first() or active_call

    context = {
        'room_name': roomName,
        'curent_user': request.user.username,
        'other_user_name': None,
        'other_user_id': None,
        'call_id': active_call.id if active_call else None,
        'end_call_url': reverse('videoCall:end_call', args=[active_call.id]) if active_call else None,
    }

    if active_call:
        other_user = active_call.callee if active_call.caller == request.user else active_call.caller
        context['other_user_name'] = other_user.username
        context['other_user_id'] = other_user.id

    return render(request, 'video/base.html', context)


@login_required
def start_video_call(request, user_id):
    other_user = get_object_or_404(CustomUser, id=user_id)

    if other_user == request.user:
        return HttpResponseForbidden("You cannot start a call with yourself.")

    room_exists = PrivateChatRoom.objects.filter(
        (models.Q(user1=request.user) & models.Q(user2=other_user)) |
        (models.Q(user1=other_user) & models.Q(user2=request.user))
    ).exists()

    if not room_exists:
        return HttpResponseForbidden("You do not have permission to call this user.")

    room_name = _build_room_name(request.user, other_user)
    room, _ = Room.objects.get_or_create(name=room_name, defaults={'created_by': request.user})
    room.participants.add(request.user, other_user)

    active_call = Call.objects.filter(room=room, is_active=True).order_by('-started_at').first()

    created_new_call = False

    if active_call and {active_call.caller_id, active_call.callee_id} == {request.user.id, other_user.id}:
        call = active_call
    else:
        Call.objects.filter(room=room, is_active=True).update(is_active=False, ended_at=timezone.now())
        call = Call.objects.create(room=room, caller=request.user, callee=other_user)
        created_new_call = True

    url = f"{reverse('videoCall:room', kwargs={'roomName': room_name})}?call={call.id}"

    if created_new_call:
        Notification.objects.create(
            target=other_user,
            from_user=request.user,
            verb=f"{request.user.username} is calling you.",
            redirect_url=url,
            content_type=ContentType.objects.get_for_model(call),
            object_id=call.id,
        )

        unread_count = Notification.objects.filter(target=other_user, read=False).count()

        channel_layer = get_channel_layer()
        sorted_ids = sorted([request.user.id, other_user.id])
        chat_group = f"chat_{sorted_ids[0]}_{sorted_ids[1]}"

        async_to_sync(channel_layer.group_send)(
            chat_group,
            {
                'type': 'video_call_invite',
                'call_url': url,
                'call_id': call.id,
                'caller_id': request.user.id,
                'caller_name': request.user.username,
                'target_id': other_user.id,
            }
        )

        async_to_sync(channel_layer.group_send)(
            f"notification_user_{other_user.id}",
            {
                'type': 'notification',
                'notification': f"Incoming video call from {request.user.username}",
                'count': unread_count,
                'event': 'incoming_call',
                'call_url': url,
                'caller_id': request.user.id,
                'caller_name': request.user.username,
            }
        )

    return redirect(url)


@login_required
@require_POST
def end_video_call(request, call_id):
    call = get_object_or_404(Call, id=call_id)

    if request.user not in [call.caller, call.callee]:
        return HttpResponseForbidden("You are not part of this call.")

    if call.is_active:
        call.is_active = False
        call.ended_at = timezone.now()
        call.save(update_fields=['is_active', 'ended_at'])

    return JsonResponse({'status': 'ended'})


def add_user(request):
    return render(request, 'video/add_user.html')





#API View

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import RoomSerializer

class RoomCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['created_by'] = request.user.email  # Automatically set the logged-in user's email
        serializer = RoomSerializer(data=data)
        if serializer.is_valid():
            room = serializer.save()
            return Response({
                'message': 'Room created successfully!',
                'room': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
