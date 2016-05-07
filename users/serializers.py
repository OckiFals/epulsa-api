from rest_framework import serializers
from users.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name='customer-detail')

    class Meta:
        model = Customer
        fields = ('id', 'username', 'name', 'saldo', 'phone', 'provider', 'url')

    @staticmethod
    def get_username(obj):
        return obj.user.username

    @staticmethod
    def get_name(obj):
        return "%s %s" % (obj.user.first_name, obj.user.last_name)
