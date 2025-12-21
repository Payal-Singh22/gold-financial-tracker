# Jewellery Billing Software

A complete web-based billing system for jewellery stores built with Django, featuring bill creation, gold rate management, customer management, PDF generation, and email functionality.

## Features

- **Authentication System**: Secure login/logout functionality
- **Dashboard**: Overview with statistics and recent bills
- **Gold Rate Management**: Update and track current gold rates
- **Bill Creation**: 
  - Multiple items per bill
  - Auto-calculation of fine gold (Net weight × Tunch / 100)
  - Auto-calculation of totals
  - Old gold exchange adjustment
  - Tax calculations (CGST/SGST)
- **Customer Management**: Create, update, and manage customers
- **Bill Management**: 
  - View, edit, and delete bills
  - Bill history and search
  - Payment tracking
- **Print & PDF**: 
  - Print-friendly A5 bill layout
  - PDF generation for bills
- **Email**: Send bills as PDF via email
- **Reports**: Sales reports with date filtering
- **Mobile Responsive**: Bootstrap 5 responsive design

## Technology Stack

- **Backend**: Django 4.2.7 (Python)
- **Frontend**: Django Templates + Bootstrap 5
- **Database**: SQLite (default), PostgreSQL ready
- **PDF Generation**: WeasyPrint
- **Forms**: Django Crispy Forms
- **JavaScript**: Vanilla JS (no frameworks)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or navigate to the project directory**
   ```bash
   cd JwelleryBillingSoftware
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser (admin account)**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create an admin user.

6. **Collect static files**
   ```bash
   python manage.py collectstatic --noinput
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Open your browser and go to: `http://127.0.0.1:8000`
   - Login with the superuser credentials you created

## Project Structure

```
JwelleryBillingSoftware/
├── billing/                 # Main app
│   ├── models.py           # Database models
│   ├── views.py            # View functions and class-based views
│   ├── forms.py            # Django forms
│   ├── urls.py             # URL routing
│   ├── admin.py            # Admin configuration
│   └── migrations/         # Database migrations
├── jewellery_billing/      # Project settings
│   ├── settings.py         # Django settings
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py             # WSGI configuration
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   └── billing/           # App-specific templates
├── static/                # Static files
│   ├── css/              # Stylesheets
│   └── js/               # JavaScript files
├── media/                 # User uploaded files
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Database Models

- **User**: Django's built-in user model (authentication)
- **Customer**: Customer information (name, phone, email, address)
- **GoldRate**: Current gold rate tracking
- **Bill**: Main bill model with totals and status
- **BillItem**: Individual items in a bill
- **OldGold**: Old gold exchange records
- **Payment**: Payment tracking for bills

## Usage Guide

### 1. Setting Up Gold Rate

1. Go to Dashboard
2. Update the gold rate in the top section
3. Click the save button to update

### 2. Creating a Customer

1. Navigate to **Customers** from the menu
2. Click **New Customer**
3. Fill in customer details
4. Save

### 3. Creating a Bill

1. Click **New Bill** from the dashboard or menu
2. Select a customer
3. Add items:
   - Click **Add Item**
   - Enter description, net weight, tunch, and rate
   - Fine gold and amount are calculated automatically
4. Add old gold exchange (if applicable):
   - Enter weight, rate, and description
   - Click **Add Old Gold**
5. Adjust tax percentages if needed (default: 1.5% CGST, 1.5% SGST)
6. Enter cash received
7. Click **Create Bill**

### 4. Viewing and Managing Bills

- **View Bills**: See all bills with search and filter options
- **Bill Detail**: View complete bill details, add payments
- **Print**: Print-friendly view
- **PDF**: Download bill as PDF
- **Email**: Send bill as PDF to customer's email

### 5. Reports

- Navigate to **Reports**
- Filter by date range
- View sales statistics and bill details

## Configuration

### Database (PostgreSQL)

To use PostgreSQL instead of SQLite, update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'jewellery_billing',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Email Configuration

For production email, update `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'
```

### Static Files

In production, configure your web server to serve static files, or use:
```bash
python manage.py collectstatic
```

## Development

### Running Tests

```bash
python manage.py test
```

### Creating Migrations

After modifying models:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Accessing Admin Panel

1. Go to: `http://127.0.0.1:8000/admin`
2. Login with superuser credentials
3. Manage all models from the admin interface

## Troubleshooting

### WeasyPrint Installation Issues (PDF Generation)

**Note:** The application will run without WeasyPrint, but PDF generation will not work until GTK3 runtime is installed.

**On Windows:**
1. Download and install GTK3 Runtime from:
   - https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer
   - Or: https://www.gtk.org/docs/installations/windows/
2. After installation, restart your terminal/command prompt
3. The application will automatically detect WeasyPrint once GTK3 is installed

**On Linux:**
```bash
sudo apt-get install python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
```

**Alternative:** If you don't need PDF generation, you can use the print function (Ctrl+P) from the browser instead.

### Static Files Not Loading

1. Ensure `DEBUG = True` in development
2. Run `python manage.py collectstatic`
3. Check `STATIC_URL` and `STATICFILES_DIRS` in settings.py

### Database Issues

1. Delete `db.sqlite3` and migrations folder (except `__init__.py`)
2. Run `python manage.py makemigrations`
3. Run `python manage.py migrate`

## Security Notes

- Change `SECRET_KEY` in `settings.py` for production
- Set `DEBUG = False` in production
- Configure `ALLOWED_HOSTS` properly
- Use HTTPS in production
- Keep dependencies updated

## License

This project is provided as-is for educational and commercial use.

## Support

For issues or questions, please check the code comments or Django documentation.

## Future Enhancements

- Barcode scanning for items
- Inventory management
- Advanced reporting with charts
- Multi-currency support
- Backup and restore functionality
- API endpoints for mobile apps

