from rest_framework import serializers

from .models import Membership


class MembershipSerializer(serializers.ModelSerializer):
    next_membership = serializers.SerializerMethodField()

    class Meta:
        model = Membership
        fields = '__all__'
        
    def get_next_membership(self, obj):
        if obj.next_membership:
            return MembershipSerializer(obj.next_membership).data
        return None


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
            'next_membership': {'required': False},
        }
        
    def update(self, instance, validated_data):
        instance.is_enabled = validated_data.get('is_enabled', instance.is_enabled)
        instance.rules = validated_data.get('rules', instance.rules)
        instance.benefits = validated_data.get('benefits', instance.benefits)
        instance.type = validated_data.get('type', instance.type)
        instance.name = validated_data.get('name', instance.name)
        instance.next_membership = validated_data.get('next_membership', instance.next_membership)
        instance.save()
        return instance
