from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import status

from order.models import Order
from order.serializer import OrderSerializer
from users.models import Customer


class OrderList(APIView):
    """
    List all order for authenticated customer, or create a new order instance.
    """
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request, format=None):
        customer = Customer.objects.get(user=request.user)
        orders = Order.objects.filter(customer=customer.id, status=1)
        serializer = OrderSerializer(orders, many=True, context={'request': request})
        return Response(serializer.data)

    @staticmethod
    def post(request, format=None):
        serializer = OrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            order = serializer.save()
            order.save()
            return Response(
                OrderSerializer(order, context={'request': request}).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetail(APIView):
    """
    Retrieve or update a Order instance.
    """
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get_object(request, pk):
        try:
            order = Order.objects.get(pk=pk)
            if request.user.id is not order.customer.user.id:
                raise Http404
            return order
        except Order.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        order = self.get_object(request, pk)
        serializer = OrderSerializer(order, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        order = self.get_object(pk)
        serializer = OrderSerializer(order, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            order = serializer.save()
            order.save()
            return Response(data=serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)