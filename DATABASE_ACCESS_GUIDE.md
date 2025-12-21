# Database Access Guide

This guide shows you how to access and view your database tables in the Jewellery Billing System.

## Method 1: Django Admin Interface (Easiest - Recommended)

The Django Admin provides a web-based interface to view and manage all your database tables.

### Steps:

1. **Start the Django server** (if not already running):
   ```bash
   python manage.py runserver
   ```

2. **Create a superuser** (if you haven't already):
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create an admin account.

3. **Access the admin panel**:
   - Open your browser and go to: `http://127.0.0.1:8000/admin/`
   - Login with your superuser credentials

4. **Available Tables in Admin**:
   - **Customers** - View, add, edit, delete customers
   - **Bills** - View all bills with filters and search
   - **Bill Items** - View individual items in bills
   - **Old Gold** - View old gold exchanges
   - **Payments** - View payment records
   - **Gold Rates** - View and manage gold rates
   - **Users** - Manage user accounts

### Features:
- ✅ Search and filter records
- ✅ Add, edit, delete records
- ✅ View related records (e.g., items in a bill)
- ✅ Export data (with extensions)

---

## Method 2: Django Shell (Command Line)

Use Django's interactive Python shell to query the database programmatically.

### Steps:

1. **Open Django shell**:
   ```bash
   python manage.py shell
   ```

2. **Example Queries**:

   ```python
   # Import models
   from billing.models import Customer, Bill, BillItem, OldGold, Payment, GoldRate
   from django.contrib.auth.models import User
   
   # View all customers
   customers = Customer.objects.all()
   for customer in customers:
       print(f"{customer.name} - {customer.phone}")
   
   # Count records
   print(f"Total Customers: {Customer.objects.count()}")
   print(f"Total Bills: {Bill.objects.count()}")
   
   # Get a specific customer
   customer = Customer.objects.get(name="Rohit Sharma")
   
   # Get all bills for a customer
   bills = Bill.objects.filter(customer=customer)
   for bill in bills:
       print(f"Bill {bill.bill_number}: ₹{bill.net_payable}")
   
   # Get items in a bill
   bill = Bill.objects.first()
   items = bill.items.all()
   for item in items:
       print(f"{item.description}: {item.net_weight}gm - ₹{item.amount}")
   
   # Filter bills by date
   from datetime import date
   today_bills = Bill.objects.filter(bill_date__date=date.today())
   
   # Search customers
   customers = Customer.objects.filter(name__icontains="rohit")
   
   # Get recent bills
   recent_bills = Bill.objects.order_by('-bill_date')[:10]
   ```

3. **Exit shell**:
   ```python
   exit()
   ```

---

## Method 3: SQLite Browser (GUI Tool)

Use a graphical tool to browse the SQLite database directly.

### Recommended Tools:

1. **DB Browser for SQLite** (Free, Cross-platform)
   - Download: https://sqlitebrowser.org/
   - Steps:
     1. Install DB Browser for SQLite
     2. Open the tool
     3. Click "Open Database"
     4. Navigate to: `C:\Users\rohit\Desktop\AstraByte\JwelleryBillingSoftware\db.sqlite3`
     5. Browse tables in the left sidebar
     6. View data, run SQL queries, export data

2. **SQLiteStudio** (Free, Cross-platform)
   - Download: https://sqlitestudio.pl/
   - Similar interface to DB Browser

3. **VS Code Extension** (If using VS Code)
   - Install "SQLite Viewer" extension
   - Right-click `db.sqlite3` → "Open Database"

### Database Location:
```
C:\Users\rohit\Desktop\AstraByte\JwelleryBillingSoftware\db.sqlite3
```

---

## Method 4: Direct SQL Queries via Django Shell

Run raw SQL queries if needed.

### Steps:

1. **Open Django shell**:
   ```bash
   python manage.py shell
   ```

2. **Run SQL queries**:
   ```python
   from django.db import connection
   
   # Get cursor
   cursor = connection.cursor()
   
   # Execute query
   cursor.execute("SELECT * FROM billing_customer")
   rows = cursor.fetchall()
   
   # Get column names
   columns = [col[0] for col in cursor.description]
   
   # Print results
   for row in rows:
       print(dict(zip(columns, row)))
   ```

---

## Method 5: Django Management Commands

Create custom management commands for specific queries.

### Example: View Database Summary

Create a file: `billing/management/commands/db_summary.py`

```python
from django.core.management.base import BaseCommand
from billing.models import Customer, Bill, BillItem, Payment

class Command(BaseCommand):
    help = 'Display database summary'

    def handle(self, *args, **options):
        self.stdout.write("=== Database Summary ===")
        self.stdout.write(f"Customers: {Customer.objects.count()}")
        self.stdout.write(f"Bills: {Bill.objects.count()}")
        self.stdout.write(f"Bill Items: {BillItem.objects.count()}")
        self.stdout.write(f"Payments: {Payment.objects.count()}")
```

Then run:
```bash
python manage.py db_summary
```

---

## Quick Reference: Table Names

Django creates tables with app prefix. Your tables are:

- `billing_customer` - Customer information
- `billing_bill` - Bills/Invoices
- `billing_billitem` - Items in bills
- `billing_oldgold` - Old gold exchanges
- `billing_payment` - Payment records
- `billing_goldrate` - Gold rate history
- `auth_user` - User accounts
- `django_session` - Session data

---

## Tips:

1. **Backup Database**: Always backup before making changes
   ```bash
   copy db.sqlite3 db.sqlite3.backup
   ```

2. **Export Data**: Use Django admin or shell to export to CSV/JSON

3. **View Table Structure**: In Django shell
   ```python
   from billing.models import Bill
   print(Bill._meta.get_fields())
   ```

4. **Check Database Size**:
   ```bash
   dir db.sqlite3
   ```

---

## Recommended Approach:

- **For daily use**: Django Admin (`/admin/`)
- **For data analysis**: Django Shell
- **For database inspection**: DB Browser for SQLite
- **For complex queries**: Django Shell with ORM

