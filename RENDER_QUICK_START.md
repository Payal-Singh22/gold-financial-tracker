# Quick Start: Deploy to Render in 10 Minutes

## Prerequisites
- ✅ GitHub account
- ✅ Render account (sign up at https://render.com - free)

---

## Step-by-Step Instructions

### Step 1: Push Code to GitHub (5 minutes)

1. **Initialize Git** (if not done):
   ```bash
   git init
   git add .
   git commit -m "Ready for Render deployment"
   ```

2. **Create GitHub Repository**:
   - Go to https://github.com/new
   - Repository name: `jewellery-billing-software`
   - Click **"Create repository"**

3. **Push Code**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/jewellery-billing-software.git
   git branch -M main
   git push -u origin main
   ```

---

### Step 2: Create PostgreSQL Database on Render (2 minutes)

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"PostgreSQL"**
3. Fill in:
   - **Name**: `jewellery-billing-db`
   - **Database**: `jewellery_billing`
   - **Plan**: Free
4. Click **"Create Database"**
5. **Wait 1-2 minutes** for database to be ready
6. **Copy these values** (you'll need them):
   - Internal Database URL (looks like: `postgresql://user:pass@host:5432/dbname`)

---

### Step 3: Create Web Service on Render (3 minutes)

1. In Render Dashboard, click **"New +"** → **"Web Service"**

2. **Connect GitHub**:
   - Click **"Connect GitHub"** (if first time)
   - Authorize Render
   - Select repository: `jewellery-billing-software`

3. **Configure Service**:
   - **Name**: `jewellery-billing-app`
   - **Region**: Choose closest
   - **Branch**: `main`
   - **Root Directory**: (leave empty)
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `./start.sh`

4. **Add Environment Variables**:
   Click **"Add Environment Variable"** and add these:

   ```
   SECRET_KEY=generate-random-key-here
   DEBUG=False
   ALLOWED_HOSTS=your-app-name.onrender.com
   DB_NAME=jewellery_billing
   DB_USER=copy-from-database-dashboard
   DB_PASSWORD=copy-from-database-dashboard
   DB_HOST=copy-from-database-dashboard
   DB_PORT=5432
   ```

   **To generate SECRET_KEY**, run this locally:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

   **To get DB credentials**:
   - Go to your PostgreSQL dashboard
   - Copy values from "Internal Database URL"
   - Format: `postgresql://USER:PASSWORD@HOST:5432/DB_NAME`
   - Extract USER, PASSWORD, HOST, DB_NAME

5. **Link Database**:
   - Scroll to **"Advanced"** section
   - Under **"Add Database"**, select `jewellery-billing-db`
   - This auto-populates DB environment variables

6. **Plan**: Free (or Starter $7/month for always-on)

7. Click **"Create Web Service"**

---

### Step 4: Wait for Deployment (2-3 minutes)

- Render will:
  1. Clone your repository
  2. Install dependencies
  3. Run `build.sh` (collects static files, runs migrations)
  4. Start your app

- Watch the **"Logs"** tab for progress
- Look for: ✅ "Build successful" and ✅ "Your service is live"

---

### Step 5: Create Admin User

1. In Web Service dashboard, go to **"Shell"** tab
2. Run:
   ```bash
   python manage.py createsuperuser
   ```
3. Enter username, email, password
4. Done!

---

### Step 6: Access Your App

1. Your app URL: `https://your-app-name.onrender.com`
2. Login with superuser credentials
3. Start using the application!

---

## Troubleshooting

### Build Fails
- Check logs for errors
- Verify `build.sh` exists and has execute permissions
- Check `requirements.txt` is correct

### Static Files 404
- Check build logs for "collectstatic" output
- Verify WhiteNoise is in requirements.txt
- Check STATICFILES_STORAGE in settings.py

### Database Connection Error
- Verify all DB environment variables are set
- Check database is running (green status)
- Verify connection string format

### App Won't Start
- Check logs for error messages
- Verify SECRET_KEY is set
- Check DEBUG=False
- Verify ALLOWED_HOSTS includes your domain

---

## Environment Variables Reference

```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
DB_NAME=jewellery_billing
DB_USER=db_user_from_render
DB_PASSWORD=db_password_from_render
DB_HOST=dpg-xxxxx-a.oregon-postgres.render.com
DB_PORT=5432
```

---

## Next Steps

- ✅ Test all features
- ✅ Set up custom domain (optional)
- ✅ Configure email (optional)
- ✅ Enable backups (paid plans)

---

## Cost

**Free Tier:**
- Web Service: Free (spins down after 15 min inactivity)
- PostgreSQL: Free (90 days)
- Good for: Testing

**Starter Plan:**
- Web Service: $7/month (always on)
- PostgreSQL: $7/month
- Total: ~$14/month
- Good for: Production

---

## Support

- Render Docs: https://render.com/docs
- Render Community: https://community.render.com

