from django.urls import path
from . import views

urlpatterns = [
    path("vendors/", views.vendors),
    path("vendors/<str:vendor_id>", views.vendor),
    path("purchase_orders/", views.purchase_orders),
    path("purchase_order/<int:po_id>/", views.purchase_order),
    path("purchase_orders/<int:po_id>/acknowledge", views.acknowledge),
    path("vendors/<str:vendor_id>/performance", views.performance),
]