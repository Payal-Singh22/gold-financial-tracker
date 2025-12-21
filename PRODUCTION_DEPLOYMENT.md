# Production Deployment Guide - Static Files Fix

## Issue
Static files (CSS, JS) are returning 404 errors and MIME type errors in production deployment.

## Root Cause
Django doesn't serve static files automatically in production. The static files need to be:
1. Collected into a single directory
2. Served by WhiteNoise middleware or web server

## Solution

### Option 1: Using WhiteNoise (Recommended - Already Configured)

#### Step 1: Install WhiteNoise
```bash
pip install whitenoise==6.6.0
```

#### Step 2: Verify Settings
Check that `jewellery_billing/settings.py` has:
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Must be after SecurityMiddleware
    # ... other middleware
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

#### Step 3: Collect Static Files
On your production server, run:
```bash
python manage.py collectstatic --noinput
```

This collects all static files from:
- `static/` directory (your custom CSS/JS)
- Django admin static files
- Crispy Forms static files
- Bootstrap static files

Into: `staticfiles/` directory

#### Step 4: Update ALLOWED_HOSTS
In `settings.py`, update:
```python
ALLOWED_HOSTS = ['kljewellers.novagreen.help', 'www.kljewellers.novagreen.help']
```

#### Step 5: Set DEBUG = False
```python
DEBUG = False
```

#### Step 6: Restart Server
Restart your Django application server (Gunicorn, uWSGI, etc.)

### Option 2: Using Web Server (Nginx/Apache)

If you prefer to serve static files via web server:

#### Nginx Configuration
```nginx
server {
    listen 80;
    server_name kljewellers.novagreen.help;
    
    # Django application
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Static files
    location /static/ {
        alias /path/to/your/project/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Media files
    location /media/ {
        alias /path/to/your/project/media/;
    }
}
```

#### Apache Configuration
```apache
<VirtualHost *:80>
    ServerName kljewellers.novagreen.help
    
    # Django application
    WSGIScriptAlias / /path/to/your/project/jewellery_billing/wsgi.py
    WSGIDaemonProcess jewellery_billing python-path=/path/to/your/project python-home=/path/to/venv
    WSGIProcessGroup jewellery_billing
    
    <Directory /path/to/your/project/jewellery_billing>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>
    
    # Static files
    Alias /static /path/to/your/project/staticfiles
    <Directory /path/to/your/project/staticfiles>
        Require all granted
    </Directory>
    
    # Media files
    Alias /media /path/to/your/project/media
    <Directory /path/to/your/project/media>
        Require all granted
    </Directory>
</VirtualHost>
```

## Quick Fix Commands

### On Production Server:
```bash
# 1. Install WhiteNoise
pip install whitenoise==6.6.0

# 2. Collect static files
python manage.py collectstatic --noinput

# 3. Restart your server
# For Gunicorn:
pkill -HUP gunicorn
# Or restart your systemd service
sudo systemctl restart your-django-service
```

## Verification Checklist

After deployment, verify:

1. ✅ Static CSS loads: `https://kljewellers.novagreen.help/static/css/style.css`
2. ✅ Static JS loads: `https://kljewellers.novagreen.help/static/js/main.js`
3. ✅ No 404 errors in browser console
4. ✅ No MIME type errors
5. ✅ JavaScript functions work (e.g., `addItem` function)
6. ✅ Page styling appears correctly

## Troubleshooting

### If static files still return 404:

1. **Check STATIC_ROOT exists:**
   ```bash
   ls -la staticfiles/
   ```

2. **Verify WhiteNoise middleware order:**
   Must be after `SecurityMiddleware` but before other middleware

3. **Check file permissions:**
   ```bash
   chmod -R 755 staticfiles/
   ```

4. **Verify STATIC_URL:**
   Should be `/static/` (with trailing slash)

5. **Check web server configuration:**
   If using Nginx/Apache, ensure static files location is correct

### If MIME type errors persist:

1. Ensure WhiteNoise is installed and configured
2. Clear browser cache
3. Check web server MIME type configuration

## Files Modified

- ✅ `requirements.txt` - Added whitenoise
- ✅ `jewellery_billing/settings.py` - Added WhiteNoise middleware and storage
- ✅ Created deployment scripts

## Next Steps

1. Run `pip install -r requirements.txt` on production server
2. Run `python manage.py collectstatic --noinput`
3. Restart Django server
4. Test the application

