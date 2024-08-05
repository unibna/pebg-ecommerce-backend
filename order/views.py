from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView


from . import models, serializers
from cart.models import CartItem


class OrderViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_permissions(self):
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        cart_item_ids = request.data.get('cart_items', [])
        validated_cart_items = CartItem.objects.filter(
            id__in=cart_item_ids,
            cart__user=request.user,
            is_enabled=True,
            is_deleted=False
        )
        if len(validated_cart_items) != len(cart_item_ids):
            raise ValidationError('Invalid cart items')

        order = models.Order.objects.filter(
            user=request.user,
            status=models.enums.OrderStatusEnum.DRAFT
        ).first()
        with transaction.atomic():
            if order:
                if order.status != models.enums.OrderStatusEnum.DRAFT:
                    raise PermissionDenied('Cannot create order')

                models.OrderItem.objects.filter(order=order).delete()
                serializers.OrderSerializer(order, )
            else:
                order = models.Order.objects.create(user=request.user)

            new_order_items_batch = []
            for cart_item in validated_cart_items:
                new_order_items_batch.append(
                    models.OrderItem(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity,
                        price=cart_item.product.price
                    )
                )
            models.OrderItem.objects.bulk_create(new_order_items_batch)
            order.update_total_amount()

        serializer = serializers.OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        order = self.get_object()
        serializer = serializers.OrderItemSerializer(order.order_items.all(), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def checkout(self, request, pk=None):
        order = self.get_object()
        if order.status != models.enums.OrderStatusEnum.DRAFT:
            raise PermissionDenied('Cannot update order')
        order.status = models.enums.OrderStatusEnum.PAYMENT_COMPLETED
        order.save()
        serializer = serializers.OrderSerializer(order)
        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def process(self, request, pk=None):
        order = self.get_object()
        if order.status != models.enums.OrderStatusEnum.PAYMENT_COMPLETED:
            raise PermissionDenied('Cannot update order')
        order.status = models.enums.OrderStatusEnum.PROCESSING
        order.save()
        serializer = serializers.OrderSerializer(order)
        return Response(serializer.data)
    
    @action(detail=True, methods=['put'])
    def deliver(self, request, pk=None):
        order = self.get_object()
        if order.status != models.enums.OrderStatusEnum.PROCESSING:
            raise PermissionDenied('Cannot update order')
        order.status = models.enums.OrderStatusEnum.DELIVERING
        order.save()
        serializer = serializers.OrderSerializer(order)
        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def complete(self, request, pk=None):
        order = self.get_object()
        # if order.status != models.enums.OrderStatusEnum.DELIVERING:
        #     raise PermissionDenied('Cannot update order')
        order.status = models.enums.OrderStatusEnum.COMPLETED
        order.save()
        serializer = serializers.OrderSerializer(order)
        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        if order.status != models.enums.OrderStatusEnum.COMPLETED:
            raise PermissionDenied('Cannot update order')
        order.status = models.enums.OrderStatusEnum.CANCELED
        order.save()
        serializer = serializers.OrderSerializer(order)
        return Response(serializer.data)


class OrderItemViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = models.OrderItem.objects.all()
    serializer_class = serializers.OrderItemSerializer
    
    def get_queryset(self):
        return self.queryset.filter(order__user=self.request.user)

    def get_permissions(self):
        if self.action in ['create']:
            raise NotFound()
        return super().get_permissions()
    
    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return serializers.OrderItemUpdateSerializer
        return self.serializer_class
    
    def perform_update(self, serializer):
        instance = serializer.save()
        instance.order.update_total_amount()
