"""
URL configuration for ChatApplication project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from useraccount import views as uv
from globalchat import views as GC
from privatechat import views as PV
from friends import views as F
from Notification import views as NV


router = routers.DefaultRouter()
router.register(r'user-data', uv.UserAccountView)
router.register('friend-list',F.Friend_List)
router.register('friend-request-list',F.Friend_request_List)
router.register('notification/data',NV.Notification_list,basename="notification_list")
router.register('read/data',NV.mark_notifications_as_read,basename="notification_read_data"),

# router.register('friends_data',PV.Friends_viewsets,basename="friend_dta")

urlpatterns = [
    path('admin/', admin.site.urls),
    
   
    # path("rl",uv.Requested_list,name='requested_list'),
    # path("ap",uv.Add_people,name='add_people'),
    # path("up",uv.UserProfile,name='user_profile'),
    path("",include('useraccount.urls')),

    # path('reg',uv.register_view,name='registration'),
    # path('l',uv.Login,name='login'),

    path("",include('globalchat.urls')),

    # path("pu",GC.Public_chat,name='public_url'),
    # path('chat/<str:room_name>/', GC.chat_room, name='chat_room'),

    path("",include('privatechat.urls')),

    # path('explore',PV.Explore_people,name='explore_people'),
    path("",include("friends.urls")),

    # path("",include('Notification.urls')),

    path("",include("videoCall.urls")),


    # API 
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),


]
