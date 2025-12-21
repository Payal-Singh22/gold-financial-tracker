# Setup Instructions for Jewellery Billing Software

## Issue: Pillow Installation on Python 3.13

If you're using Python 3.13 (like Python 3.13.2), you may encounter issues installing Pillow 10.1.0. The requirements.txt has been updated to use Pillow >=10.3.0 which supports Python 3.13.

## Installation Steps

### Option 1: Install with Updated Requirements (Recommended)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   If Pillow still fails, try installing it separately first:
   ```bash
   pip install Pillow
   pip install -r requirements.txt
   ```

### Option 2: Use a Virtual Environment (Best Practice)

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

3. **Upgrade pip:**
   ```bash
   python -m pip install --upgrade pip
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Option 3: Install Packages Individually

If you continue to have issues, install packages one by one:

```bash
pip install Django==4.2.7
pip install django-crispy-forms==2.1
pip install crispy-bootstrap5==0.7
pip install Pillow
pip install WeasyPrint
pip install django-environ==0.11.2
```

## After Installation

Once all packages are installed successfully:

1. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

3. **Collect static files:**
   ```bash
   python manage.py collectstatic --noinput
   ```

4. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

5. **Access the application:**
   - Open browser: `http://127.0.0.1:8000`
   - Login with your superuser credentials

## Troubleshooting

### If Pillow installation still fails:

1. **Try installing pre-built wheel:**
   ```bash
   pip install --upgrade pip
   pip install --only-binary :all: Pillow
   ```

2. **Or use conda (if available):**
   ```bash
   conda install pillow
   ```

### If WeasyPrint installation fails:

WeasyPrint requires system dependencies. On Windows, it should work with pip. If it fails:

1. **Install GTK3 runtime** (if needed):
   - Download from: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer

2. **Or use an alternative PDF library:**
   - Update `billing/views.py` to use `xhtml2pdf` instead
   - Install: `pip install xhtml2pdf`

## Notes

- Python 3.13 is very new, and some packages may not have full support yet
- If you encounter compatibility issues, consider using Python 3.11 or 3.12
- Always use a virtual environment for Python projects to avoid conflicts

