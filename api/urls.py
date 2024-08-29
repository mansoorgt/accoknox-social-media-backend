
from django.urls import path
from api import views

urlpatterns = [
    path('sign-up',views.SignUpView.as_view()),
    path('login', views.LoginView.as_view(), name='login'),
    path('search',views.UserSearch.as_view()),
    path('send-request',views.SendFriendRequest.as_view()),
    path('get-pending-requests',views.GetPendingFriendRequest.as_view()),
    path("update-friend-request",views.UpdateFriendRequest.as_view()),
    path('get-all-friends',views.GetAllFriends.as_view())
]
