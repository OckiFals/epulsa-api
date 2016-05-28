from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from users.models import Customer, Counter
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    JSON serializable format
    {
        "username": x,
        "password": x # -> write_only
    }
    """
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(min_length=5, max_length=15)
    password = serializers.CharField(min_length=8, max_length=15, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password')

    @staticmethod
    def validate_username(value):
        """
        Check that the username is unique.
        """
        try:
            User.objects.get(username=value)
        except User.DoesNotExist:
            return value
        raise serializers.ValidationError("That username has already taken.")


class CustomerSerializer(serializers.ModelSerializer):
    """
    JSON serializable format
    {
        "id": x,
        "url": x, # -> read_only
        "user": { # -> required on update
            "username": x,
            "password": x
        },
        "saldo": x,
        "phone": x,
        "provider": x
    }
    """
    user = UserSerializer()
    type = serializers.IntegerField(read_only=True)

    # url = serializers.HyperlinkedIdentityField(view_name='customer-detail')

    class Meta:
        model = Customer
        fields = ('id', 'user', 'saldo', 'phone', 'provider', 'type')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        return Customer.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user
        instance.saldo = validated_data.get('saldo', instance.saldo)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.provider = validated_data.get('provider', instance.provider)
        instance.save()
        user.username = user_data.get('username', user.username)
        if 'password' in user_data:
            user.password = make_password(user_data.get('password', user.password))
        user.save()
        return instance


class CounterSerializer(serializers.ModelSerializer):
    """
    JSON serializable format
    {
        "id": x,
        "url": x, # -> read_only
        "user": { # -> required on update
            "username": x,
            "password": x
        },
        "saldo": x,
        "income": x,
        "is_online": x
    }
    """

    user = UserSerializer()
    type = serializers.IntegerField(read_only=True)

    class Meta:
        model = Counter
        field = ('id', 'user', 'saldo', 'phone', 'income', 'is_online', 'type')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        return Counter.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user
        instance.saldo = validated_data.get('saldo', instance.saldo)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.income = validated_data.get('income', instance.income)
        instance.is_online = validated_data.get('is_online', instance.is_online)
        instance.save()
        user.username = user_data.get('username', user.username)
        if 'password' in user_data:
            user.password = make_password(user_data.get('password', user.password))
        user.save()
        return instance


class AdminSerializer(serializers.ModelSerializer):
    """
    JSON serializable format
    {
        "username": x,
        "password": x, # -> write_only
        "email": x,
        "first_name": x,
        "last_name": x
    }
    """
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(min_length=5, max_length=15)
    password = serializers.CharField(min_length=8, max_length=15, write_only=True)
    email = serializers.CharField(max_length=254, required=True)
    first_name = serializers.CharField(max_length=30, required=True)
    last_name = serializers.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')

    @staticmethod
    def validate_username(value):
        """
        Check that the username is unique.
        """
        try:
            User.objects.get(username=value)
        except User.DoesNotExist:
            return value
        raise serializers.ValidationError("That username has already taken.")

    def create(self, validated_data):
        return User.objects.create_user(
            is_superuser=1, is_staff=1, is_active=1, **validated_data
        )

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        if 'password' in validated_data:
            instance.password = make_password(validated_data.get('password', instance.password))
        instance.save()
        return instance
