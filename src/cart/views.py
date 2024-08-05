from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError, NotFound
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from . import models, serializers


class CartAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        cart = models.Cart.objects.filter(user=user).first()
        if not cart:
            cart = models.Cart.objects.create(user=user)
        serializer = serializers.CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartItemViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    serializer_class = serializers.CartItemSerializer
    permission_classes = [IsAuthenticated]
    queryset = models.CartItem.objects.all()

    def get_queryset(self):
        cart = models.Cart.objects.filter(
            user=self.request.user
        ).first()
        if not cart:
            raise ValidationError('Cart not found')
        return models.CartItem.objects.filter(
            cart=cart,
            is_deleted=False,
        )

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            raise NotFound('Method not allowed')
        return super().get_permissions()

    def perform_destroy(self, instance):
        if instance.cart.user != self.request.user:
            raise PermissionDenied('You can only delete your own cart items')
        instance.delete()


class CartItemCreateUpdateAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = models.Cart.objects.filter(user=request.user).first()
        if not cart:
            raise ValidationError('Cart not found')
        
        cart_item = models.CartItem.objects.filter(
            cart=cart,
            product=request.data['product']
        ).first()

        if cart_item:
            serializer = serializers.CartItemUpdateSerializer(
                cart_item,
                data=request.data
            )
        else:
            serializer = serializers.CartItemCreateSerializer(
                data=request.data, 
                context={'request': request}
            )
        serializer.is_valid(raise_exception=True)
        serializer.save(cart=cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
