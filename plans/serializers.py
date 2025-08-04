from rest_framework import serializers
from .models import Provider, Plans

class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ['id', 'title', 'discount_percentage','is_active']

class PlansSerializer(serializers.ModelSerializer):
    provider = ProviderSerializer(read_only=True)
    provider_id = serializers.IntegerField(write_only=True)
    discount_price = serializers.SerializerMethodField()
    class Meta:
        model = Plans
        fields = [
            'id', 'provider', 'provider_id', 'title', 'description', 
            'validity', 'is_active', 'amount', 'discount_price', 'identifier', 'created_at'
        ]
        read_only_fields = ['created_at']
    def get_discount_price(self, obj):
        if obj.provider and obj.provider.discount_percentage:
            discount = (obj.amount * obj.provider.discount_percentage) / 100
            return round(obj.amount - discount, 2)
        return obj.amount
class PlansListSerializer(serializers.ModelSerializer):
    provider = ProviderSerializer(read_only=True)
    discount_price = serializers.SerializerMethodField()
    class Meta:
        model = Plans
        fields = [
            'id', 'provider', 'title', 'description', 
            'validity', 'amount', 'discount_price', 'identifier', 'created_at'
        ]
    def get_discount_price(self, obj):
        if obj.provider and obj.provider.discount_percentage:
            discount = (obj.amount * obj.provider.discount_percentage) / 100
            return round(obj.amount - discount, 2)
        return obj.amount
    

class ProviderDiscountUpdateSerializer(serializers.ModelSerializer):
    discount_percentage = serializers.DecimalField(
        max_digits=5, decimal_places=2, required=False, allow_null=True
    )
    class Meta:
        model = Provider
        fields = ['id', 'title', 'discount_percentage']