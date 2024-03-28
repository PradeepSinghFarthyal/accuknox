from django.urls import path
from user import views

urlpatterns = [
    path('signup/', views.SignupAPIView.as_view(), name='Signup'),
    path('login/', views.LoginAPIView.as_view(), name='Login'),
    path('search/', views.UserSearchAPIView.as_view(), name='SearchUser'),
    # Request's API
    path('send_request/', views.SendFriendRequestAPIView.as_view(), name='SendFriendRequest'),
    path('respond-friend-request/<int:pk>/', views.RespondToFriendRequestAPIView.as_view(), name='Respond Friend Request'),
    path('accepted_request/', views.ListFriendsAPIView.as_view(), name='AcceptedRequestUser'),
    path('pending_request/', views.ListPendingRequestsAPIView.as_view(), name='PendingRequestUser'),
]
