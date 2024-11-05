from django.shortcuts import render
from  useraccount.models import CustomUser
from friends.models import FriendList,FriendRequest
from django.shortcuts import get_object_or_404
# Create your views here.
def Explore_people(request):
    user=request.user
    print('user-----',user)
    context={}
    all_user_Data=CustomUser.objects.all()
    # print('----all user----',all_user_Data)


    friends_Data=FriendList.objects.filter(user=user).first()
    # print("freind-----",friends_Data)
    if  friends_Data:
        friend_list=friends_Data.friends.all()
    else:
        friend_list=[]
        print('no friend list')


    # requested list

   
    


    request_data=FriendRequest.objects.filter(receiver=user,is_active=True)
    print('req----',request_data)
    # for i in request_data:
    for i in request_data:
        print(i.receiver.username)

    # print(request_data.receiver.username)
    # request_list=request_data.receiver.all()
    # for i in request_data.receiver:
    #     print(i.username)
    


    context['all_user']=all_user_Data
    context['friends']=friend_list
    context['request_data']=request_data



    return render(request,'explore_people.html',context)
    # return render(request,'e1.html',context)