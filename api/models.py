from django.db import models
import string, random
from django.utils import timezone



# Create your models here.

# from datetime import datetime, timezone
# def get_date_time():
#     return datetime.now().replace(tzinfo=timezone.utc)

def get_vendor_code():
    flag = True
    N = 10

    while(flag == True):
        res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
        try:
            v = Vendor.objects.get(vendor_code=res)
            continue
        except:
            return res


class Vendor(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    vendor_code = models.CharField(primary_key=True, max_length=10, default=get_vendor_code)
    contact_details = models.TextField(max_length=10, null=False, blank=False)
    address = models.TextField(null=False, blank=False, default="user address")

    def __str__(self):
        return f"{self.name} - {self.vendor_code}"


class PurchaseOrder(models.Model):
    status_choices = (
        ("pending", "pending"),
        ("completed", "completed"),
        ("canceled", "canceled")
    )

    po_number = models.AutoField(primary_key=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(null=True, blank=True)
    delivery_date = models.DateTimeField(null=False, blank=False)
    items = models.JSONField(null=False, blank=False, default=dict)
    quantity = models.IntegerField(null=False, blank=False)
    status = models.CharField(choices=status_choices, max_length=9, default="pending")
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgement_date = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return f"{self.po_number}: {self.status} by {self.vendor}"




class HistoricalPerformance(models.Model):

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(null=False, blank=False, default=timezone.now)
    on_time_delivery_rate = models.FloatField(null=True, blank=True)
    quality_rating_avg = models.FloatField(null=True, blank=True)
    average_response_time = models.FloatField(null=True, blank=True)
    fulfillment_rate = models.FloatField(null=True, blank=True)

    # def __str__(self):
    #     return f"{self.name} : {self.date}"



# HistoricalPerformanceSerializer(hp, {"on_time_delivery_rate":get_on_time_delivery_rate, "quality_rating_avg":"", "average_response_time":""})