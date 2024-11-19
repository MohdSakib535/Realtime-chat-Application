from django.shortcuts import render
from rest_framework import routers ,viewsets
from rest_framework.response import Response
from friends.models import FriendList,FriendRequest
from friends.serializers import friends_Serializer,friends_request_Serializer,FriendsRequestSerializer
from Notification.models import Notification
from useraccount.models import CustomUser
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.views import APIView
# Create your views here.




def new_Explore_people(request):
    user=request.user
    context={}
    friends_data = FriendList.objects.filter(user=user).first()
    friend_ids = friends_data.friends.values_list('id', flat=True) if friends_data else []
    all_user_Data = CustomUser.objects.exclude(id__in=friend_ids).exclude(id=user.id)

    friends_Data=FriendList.objects.filter(user=user).first()
    if  friends_Data:
        friend_list=friends_Data.friends.all()
    else:
        friend_list=[]
        print('no friend list')

    request_data=FriendRequest.objects.filter(receiver=user,is_active=True)

    notification_data=Notification.objects.filter(target=user,read=False).select_related().order_by('-timestamp')
    notification_count = notification_data.count() 

    context['all_user']=all_user_Data
    context['friends']=friend_list
    context['request_data']=request_data
    context['notification_data']=notification_data
    context['notification_count']=notification_count
    return render(request,'explore2.html',context)




class friend_request_data(APIView):
    def get(request):
        friend_data=FriendRequest.objects.all()
        serializers_data=Friend_request_List(friend_data,many=True)
        return Response({"data":serializers_data})



class Friend_List(viewsets.ModelViewSet):
    queryset = FriendList.objects.all()
    serializer_class = friends_Serializer


class Friend_request_List(viewsets.ModelViewSet):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendsRequestSerializer
    
    def create(self,request,*args,**kwargs):
        params=request.data
        print('params-------',params)

        sender=params.get('user_id')

        action=params.get('action')
        if not sender or action not in ['accept','decline']:
            return Response({'status':'error','message':'error in data'})
        
        try:
            sender = CustomUser.objects.get(id=sender)
            print('sender data-----',sender)
        except CustomUser.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User does not exist.'}, status=404)
        
        # Retrieve the active friend request
        try:
            friend_request = FriendRequest.objects.get(sender=sender, receiver=request.user, is_active=True)
            print('freind data-------',friend_request)
        except FriendRequest.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Friend request does not exist.'}, status=404)
        

        if action =='accept':
            # Get or create FriendList for both users
            receiver_friend_list, created = FriendList.objects.get_or_create(user=request.user)
            sender_friend_list, created = FriendList.objects.get_or_create(user=sender)

             # Add each other as friends
            receiver_friend_list.friends.add(sender)
            sender_friend_list.friends.add(request.user)

             # Deactivate the friend request
            friend_request.is_active = False
            friend_request.save()



            # # check user is already exist or not in friendlist
            # exist_friend_data=FriendList.objects.filter(user=request.user).first()
            # if exist_friend_data:
            #     exist_friend_data.friends.add(sender)
            # else:
            #     add_friend_data=FriendList.objects.create(user=request.user)
            #     add_friend_data.friends.add(sender)

            # print(request.user)
            # friend_request.is_active = False
            # friend_request.save()

            notification = Notification.objects.create(
                target=sender,
                verb=f"{request.user} is accept your friend request",
                from_user=request.user,
                redirect_url='/friends/',  # Adjust the URL as needed
                content_type=ContentType.objects.get_for_model(friend_request),
                object_id=friend_request.id,

            )
            print("- notification data--",notification.verb)


            # Send real-time notification via channel layer
            channel_layer = get_channel_layer()
            print('channel layer--------',channel_layer)
            group_name = f"notification_user_{sender.id}"

            print('notif gp id----views.---',group_name)
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    'type': 'notification',  # This corresponds to the handler in the consumer
                    'notification': f'{notification.verb}',
                    'count': Notification.objects.filter(target=sender, read=False).count(),
                }
            )
            return Response({"status":"success"})
        
        if action =="decline":
            decline_friend_request_data=FriendRequest.objects.get(sender=sender)
            print("decline-----",decline_friend_request_data)
            decline_friend_request_data.is_active=False
            decline_friend_request_data.save()
            Notification.objects.create(
                target=sender,
                verb=f"{request.user.username} has declined your friend request.",
                from_user=request.user,
                redirect_url='/friends/',
                content_type=ContentType.objects.get_for_model(friend_request),
                object_id=friend_request.id,
            )
            return JsonResponse({'status':"decline"})
        
        




    






