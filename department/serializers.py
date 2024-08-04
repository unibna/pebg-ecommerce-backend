from rest_framework import serializers

from .models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name', 'description')
        extra_kwargs = {
            'id': {'read_only': True},
            'name': {'required': False},
            'description': {'required': False},
        }
        
    def create(self, validated_data):
        department = Department.objects.create(**validated_data)
        return department
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
