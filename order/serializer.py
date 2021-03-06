from rest_framework import serializers
from order.models import Order, OrderTurn
from users.models import Customer, Counter


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
    counter = serializers.ReadOnlyField(source='counter.id')
    purchase = serializers.IntegerField()
    phone_number = serializers.CharField(min_length=11, max_length=15)
    status = serializers.IntegerField(default=1)

    class Meta:
        model = Order
        fields = ('id', 'customer', 'counter', 'purchase', 'phone_number', 'status', 'time')

    def create(self, validated_data):
        customer_id = self.context['request'].user.customer.id
        counter = Counter.objects.filter(saldo__gte = validated_data.get('purchase'))
        turn = OrderTurn.objects.get(pk=1).turn
        order = Order()
        order.customer = Customer.objects.get(pk=customer_id)
        order.counter = counter[turn]
        order.purchase = validated_data.get('purchase')
        order.phone_number = validated_data.get('phone_number')
        return order

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
