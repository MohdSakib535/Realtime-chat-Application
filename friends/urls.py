from django.urls import path
from friends import views

urlpatterns=[
    path("new-explore",views.new_Explore_people,name="new_exlpore"),
    path("nf",views.friend_request_data.as_view(),name="friend_request_data")
   

]