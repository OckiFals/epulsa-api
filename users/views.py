from django.http import Http404
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from epulsa import settings
from users.models import Customer, Counter
from users.serializers import CustomerSerializer, CounterSerializer, AdminSerializer
from users.forms import LoginForm
from rest_framework_jwt.utils import jwt_payload_handler
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
import jwt

"""
Menggenerate token untuk credential yang valid
digunakan pada view login client
@route: /api/auth2/
"""


class TokenCreator(APIView):
    """
    Create token if user credentials was provided and valid.
    """

    # alamat ini hanya mendukung method POST
    def post(self, request, format=None):
        # validasi form 
        form = LoginForm(request.POST)
        # jika form valid
        if form.is_valid():
            # dapatkan credential dari username dan password
            credential = self.get_account_type(form.user)

            # kembalikan credential user beserta access token
            return Response({
                'user': credential['serializer'].data,
                'token': credential['token']
            })
        # jika gagal, kembalikan error
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    # memilah credential berdasatkan tipe akun
    def get_account_type(self, user):
        if self.is_customer(user):  # jika user adalah customer
            return {
                'token': self.create_token(user),
                'serializer': CustomerSerializer(user.customer),
            }
        elif self.is_counter(user):
            return {
                'token': self.create_token(user),
                'serializer': CounterSerializer(user.counter),
            }
        elif self.is_admin(user):
            return {
                'token': self.create_token(user),
                'serializer': AdminSerializer(user),
            }
        return None

    @staticmethod
    def create_token(user):
        payload = jwt_payload_handler(user)
        token = jwt.encode(payload, settings.SECRET_KEY)
        return token.decode('unicode_escape')

    @staticmethod
    def is_customer(user):
        try:
            Customer.objects.get(user=user)
        except Customer.DoesNotExist:
            return False
        return True

    @staticmethod
    def is_counter(user):
        try:
            Counter.objects.get(user=user)
        except Counter.DoesNotExist:
            return False
        return True

    @staticmethod
    def is_admin(user):
        try:
            User.objects.get(username=user.username, is_superuser=1)
        except User.DoesNotExist:
            return False
        return True


"""
Menampilkan list customer
digunakan pada view account/customer-all.php
@target: admin
@route: /user/customer/
"""


class CustomerList(APIView):
    """
    List all customer, or create a new customer.
    """

    # mendukung method get
    # mendapatkan semua data customer
    @staticmethod
    def get(request, format=None):
        # customer = User.objects.filter(groups__name='customer')
        customer = Customer.objects.filter(type=3)
        serializer = CustomerSerializer(customer, many=True, context={'request': request})
        return Response(serializer.data)

    # method HTTP post untuk membuat customer baru
    @staticmethod
    def post(request, format=None):
        # validasi form input menggunakan serializer
        serializer = CustomerSerializer(data=request.data, context={'request': request})
        # jika serializer valid
        if serializer.is_valid():
            # simpan data
            serializer.save()
            return Response(
                serializer.data,  # list customer dalam bentuk JSON
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
Menampilkan data customer spesifik
@target: admin
@route: /user/customer/[:id]
"""


class CustomerDetail(APIView):
    """
    Retrieve, update or delete a Customer instance.
    """

    # dapatkan customer berdasarkan primary key
    @staticmethod
    def get_object(pk):
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            raise Http404

    # method GET
    def get(self, request, pk, format=None):
        customer = self.get_object(pk)
        # ubah objek customer ke dalam format JSON
        serializer = CustomerSerializer(customer, context={'request': request})
        return Response(serializer.data)  # tampilkan data JSON

    # method put
    # memperbarui data customer
    def put(self, request, pk, format=None):
        customer = self.get_object(pk)

        # jika yang diperbarui hanya saldo saja
        if 'saldo' in request.POST:
            saldo = customer.saldo + int(request.POST.get('saldo'))
            serializer = CustomerSerializer(
                customer, data={'saldo': saldo, 'user': {}},
                context={'request': request}, partial=True
            )
        else:
            serializer = CustomerSerializer(customer, data=request.data, context={'request': request}, partial=True)

        # jika serializer valid
        if serializer.is_valid():
            # perbarui data
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # method DELETE
    # hapus customer dengan id tertentu
    def delete(self, request, pk, format=None):
        customer = self.get_object(pk)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
Menampilkan list counter
digunakan pada view account/counter-all.php
@target: admin
@route: /user/counter/
"""


class CounterList(APIView):
    """
    List all counter, or create a new counter.
    """
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request, format=None):
        counter = Counter.objects.all()
        serializer = CounterSerializer(counter, many=True, context={'request': request})
        return Response(serializer.data)

    @staticmethod
    def post(request, format=None):
        serializer = CounterSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CounterDetail(APIView):
    @staticmethod
    def get_object(pk):
        try:
            return Counter.objects.get(pk=pk)
        except Counter.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        counter = self.get_object(pk)
        serializer = CounterSerializer(counter, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        counter = self.get_object(pk)
        serializer = CounterSerializer(counter, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        counter = self.get_object(pk)
        counter.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminList(APIView):
    """
    List all admin, or create a new admin.
    """
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAdminUser,)

    @staticmethod
    def get(request, format=None):
        admin = User.objects.filter(is_superuser=1)
        serializer = AdminSerializer(admin, many=True, context={'request': request})
        return Response(serializer.data)

    @staticmethod
    def post(request, format=None):
        serializer = AdminSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminDetail(APIView):
    @staticmethod
    def get_object(pk):
        try:
            return User.objects.get(pk=pk, is_superuser=1)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        admin = self.get_object(pk)
        serializer = AdminSerializer(admin, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        admin = self.get_object(pk)
        req = request.data.copy()

        if admin.username == req.get('username'):
            del req['username']

        if '' == req.get('password'):
            del req['password']

        serializer = AdminSerializer(admin, data=req, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        admin = self.get_object(pk)
        admin.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# uji coba aja
class AuthTestView(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        content = {
            'status': 'authorizated',
            'user': unicode(request.auth),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(content)
