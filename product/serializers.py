from rest_framework import serializers

from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'department')
        extra_kwargs = {
            'id': {'read_only': True},
            'name': {'required': True},
            'department': {'required': True}
        }
        
    def create(self, validated_data):
        category = Category.objects.create(**validated_data)
        return category


class CategoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'name': {'required': False},
            'description': {'required': False},
            'department': {'required': False},
            'is_enabled': {'required': False},
        }
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.department = validated_data.get('department', instance.department)
        instance.is_enabled = validated_data.get('is_enabled', instance.is_enabled)
        instance.save()
        return instance


class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
        }
        
    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        return product


class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'name': {'required': False},
            'category': {'required': False},
            'description': {'required': False},
            'price': {'required': False},
            'stock': {'required': False},
            'is_enabled': {'required': False},
        }
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.category = validated_data.get('category', instance.category)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.stock = validated_data.get('stock', instance.stock)
        instance.is_enabled = validated_data.get('is_enabled', instance.is_enabled)
        instance.save()
        return instance

