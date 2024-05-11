from datetime import datetime, timezone 

from api.models import PurchaseOrder, HistoricalPerformance
 
a= PurchaseOrder(delivery_date=datetime.now().replace(tzinfo=timezone.utc), items={}, quantity=3, status='pending', quality_rating=1.2)



PurchaseOrder(vendor=a, order_date=datetime(2024,5,15,10,30).replace(tzinfo=timezone.utc), delivery_date=datetime(2024,5,15,12).replace(tzinfo=timezone.utc), items={'smartphone':1, 'charger':1}, quantity=2, status="completed", acknowledgement_date=datetime(2024,5,11,11,30).replace(tzinfo=timezone.utc))

PurchaseOrder(vendor=a, order_date=datetime(2024,5,17,10,30).replace(tzinfo=timezone.utc), delivery_date=datetime(2024,5,13,12).replace(tzinfo=timezone.utc), items={'laptop':1, 'case':3}, quantity=4, status="completed", acknowledgement_date=datetime(2024,5,12,11,30).replace(tzinfo=timezone.utc))

PurchaseOrder(vendor=a, order_date=datetime(2024,5,15,10,30).replace(tzinfo=timezone.utc), delivery_date=datetime(2024,5,15,12).replace(tzinfo=timezone.utc), items={'smartphone':1, 'toy':2}, quantity=3, status="pending", acknowledgement_date=datetime(2024,5,11,11,30).replace(tzinfo=timezone.utc))