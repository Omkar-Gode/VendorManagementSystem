from .models import Vendor, PurchaseOrder, HistoricalPerformance
from django.db.models import F, Sum, Q, Avg
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_aware, make_aware
from datetime import timezone
from rest_framework import serializers


def get_on_time_delivery_rate(vendorObject):
    total_completed_orders = PurchaseOrder.objects.filter(vendor=vendorObject, status="completed")
    in_time_completed_orders = total_completed_orders.filter(order_date__lte = F("delivery_date"))
    rate = len(in_time_completed_orders)/len(total_completed_orders)
    return rate
    
def get_quality_rating_avg(vendorObject):
    total_completed_orders = PurchaseOrder.objects.filter(vendor=vendorObject, status="completed")
    sum = total_completed_orders.aggregate(Sum("quality_rating"))['quality_rating__sum']
    return sum/len(total_completed_orders)


# def time_diff_in_hours(from_date, to_date):
#     diff = to_date -from_date
#     return (diff.days*24) + (diff.seconds/60)/60


def get_avg_response_time(vendorObject):
    acknowledged_orders = PurchaseOrder.objects.filter(vendor=vendorObject).filter(~Q(acknowledgement_date = None))
    if len(acknowledged_orders) == 0:
        return None
    diff = acknowledged_orders.annotate(diff=F('acknowledgement_date')-F('issue_date')).aggregate(Avg("diff"))["diff__avg"]
    return (diff.days*24) + (diff.seconds/60)/60


def get_fulfilment_rate(vendorObject):
    total_orders = PurchaseOrder.objects.filter(vendor=vendorObject)
    if len(total_orders) == 0:
        return None
    total_completed_orders = total_orders.filter(status="completed")
    if len(total_completed_orders) == 0:
        return None
    return len(total_completed_orders)/len(total_orders)


def get_parsed_datetime(datetime_string):
    parsed = parse_datetime(datetime_string)
    if not parsed:
        raise serializers.ValidationError("wrong date format it should be :  YYYY-MM-DD HH:MM:SS")
    if not is_aware(parsed):
        parsed = make_aware(parsed)
    return parsed



"""
from api.backendLogic import get_parsed_datetime
get_parsed_datetime("2024-05-11 16:57:00.024309")



from api.models import Vendor
from api.backendLogic import get_on_time_delivery_rate

from api.models import Vendor, PurchaseOrder
from api.backendLogic import get_avg_response_time
v = Vendor.objects.get(name="Omkar Gode")
get_avg_response_time(v)

from api.models import Vendor, PurchaseOrder
from api.backendLogic import get_fulfilment_rate
v = Vendor.objects.get(name="Omkar Gode")
get_fulfilment_rate(v)

get_on_time_delivery_rate(vendorObject = v)

"""
# PurchaseOrder.objects.