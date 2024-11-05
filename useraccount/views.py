from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from rest_framework import routers ,viewsets
from useraccount.models import CustomUser
from useraccount.serializers import user_account_Serializers
# Create your views here.


def home(request):
    return render(request,'home.html')

def Public_chat(request):
    return render(request,'public_chat.html')

def Private_chat(request):
    return render(request,'private_chats.html')

def Requested_list(request):
    return render(request,'requested_list.html')

def Add_people(request):
    return render(request,'addpeople.html')



def UserProfile(request):
    context={}
    user=request.user
    print('------',user)
    profile_data=CustomUser.objects.get(username=user)
    context['user_profile']=profile_data
    print('pro-----',profile_data)

    return render(request,'userProfile.html',context)



def register_view(request, *args, **kwargs):
    user=request.user
    print('user--',user)
    if request.method=="POST":
        username=request.POST['username']
        print('username',username)
        email=request.POST['email']
        print('username',email)
        password1=request.POST['password1']
        print('password1',password1)
        password2=request.POST['password2']
        print('password2',password2)

        if CustomUser.objects.filter(email=email).exists():
            return redirect('registration')
        
        if password1 == password2:
            
            registered_user=CustomUser.objects.create_user(username=username,email=email,password=password1)
            registered_user.save()

    return render(request,'home.html')



def Login(request):
    if request.method=='POST':
        email=request.POST['email']
        # print('----',email)
        password=request.POST['password']
        # print('---',password)
        user = authenticate(email=email,password=password)
        # print('--cd----',user)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return redirect('registration')
    

    return render(request,'home.html')


"""
API
"""

class UserAccountView(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = user_account_Serializers
