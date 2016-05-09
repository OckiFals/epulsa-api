from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from users.models import Customer


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
        "user": {
            "username": x,
            "password": x
        },
        "saldo": x,
        "phone": x,
        "provider": x
    }
    """
    user = UserSerializer()
    # url = serializers.HyperlinkedIdentityField(view_name='customer-detail')

    class Meta:
        model = Customer
        fields = ('id', 'user', 'saldo', 'phone', 'provider')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User(**user_data)
        user.save()
        customer = Customer(user=user, **validated_data)
        return customer

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
