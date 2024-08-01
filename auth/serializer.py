from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
)


class AuthTokenPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_id'] = user.id
        token['email'] = user.email
        return token
