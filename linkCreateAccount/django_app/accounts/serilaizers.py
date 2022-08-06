from rest_framework import serializers
# from django.contrib.auth.models import User
from .models import Person, LinkToRegisterPermission
from django.contrib.auth import authenticate
# User Serializer

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'username')
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'username', 'email')

# Register Serializer
class LinkToRegisterPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkToRegisterPermission
        fields = ('id', 'code', 'created')
        extra_kwargs = {'created': {'read_only': True}}

class RegisterSerializer(serializers.ModelSerializer):
    # code = serializers.CharField()
    class Meta:
        model = Person
        fields = ('id',  'email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Person.objects.create_user(
            validated_data['email'], validated_data['username'], validated_data['password'])

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()