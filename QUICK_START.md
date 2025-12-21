# Quick Start Guide

## ✅ Installation Complete!

Your Django application is now set up. Follow these steps to get started:

### 1. Create a Superuser Account

Run this command and follow the prompts to create your admin account:

```bash
python manage.py createsuperuser
```

You'll be asked for:
- Username
- Email (optional)
- Password (twice)

### 2. Start the Development Server

```bash
python manage.py runserver
```

### 3. Access the Application

- **Main Application**: http://127.0.0.1:8000
- **Admin Panel**: http://127.0.0.1:8000/admin

### 4. Login

Use the superuser credentials you just created to login.

## Important Notes

### PDF Generation (WeasyPrint)

The application will run normally, but **PDF generation requires GTK3 runtime** on Windows:

1. **To enable PDF generation**, download and install GTK3 Runtime:
   - https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer
   - After installation, restart your terminal

2. **Alternative**: Use the browser's print function (Ctrl+P) from the bill print page

### First Steps

1. **Set Gold Rate**: Go to Dashboard and update the current gold rate
2. **Create Customers**: Navigate to Customers → New Customer
3. **Create Bills**: Click "New Bill" from the dashboard
4. **View Reports**: Check the Reports section for sales statistics

## Troubleshooting

- **WeasyPrint Warning**: This is normal if GTK3 is not installed. The app works fine without it.
- **Static Files**: If styles don't load, run: `python manage.py collectstatic`
- **Database Issues**: Delete `db.sqlite3` and run migrations again if needed

Enjoy your Jewellery Billing Software! 💎

