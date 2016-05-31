from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import status

from order.models import Order, OrderTurn
from order.serializer import OrderSerializer
from users.models import Customer, Counter


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


class OrderStream(APIView):
    """
    List order from customer for authenticated Counter.
    """
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request, format=None):
        counter = Counter.objects.get(user=request.user)
        orders = Order.objects.filter(counter=counter.id, status=1)
        serializer = OrderSerializer(orders, many=True, context={'request': request})
        return Response(serializer.data)


class CounterTurn(APIView):
    
    @staticmethod
    def get(request, format=None):
        request.session.modified = True
        if 'order' in request.GET:
            counter = Counter.objects.filter(is_online=1, saldo__gte = request.GET['order'])
        else:
            counter = Counter.objects.filter(is_online=1)

        order_turn = OrderTurn.objects.get(pk=1)

        if False:
            pass
        else:
            if counter.count() != order_turn.count:
                order_turn.turn = 0
                order_turn.count = counter.count()
                order_turn.save()
            else:
                if counter.count() - 1 == order_turn.turn:
                    order_turn.turn = 0
                    order_turn.save()
                else:
                    order_turn.turn = order_turn.turn + 1
                    order_turn.save()

            return Response({
                'counter': counter[order_turn.turn].id
            })


class CounterTurnSession(APIView):
    
    @staticmethod
    def get(request, format=None):
        request.session.modified = True
        if 'order' in request.GET:
            counter = Counter.objects.filter(is_online=1, saldo__gte = request.GET['order'])
        else:
            counter = Counter.objects.filter(is_online=1)

        if 'order_turn' not in request.session:
            request.session['order_turn'] = 0
            request.session['counter_count'] = counter.count()
            return Response({
                'status': 'New',
                'counter': counter[request.session.get('order_turn')].id
            })
        else:
            if counter.count() != request.session['counter_count']:
                request.session['order_turn'] = 0
                request.session['counter_count'] = counter.count()
            else:
                if counter.count() - 1 == request.session['order_turn']:
                    request.session['order_turn'] = 0
                else:
                    request.session['order_turn'] = request.session['order_turn'] + 1

            return Response({
                'counter': counter[request.session.get('order_turn')].id
            })