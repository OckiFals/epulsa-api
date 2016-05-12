from rest_framework import serializers
from order.models import Order
from users.models import Customer


class OrderSerializer(serializers.ModelSerializer):
    """
    JSON serializable format
    {
        "id": x,
        "url": x,
        "customer": x,
        "purchase": xxxx,
        "phone_number": xxxxx,
        "status": x,
        "time": xxxxxxxxx
    }
    """
    id = serializers.IntegerField(read_only=True)
    # url = serializers.HyperlinkedIdentityField(view_name='order-detail')
    customer = serializers.ReadOnlyField(source='customer.id')
    purchase = serializers.IntegerField()
    phone_number = serializers.CharField(min_length=11, max_length=15)
    status = serializers.IntegerField(default=1)

    class Meta:
        model = Order
        fields = ('id', 'customer', 'purchase', 'phone_number', 'status', 'time')

    def create(self, validated_data):
        customer_id = self.context['request'].user.customer.id
        order = Order()
        order.customer = Customer.objects.get(pk=customer_id)
        order.purchase = validated_data.get('purchase')
        order.phone_number = validated_data.get('phone_number')
        return order

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
