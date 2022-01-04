from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from . models import User
from . import serializers
from drf_yasg.utils import swagger_auto_schema

class UserCreateView(generics.GenericAPIView):
    
    serializer_class = serializers.UserCreationSerializer 
    @swagger_auto_schema(operation_summary="Create a user account")
    def post(self,request):
        data = request.data 
        # password = request.data['password']
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)