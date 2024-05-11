from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.utils import timezone
from datetime import datetime

from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .backendLogic import get_on_time_delivery_rate, get_fulfilment_rate, get_avg_response_time, get_quality_rating_avg

# Create your views here.


@api_view(["GET", "POST"])
def vendors(request):
    """
    on GET - This view returns list of Vendors
    on POST - This view creates new Vendor 
    """

    if request.method == "POST":
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            hp = HistoricalPerformance(vendor=serializer.data['vendor_code'])
            hp.save()
            return Response({"message":"vendor successfully created", "vendor":serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "GET":
        vendors = Vendor.objects.all()
        data = VendorSerializer(vendors, many=True).data

        return Response(data=data, status=status.HTTP_200_OK)


@api_view(["GET","PUT","DELETE"])
def vendor(request, vendor_id):
    """
    on GET - This view returns Vendor with given id
    on PUT - This view updates Vendor
    on DELETE - This view deletes Vendor 
    """

    if request.method == "GET":
        try:
            vendor = Vendor.objects.get(vendor_code=vendor_id)
            data = VendorSerializer(vendor).data
            return Response(data=data, status=status.HTTP_200_OK)
        except:
            return Response({"message":"No vendor found with given id"}, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "DELETE":
        try:
            vendor = Vendor.objects.get(vendor_code=vendor_id)
            vendor.delete()
            return Response({"message":"Vendor deleted successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({"message":"No vendor found with given id"}, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "PUT":
        try:
            vendor = Vendor.objects.get(vendor_code=vendor_id)
            serializer = VendorSerializer(vendor, request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"vendor successfully updated", "vendor":serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message":"No vendor found with given id"}, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(["GET", "POST"])
def purchase_orders(request):
    """
    on GET - This view returns all purchase orders
    on POST - This view creates new purchase order 
    """

    if request.method == "POST":
        if 'status' in request.data and request.data['status'] == "completed":
            request.data['order_date'] = timezone.now()
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            if serializer.data['status'] == 'completed':
                hp = HistoricalPerformance.objects.get(vendor=serializer.data["vendor"])
                hps = HistoricalPerformanceSerializer(hp, data={"on_time_delivery_rate":get_on_time_delivery_rate(serializer.data['vendor']), "quality_rating_avg":get_quality_rating_avg(serializer.data['vendor'])}, partial=True)
                if hps.is_valid():
                    hps.save()
                else:
                    return Response(hps.errors, status=status.HTTP_400_BAD_REQUEST)
            if 'status' in serializer.data:
                    hp = HistoricalPerformance.objects.get(vendor=serializer.data["vendor"])
                    hps = HistoricalPerformanceSerializer(hp, data={"fulfillment_rate":get_fulfilment_rate(serializer.data['vendor'])}, partial=True)
                    if hps.is_valid():
                        hps.save()
                    else:
                        return Response(hps.errors, status=status.HTTP_400_BAD_REQUEST)
                    
            return Response({"message":"purchase order successfully created", "purchase_order":serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == "GET":
        try:
            vendor = Vendor.objects.get(vendor_code=request.data["vendor_id"])
            purchase_orders = PurchaseOrder.objects.filter(vendor=vendor)
            data = PurchaseOrderSerializer(purchase_orders, many=True).data
            return Response(data=data, status=status.HTTP_200_OK)
        except:
            return Response({"message":"No vendor found with given id"}, status=status.HTTP_400_BAD_REQUEST)
        


@api_view(["GET", "DELETE", "PUT"])
def purchase_order(request, po_id):
    """
    on GET - This view returns purchase order with given id
    on PUT - This view updates purchase order
    on DELETE - This view deletes purcehase order  
    """

    if request.method == "GET":
        try:
            purchase_order = PurchaseOrder.objects.get(po_number=po_id)
            data = PurchaseOrderSerializer(purchase_order).data
            return Response(data=data, status=status.HTTP_200_OK)
        except:
            return Response({"message":"No Purchase Order found with given id"}, status=status.HTTP_400_BAD_REQUEST)
        
    if request.method == "DELETE":
        try:
            purchase_order = PurchaseOrder.objects.get(po_number=po_id)
            purchase_order.delete()
            return Response({"message":"Purchase Order deleted successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({"message":"No Purchase Order found with given id"}, status=status.HTTP_400_BAD_REQUEST)
        
    if request.method == "PUT":
        try:
            if 'status' in request.data and request.data['status'] == "completed":
                request.data['order_date'] = timezone.now()
            purchase_order = PurchaseOrder.objects.get(po_number=po_id)
            serializer = PurchaseOrderSerializer(purchase_order, request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                if serializer.data['status'] == 'completed':
                    hp = HistoricalPerformance.objects.get(vendor=serializer.data["vendor"])
                    hps = HistoricalPerformanceSerializer(hp, data={"on_time_delivery_rate":get_on_time_delivery_rate(serializer.data['vendor']), "quality_rating_avg":get_quality_rating_avg(serializer.data['vendor'])}, partial=True)
                    if hps.is_valid():
                        hps.save()
                    else:
                        return Response(hps.errors, status=status.HTTP_400_BAD_REQUEST)
                if 'status' in serializer.data:
                    hp = HistoricalPerformance.objects.get(vendor=serializer.data["vendor"])
                    hps = HistoricalPerformanceSerializer(hp, data={"fulfillment_rate":get_fulfilment_rate(serializer.data['vendor'])}, partial=True)
                    if hps.is_valid():
                        hps.save()
                    else:
                        return Response(hps.errors, status=status.HTTP_400_BAD_REQUEST)
                    
                return Response({"message":"Purchase Order successfully updated", "purchase_order":serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message":"No Purchase Order found with given id"}, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(["POST"])
def acknowledge(request, po_id):
    """
    on POST - This view updates acknowledgement_date of purchase order with given id
    """

    if request.method == "POST":
        try:
            purchase_order = PurchaseOrder.objects.get(po_number=po_id)
            serializer = PurchaseOrderSerializer(purchase_order, data={'acknowledgement_date':timezone.now()}, partial=True)
            if serializer.is_valid():
                serializer.save()
                print(serializer.data["vendor"])
                hp = HistoricalPerformance.objects.get(vendor=serializer.data["vendor"])
                hps = HistoricalPerformanceSerializer(
                    hp, 
                    data={"average_response_time":get_avg_response_time(serializer.data["vendor"])},
                    partial=True)
                
                if hps.is_valid():
                    hps.save()
                else:
                    return Response(hps.errors, status=status.HTTP_400_BAD_REQUEST)
                
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message":"No Purchase Order found with given id"}, status=status.HTTP_400_BAD_REQUEST)
        


@api_view(["GET"])
def performance(request, vendor_id):
    """
    on GET - This view returns historical performance of vendor with given id 
    """

    if request.method == "GET":
        try:
            vendor = Vendor.objects.get(vendor_code=vendor_id)
            hp = HistoricalPerformance.objects.get(vendor=vendor)
            data = HistoricalPerformanceSerializer(hp).data
            print(data)
            return Response(data=data, status=status.HTTP_200_OK)
        except:
            return Response({"message":"No Vendor found with given id"}, status=status.HTTP_400_BAD_REQUEST)
        