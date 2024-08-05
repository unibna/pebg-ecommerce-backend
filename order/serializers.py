from rest_framework import serializers

from .models import Order, OrderItem
from .enums import OrderStatusEnum


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
        
        
class OrderItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'order': {'read_only': True},
            'product': {'read_only': True},
            'price': {'read_only': True},
            'quantity': {'required': False},
        }
        
        
class OrderSerializer(serializers.ModelSerializer):    
    order_items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        exclude = ['user']
