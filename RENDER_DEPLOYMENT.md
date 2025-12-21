# Complete Guide: Deploying Jewellery Billing Software on Render

## Prerequisites
- GitHub account (or GitLab/Bitbucket)
- Render account (sign up at https://render.com)
- Your project code pushed to a Git repository

---

## Step 1: Prepare Your Project for Deployment

### 1.1 Update Settings for Production

Edit `jewellery_billing/settings.py`:

```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-this-in-production-!@#$%^&*()')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# ... rest of settings ...

# Database - Use PostgreSQL on Render
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### 1.2 Create Build Script

Create `build.sh` in the root directory:

```bash
#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate --noinput
```

### 1.3 Create Start Script

Create `start.sh` in the root directory:

```bash
#!/usr/bin/env bash
# Exit on error
set -o errexit

# Run migrations (in case of any pending migrations)
python manage.py migrate --noinput

# Start Gunicorn
gunicorn jewellery_billing.wsgi:application --bind 0.0.0.0:$PORT
```

### 1.4 Update requirements.txt

Make sure `requirements.txt` includes Gunicorn:

```
Django==4.2.7
django-crispy-forms==2.1
crispy-bootstrap5==0.7
Pillow>=10.3.0
WeasyPrint>=60.1
django-environ==0.11.2
whitenoise==6.6.0
gunicorn==21.2.0
psycopg2-binary==2.9.9
```

### 1.5 Create .gitignore (if not exists)

Create `.gitignore`:

```
*.pyc
__pycache__/
*.log
db.sqlite3
db.sqlite3-journal
staticfiles/
media/
.env
venv/
env/
.venv
*.swp
*.swo
.DS_Store
```

---

## Step 2: Push Code to GitHub

### 2.1 Initialize Git Repository (if not already done)

```bash
git init
git add .
git commit -m "Initial commit - Ready for Render deployment"
```

### 2.2 Create GitHub Repository

1. Go to https://github.com/new
2. Create a new repository (e.g., `jewellery-billing-software`)
3. **DO NOT** initialize with README, .gitignore, or license

### 2.3 Push Code to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/jewellery-billing-software.git
git branch -M main
git push -u origin main
```

---

## Step 3: Create PostgreSQL Database on Render

### 3.1 Create Database

1. Log in to Render Dashboard: https://dashboard.render.com
2. Click **"New +"** → **"PostgreSQL"**
3. Configure:
   - **Name**: `jewellery-billing-db`
   - **Database**: `jewellery_billing`
   - **User**: (auto-generated)
   - **Region**: Choose closest to your users
   - **PostgreSQL Version**: 15 (or latest)
   - **Plan**: Free (or paid for production)
4. Click **"Create Database"**
5. **Wait for database to be ready** (takes 1-2 minutes)

### 3.2 Save Database Credentials

After creation, you'll see:
- **Internal Database URL**: `postgresql://user:password@host:5432/dbname`
- **External Database URL**: (for local connections)

**Save these credentials** - you'll need them in the next step.

---

## Step 4: Create Web Service on Render

### 4.1 Create New Web Service

1. In Render Dashboard, click **"New +"** → **"Web Service"**
2. Connect your GitHub repository:
   - Click **"Connect GitHub"** (if not connected)
   - Authorize Render to access your repositories
   - Select your repository: `jewellery-billing-software`

### 4.2 Configure Web Service

Fill in the details:

**Basic Settings:**
- **Name**: `jewellery-billing-app` (or your preferred name)
- **Region**: Same as database
- **Branch**: `main`
- **Root Directory**: (leave empty if root)
- **Runtime**: `Python 3`
- **Build Command**: `./build.sh`
- **Start Command**: `./start.sh`

**Environment Variables:**

Click **"Add Environment Variable"** and add:

```
SECRET_KEY=your-secret-key-here-generate-a-random-one
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
DB_NAME=jewellery_billing
DB_USER=your-db-user-from-step-3
DB_PASSWORD=your-db-password-from-step-3
DB_HOST=your-db-host-from-step-3
DB_PORT=5432
```

**To generate SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Plan:**
- **Free Plan**: (for testing)
- **Starter Plan**: $7/month (recommended for production)

### 4.3 Create Web Service

Click **"Create Web Service"**

---

## Step 5: Configure Static Files

### 5.1 WhiteNoise is Already Configured

The settings.py already has WhiteNoise configured, which will serve static files automatically.

### 5.2 Verify Build Script

Make sure `build.sh` includes:
```bash
python manage.py collectstatic --noinput
```

---

## Step 6: Create Superuser

### 6.1 Using Render Shell

1. In your Web Service dashboard, go to **"Shell"** tab
2. Run:
```bash
python manage.py createsuperuser
```
3. Follow prompts to create admin user

### 6.2 Alternative: Using Django Management Command

Create a one-time script `create_superuser.sh`:

```bash
#!/usr/bin/env bash
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'your-password-here')
    print('Superuser created')
else:
    print('Superuser already exists')
EOF
```

Then run it in Render Shell:
```bash
chmod +x create_superuser.sh
./create_superuser.sh
```

---

## Step 7: Verify Deployment

### 7.1 Check Build Logs

1. Go to your Web Service dashboard
2. Click **"Logs"** tab
3. Check for:
   - ✅ Build successful
   - ✅ Static files collected
   - ✅ Migrations applied
   - ✅ Server started

### 7.2 Test Your Application

1. Visit your app URL: `https://your-app-name.onrender.com`
2. Test:
   - ✅ Login page loads
   - ✅ Can login with superuser
   - ✅ Dashboard loads
   - ✅ Static files (CSS/JS) load correctly
   - ✅ Can create bills

### 7.3 Common Issues

**If static files don't load:**
- Check build logs for `collectstatic` output
- Verify `STATICFILES_STORAGE` is set in settings.py
- Check WhiteNoise middleware is in MIDDLEWARE list

**If database errors:**
- Verify environment variables are correct
- Check database is running
- Verify connection string format

**If 500 errors:**
- Check logs in Render dashboard
- Verify SECRET_KEY is set
- Check DEBUG=False and ALLOWED_HOSTS includes your domain

---

## Step 8: Configure Custom Domain (Optional)

### 8.1 Add Custom Domain

1. In Web Service dashboard, go to **"Settings"**
2. Scroll to **"Custom Domains"**
3. Click **"Add Custom Domain"**
4. Enter your domain: `kljewellers.novagreen.help`
5. Follow DNS configuration instructions

### 8.2 Update ALLOWED_HOSTS

Update environment variable:
```
ALLOWED_HOSTS=your-app-name.onrender.com,kljewellers.novagreen.help,www.kljewellers.novagreen.help
```

---

## Step 9: Set Up Email (Optional)

### 9.1 Configure SMTP

Add environment variables:
```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

Update `settings.py`:
```python
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.environ.get('EMAIL_HOST', '')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@example.com')
```

---

## Step 10: Monitor and Maintain

### 10.1 Monitor Logs

- Check Render dashboard logs regularly
- Set up log alerts if needed

### 10.2 Backup Database

1. Go to PostgreSQL dashboard
2. Click **"Backups"** tab
3. Enable automatic backups (paid plans)

### 10.3 Update Application

1. Push changes to GitHub
2. Render automatically deploys (if auto-deploy enabled)
3. Or manually deploy from dashboard

---

## Quick Reference: Environment Variables

```
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-app.onrender.com
DB_NAME=jewellery_billing
DB_USER=db_user
DB_PASSWORD=db_password
DB_HOST=dpg-xxxxx-a.oregon-postgres.render.com
DB_PORT=5432
```

---

## Troubleshooting

### Build Fails

**Error: "No such file or directory: build.sh"**
- Make sure `build.sh` is in root directory
- Check file has execute permissions: `chmod +x build.sh`
- Commit and push to GitHub

**Error: "Module not found"**
- Check `requirements.txt` includes all dependencies
- Verify Python version matches

### Static Files 404

- Check `collectstatic` ran successfully in build logs
- Verify `STATICFILES_STORAGE` is set
- Check WhiteNoise middleware is configured

### Database Connection Error

- Verify all DB environment variables are set correctly
- Check database is running
- Verify connection string format

### Application Crashes

- Check logs in Render dashboard
- Verify SECRET_KEY is set
- Check DEBUG=False
- Verify ALLOWED_HOSTS includes your domain

---

## Cost Estimate

**Free Tier:**
- Web Service: Free (spins down after 15 min inactivity)
- PostgreSQL: Free (limited to 90 days)
- Good for: Testing, development

**Starter Plan:**
- Web Service: $7/month (always on)
- PostgreSQL: $7/month
- Total: ~$14/month
- Good for: Small production use

---

## Next Steps After Deployment

1. ✅ Test all features
2. ✅ Create backup strategy
3. ✅ Set up monitoring
4. ✅ Configure custom domain
5. ✅ Set up email notifications
6. ✅ Enable SSL (automatic on Render)

---

## Support

- Render Docs: https://render.com/docs
- Render Community: https://community.render.com
- Django Deployment: https://docs.djangoproject.com/en/4.2/howto/deployment/

