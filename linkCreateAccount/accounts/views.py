from django.shortcuts import render
from .serilaizers import LoginSerializer, RegisterSerializer, UserSerializer
from django.contrib.auth import authenticate
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
# Create your views here.

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user, None)[1]
        })

        
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )

        if not user:
            return Response({
                "error": "invalid email or passowrd no existing"
            }, status=400)

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user, None)[1]
        })


class UserApi(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user



# class UsersList(generics.ListAPIView):
#     serializer_class = UserListSerializer

#     # queryset = Members.objects.all()
#     filter_backends = [filters.SearchFilter]
#     search_fields  = ['^username']

#     # queryset = Members.objects.all()

#     def get_queryset(self):
#         # return self.request.user.members.all()
#         return Person.objects.exclude(username=self.request.user)