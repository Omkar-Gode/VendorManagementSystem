# Vendor Management System - Omkar Gode

# setup instructions
- clone or download repo and extract it
- create virtual env using "python -m venv envName" at same level of extracted project
- move to that directory and activate environment using "envName/Scripts/activate.bat"
- after that, move to extracted project directory and run "pip install -r requirements.txt"
- run following commands 
    "python manage.py makemigrations"
    "python manage.py migrate"
- for running server run "python manage.py runserver"

for testing the apis, following are api endpoints.

# Api endpoints

1. POST - http://127.0.0.1:8000/api/vendors/ 
    endpoint for creating vendor

2. GET - http://127.0.0.1:8000/api/vendors/
    endpoint for getting list of vendors

3. GET - http://127.0.0.1:8000/api/vendors/{vendor_id}
    endpoint for getting vendor with given vendor id

4. DELETE - http://127.0.0.1:8000/api/vendors/{vendor_id}
    endpoint for deleting vendor with given vendor id

5. PUT - http://127.0.0.1:8000/api/vendors/{vendor_id}
    endpoint from updating vendor with given vendor id

6. GET - http://127.0.0.1:8000/api/purchase_orders/
    endpoint for getting all purchase orders

7. POST - http://127.0.0.1:8000/api/purchase_orders/
    endpoint for creating a purchase order

8. GET - http://127.0.0.1:8000/api/purchase_order/{po_id}
    endpoint for getting purchase order with po_id

9. PUT - http://127.0.0.1:8000/api/purchase_order/{po_id}
    endpoint for updating purchase order with po_id

10. DELETE - http://127.0.0.1:8000/api/purchase_order/{po_id}
    endpoint for deleting purchase order with po_id

11. POST - http://127.0.0.1:8000/api/purchase_orders/{po_id}/acknowledge
    endpoint for setting acknowledging purchase order with po_id

12. GET - http://127.0.0.1:8000/api/vendors/{vendor_id}/performance
    endpoint for getting Historical Performance of vendor with vendor_id


Thank You