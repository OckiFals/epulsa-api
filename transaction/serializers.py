from rest_framework import serializers
from transaction.models import TransactionCounter
from users.models import Customer, Counter


class TransactionCounterSerializer(serializers.ModelSerializer):
	counter = serializers.IntegerField(read_only=True)
	user2 = serializers.IntegerField()
	type = serializers.IntegerField()
	total = serializers.IntegerField()

	class Meta:
		model = TransactionCounter

	def create(self, validated_data):
		counter_id = self.context['request'].user.counter.id

		if 1 == self.validated_data.get('type'):
			counter = Counter.objects.get(pk=counter_id)
			customer = Customer.objects.get(
				user_id=self.validated_data.get('user2')
			)

			total = self.validated_data.get('total')

			customer.saldo = customer.saldo - total
			counter.saldo = counter.saldo - total
			counter.income = counter.income + total

			customer.save()
			counter.save()

		return TransactionCounter.objects.create(counter=counter_id, **validated_data)