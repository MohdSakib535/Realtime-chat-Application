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
from django.urls import path
from useraccount import views as uv
from globalchat import views as GC

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",uv.home,name='home'),
   
    path("pv",uv.Private_chat,name='private_url'),
    path("rl",uv.Requested_list,name='requested_list'),
    path("ap",uv.Add_people,name='add_people'),
    path("up",uv.UserProfile,name='user_profile'),

    path('reg',uv.register_view,name='registration'),
    path('l',uv.Login,name='login'),

    path("pu",GC.Public_chat,name='public_url'),
    path('chat/<str:room_name>/', GC.chat_room, name='chat_room'),

]
