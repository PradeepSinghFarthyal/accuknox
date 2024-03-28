from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone


# Create your views here.

# SignUP API View
class SignupAPIView(generics.CreateAPIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({'message':serializer.data['email']+', created sucessfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login API View
class LoginAPIView(generics.CreateAPIView):
    def post(self, request):
        
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)

            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Search User
class UserSearchAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserSearchSerializer(data=request.data)
        if serializer.is_valid():
            search_keyword = serializer.validated_data.get('search_keyword', '').strip()
            if '@' in search_keyword:  # Search by email
                try:
                    user = User.objects.get(email__iexact=search_keyword)
                    serializer = UserSerializer(user)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except User.DoesNotExist:
                    return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            else:  # Search by name
                users = User.objects.filter(name__icontains=search_keyword)
                paginator = PageNumberPagination()
                result_page = paginator.paginate_queryset(users, request)
                serializer = UserSerializer(result_page, many=True)
                return paginator.get_paginated_response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

'''
For Rate Limit we can use Throttle Also 

REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',  # for anonymous user 
        'user': '1000/day' # for user
    }
}

'''    

# Send Friend Request
class SendFriendRequestAPIView(generics.CreateAPIView):
    serializer_class = SendFriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def post(self, serializer):
        # Check if the user has sent more than 3 friend requests within the last minute
        last_minute = timezone.now() - timezone.timedelta(minutes=1)
        num_requests = Friendship.objects.filter(sender=self.request.user, created_at__gte=last_minute).count()
        if num_requests >= 3:
            return Response({"error": "You have reached the limit of friend requests allowed per minute."}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        receiver_id = serializer.data.get('receiver_id')
        Friendship_data = Friendship(sender=self.request.user, receiver_id=receiver_id)
        Friendship_data.save()
        return Response({"success": "Friend request responded successfully."}, status=status.HTTP_200_OK)


# Respond to Friend Request ['accepted', 'rejected']
class RespondToFriendRequestAPIView(generics.UpdateAPIView):
    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        status_value = request.data.get('status')
        if status_value not in ['accepted', 'rejected']:
            return Response({"error": "Invalid status value."}, status=status.HTTP_400_BAD_REQUEST)
        instance.status = status_value
        instance.save()
        return Response({"success": "Friend request responded successfully."}, status=status.HTTP_200_OK)


# List Of accepted friend requets
class ListFriendsAPIView(generics.ListAPIView):
    serializer_class = FriendshipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Friendship.objects.filter(sender=user, status='accepted') | Friendship.objects.filter(receiver=user, status='accepted')


# List Of accepted friend requets
class ListPendingRequestsAPIView(generics.ListAPIView):
    serializer_class = FriendshipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Friendship.objects.filter(receiver=user, status='pending')