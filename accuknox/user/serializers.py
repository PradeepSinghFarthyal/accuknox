from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'name', 'password')

    def create(self, validated_data):
        print("Inside create")
      
        if not validated_data.get('name'):
            raise serializers.ValidationError({'error':'Users Must Have name'})
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})


class UserSearchSerializer(serializers.Serializer):
    search_keyword = serializers.CharField(max_length=255)


class SendFriendRequestSerializer(serializers.ModelSerializer):
    receiver_id = serializers.IntegerField()

    class Meta:
        model = Friendship
        fields = ['receiver_id']

    def validate(self, data):
        receiver_id = data.get('receiver_id')
        if not receiver_id:
            raise serializers.ValidationError("Receiver ID is required.")
        return data
    
class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = '__all__'  
