from django.shortcuts import render
from .serilaizers import LinkToRegisterPermissionSerializer, LoginSerializer, RegisterSerializer, UserSerializer
from django.contrib.auth import authenticate
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from knox.models import AuthToken
from .models import LinkToRegisterPermission
# Create your views here.

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, code, form=None):
        # print(code)
        # request.data._mutable=True
        # request.data["code"] = code
        # print(request.data["code"])
        # request.data._mutable=False
        for code_key in LinkToRegisterPermission.objects.all():
            if code_key.code == code:    
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                user = serializer.save()
                code_key.delete()
                return Response({
                    "user": UserSerializer(user, context=self.get_serializer_context()).data,
                    "token": AuthToken.objects.create(user, None)[1]
                })
        return Response({
                    "error": "Valid register url"
                }, status=status.HTTP_406_NOT_ACCEPTABLE)

class CreateRegisterUrl(generics.GenericAPIView):
    serializer_class = LinkToRegisterPermissionSerializer

    def post(self, request, form=None):
        # print(code)
        # request.data._mutable=True
        # request.data["code"] = code
        # print(request.data["code"])
        # request.data._mutable=False
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.save()
        return Response({
            "url": f"http://127.0.0.1:8000/api/register/{code.code}/",
        }, status=status.HTTP_200_OK)
        
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