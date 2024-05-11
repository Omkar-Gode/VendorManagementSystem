from rest_framework import serializers
from .models import Vendor, PurchaseOrder, HistoricalPerformance

from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_aware, make_aware



class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

    def validate(self, attrs):
        if not attrs['name'].replace(" ", "").isalpha():
            raise serializers.ValidationError("name is invalid")
        if not attrs['contact_details'].isnumeric():
            raise serializers.ValidationError("contact detail is invalid")
        if len(attrs['contact_details']) < 10 or len(attrs['contact_details']) > 10:
            raise serializers.ValidationError("contact detail is invalid")
        
        return super().validate(attrs)
    

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'
    
    # def validate(self, attrs):
    #     if attrs['status'] not in ["pending", "completed", "canceled"]:
    #         raise serializers.ValidationError("invalid status")
    #     if not parse_datetime(attrs["delivery_date"]):
    #         raise serializers.ValidationError("wrong date format it should be :  YYYY-MM-DD HH:MM:SS")
    #     return super().validate(attrs)
    
    # def create(self, validated_data):
    #     parsed = parse_datetime(validated_data["delivery_date"])
    #     if not is_aware(parsed):
    #         parsed = make_aware(parsed)
    #     validated_data['delivery_date'] = parsed

    #     purchase_order = PurchaseOrder.objects.create(validated_data)

    #     return purchase_order
    

class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'
