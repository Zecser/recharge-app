from rest_framework import serializers
from .models import Provider, Plans

class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ['id', 'title', 'discount_percentage', 'point_value', 'is_active']

class PlansSerializer(serializers.ModelSerializer):
    provider = ProviderSerializer(read_only=True)
    provider_id = serializers.IntegerField(write_only=True)
    discount_price = serializers.SerializerMethodField()
    point_discount = serializers.SerializerMethodField()
    class Meta:
        model = Plans
        fields = [
            'id', 'provider', 'provider_id', 'title', 'description', 
            'validity', 'is_active', 'amount', 'discount_price', 'point_discount','identifier', 'created_at'
        ]
        read_only_fields = ['created_at']
    def get_discount_price(self, obj):
        if obj.provider and obj.provider.discount_percentage and obj.provider.point_value:
            discount = float(obj.provider.point_value) * float(obj.provider.discount_percentage) / 100
            return round(float(obj.amount) - discount, 2)
        return float(obj.amount)

    def get_point_discount(self, obj):
        if obj.provider and obj.provider.discount_percentage and obj.provider.point_value:
            return round(float(obj.provider.point_value) * float(obj.provider.discount_percentage) / 100, 2)
        return 0.0
class PlansListSerializer(serializers.ModelSerializer):
    provider = ProviderSerializer(read_only=True)
    discount_price = serializers.SerializerMethodField()
    point_discount = serializers.SerializerMethodField()
    class Meta:
        model = Plans
        fields = [
            'id', 'provider', 'title', 'description', 
            'validity', 'amount', 'discount_price','point_discount', 'identifier', 'created_at'
        ]
    def get_discount_price(self, obj):
        if obj.provider and obj.provider.discount_percentage and obj.provider.point_value:
            discount = float(obj.provider.point_value) * float(obj.provider.discount_percentage) / 100
            return round(float(obj.amount) - discount, 2)
        return float(obj.amount)

    def get_point_discount(self, obj):
        if obj.provider and obj.provider.discount_percentage and obj.provider.point_value:
            return round(float(obj.provider.point_value) * float(obj.provider.discount_percentage) / 100, 2)
        return 0.0
    

class ProviderDiscountUpdateSerializer(serializers.ModelSerializer):

    discount_percentage = serializers.DecimalField(
        max_digits=5, decimal_places=2, required=False, allow_null=True
    )
    point_value = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )
    class Meta:
        model = Provider
        fields = ['id', 'title', 'discount_percentage', 'point_value']