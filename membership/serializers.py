from rest_framework import serializers

from .models import Membership


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = '__all__'


class MembershipUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'is_enabled': {'required': False},
            'rules': {'required': False},
            'benefits': {'required': False},
            'type': {'required': False},
            'name': {'required': False},
        }
        
    def update(self, instance, validated_data):
        instance.is_enabled = validated_data.get('is_enabled', instance.is_enabled)
        instance.rules = validated_data.get('rules', instance.rules)
        instance.benefits = validated_data.get('benefits', instance.benefits)
        instance.type = validated_data.get('type', instance.type)
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
