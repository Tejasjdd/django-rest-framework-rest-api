from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from . models import Order
from . import serializers
from authentication.models import User
from . serializers import OrderCreationSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from django.core.mail import send_mail
# from django.contrib.auth import get_user_model

# User = get_user_model()
# change permission_classes
class OrderCreateListView(generics.GenericAPIView):
    serializer_class = serializers.OrderCreationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="List all orders made")
    def get(self,request):
        orders = Order.objects.all()
        serializer = self.serializer_class(instance=orders,many=True) 
        return Response(data=serializer.data,status=status.HTTP_200_OK)  

    @swagger_auto_schema(operation_summary="Create a new order")    
    def post(self,request):      
        data = request.data
        print(data)
        serializer = self.serializer_class(data=data)
        user = request.user
        if serializer.is_valid():
            serializer.save(customer=user)
            send_mail(
                'Your order from Biryani Restaurant',
                'Thank you for ordering Biryani',
                'tejasjdorge@gmail.com',
                [user.email],
                fail_silently=False,
            )
            return Response(data=serializer.data,status=status.HTTP_200_OK)            
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class OrderDetailView(generics.GenericAPIView):
    serializer_class = serializers.OrderDetailSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(operation_summary="Retrieve an order")
    def get(self,request,order_id):
        order = get_object_or_404(Order,pk=order_id)
        serializer = self.serializer_class(instance=order)
        return Response(data=serializer.data,status=status.HTTP_200_OK)  

    @swagger_auto_schema(operation_summary="Update an order by id")    
    def put(self,request,order_id):
        data = request.data
        if data["order_status"]=="DELIVERED":
            response = {
                        "message": "Sorry you can't change status after delivery"
                    }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        order = get_object_or_404(Order,pk=order_id)
        serializer = self.serializer_class(data=data,instance=order)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Delete an order")
    def delete(self,request,order_id):
        order = get_object_or_404(Order,pk=order_id)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
class UpdateOrderStatus(generics.GenericAPIView):
    serializer_class = serializers.OrderStatusUpdateSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(operation_summary="Update an order's status")
    def put(self,request,order_id):
        order = get_object_or_404(Order,pk=order_id)
        data = request.data
        if data["order_status"]=="DELIVERED":
            response = {
                        "message": "Sorry you can't change status after delivery"
                    }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(data=data,instance=order)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_200_OK)

        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserOrderView(generics.GenericAPIView):
    serializer_class = serializers.OrderDetailSerializer

    @swagger_auto_schema(operation_summary="Get all orders for a user")
    def get(self,request,user_id):
        user = User.objects.get(pk=user_id)
        orders = Order.objects.all().filter(customer=user)
        serializer = self.serializer_class(instance=orders,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

class UserOrderDetail(generics.GenericAPIView):
    serializer_class = serializers.OrderDetailSerializer

    @swagger_auto_schema(operation_summary="Get a user's specific order")
    def get(self,request,user_id,order_id):
        user = User.objects.get(pk=user_id)
        order = Order.objects.get(Q(customer=user),Q(id=order_id)) 
        serializer = self.serializer_class(instance=order)
        return Response(data=serializer.data,status=status.HTTP_200_OK)