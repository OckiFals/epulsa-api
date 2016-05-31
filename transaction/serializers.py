from rest_framework import serializers
from transaction.models import TransactionOrder
from order.models import Order
from users.models import Customer, Counter


class TransactionOrderSerializer(serializers.ModelSerializer):
    counter = serializers.IntegerField(read_only=True)
    customer = serializers.IntegerField()
    order = serializers.IntegerField()
    total = serializers.IntegerField()

    class Meta:
        model = TransactionOrder

    def create(self, validated_data):
        counter_id = self.context['request'].user.counter.id
        counter = Counter.objects.get(pk=counter_id)
        customer = Customer.objects.get(
            pk=self.validated_data.get('customer')
        )
        order = Order.objects.get(
            pk=self.validated_data.get('order')
        )
        total = self.validated_data.get('total')

        customer.saldo = customer.saldo - total
        counter.saldo = counter.saldo - total
        counter.income = counter.income + total
        order.status = 3

        customer.save()
        counter.save()
        order.save()
        return TransactionOrder.objects.create(counter=counter_id, **validated_data)
