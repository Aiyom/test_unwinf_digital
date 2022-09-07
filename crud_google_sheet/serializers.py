from rest_framework import serializers
from .models import Orders


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = [f'{f.name}' for f in Orders._meta.get_fields()]