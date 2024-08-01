from rest_framework import serializers

from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategoryCreateUpdateSerializer(serializers.ModelSerializer):
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
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.department = validated_data.get('department', instance.department)
        instance.save()
        return instance



