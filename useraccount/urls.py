from django.urls import path
from useraccount import views

urlpatterns=[
    path("",views.home,name='home'),
    path("user/profile",views.UserProfile,name='user_profile'),
    path('reg',views.register_view,name='registration'),
    path('login/',views.Login,name='login'),

]