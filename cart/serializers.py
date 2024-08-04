from rest_framework import serializers

from .models import Cart, CartItem
from product.serializers import ProductSerializer


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    
    class Meta:
        model = CartItem
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
        }
        
        
class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'cart': {'read_only': True},
            'product': {'required': True},
            'quantity': {'required': True},
            'is_enabled': {'required': False},
            'is_deleted': {'required': False},
        }
        
    def create(self, validated_data):
        user = self.context['request'].user
        cart = Cart.objects.filter(user=user).first()
        if not cart:
            raise serializers.ValidationError('Cart not found')
        cart_item = CartItem.objects.create(**validated_data)
        return cart_item
    
    
class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'cart': {'read_only': True},
            'product': {'read_only': True},
            'quantity': {'required': False},
            'is_enabled': {'required': False},
            'is_deleted': {'required': False},
        }
        
    def update(self, instance, validated_data):
        instance.cart = validated_data.get('cart', instance.cart)
        instance.product = validated_data.get('product', instance.product)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.is_enabled = validated_data.get('is_enabled', instance.is_enabled)
        instance.is_deleted = validated_data.get('is_deleted', instance.is_deleted)
        instance.save()
        return instance
