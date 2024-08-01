from rest_framework_simplejwt.views import TokenObtainPairView


from .serializer import AuthTokenPairSerializer


class AuthTokenPairAPIView(TokenObtainPairView):
    serializer_class = AuthTokenPairSerializer
