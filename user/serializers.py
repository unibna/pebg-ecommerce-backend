from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User, UserRole
from .enums import UserRoleEnum


class UserActivationSerializer(serializers.Serializer):
    activation_token = serializers.UUIDField()
    
    def validate_activation_token(self, value):
        if not User.objects.filter(activation_token=value, is_active=False).exists():
            raise serializers.ValidationError("Invalid or expired activation code.")
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name')


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    password = serializers.CharField(
        required=True, validators=[validate_password])
    password2 = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'password2', 'first_name', 'last_name')
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True},
            'password2': {'write_only': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        else:
            attrs.pop('password2')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(
        write_only=True, required=False, validators=[validate_password])
    password2 = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'password2', 'first_name', 'last_name')
        extra_kwargs = {
            'id': {'read_only': True},
        }
        
    def validate(self, attrs):
        if 'password' in attrs and 'password2' in attrs:
            if attrs['password'] != attrs['password2']:
                raise serializers.ValidationError(
                    {"password": "Password fields didn't match."})
            else:
                attrs.pop('password2')
        return attrs


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ('id', 'role')
