from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from epulsa.serializers import UserSerializer, GroupSerializer
from transaction.models import TransactionOrder, TransactionFunds
from transaction.serializers import TransactionOrderSerializer
from rest_framework import status


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class TransactionListOrder(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request, format=None):
        if 'type' in request.GET:
            transaction = TransactionOrder.objects.filter(customer=request.user.customer.id)
        else:
            transaction = TransactionOrder.objects.filter(counter=request.user.counter.id)

        serializer = TransactionOrderSerializer(transaction, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request, format=None):
        serializer = TransactionOrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)