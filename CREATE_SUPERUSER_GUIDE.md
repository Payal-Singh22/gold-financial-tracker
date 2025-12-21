# How to Create Superuser on Render (Without Paid Shell)

## Method 1: Using Django Management Command (Recommended)

### Step 1: Add Environment Variables on Render

1. Go to your **Web Service** dashboard on Render
2. Go to **"Environment"** tab
3. Click **"Add Environment Variable"**
4. Add these variables:

```
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@yourdomain.com
DJANGO_SUPERUSER_PASSWORD=your-secure-password-here
```

### Step 2: Run Command via Render Dashboard

**Option A: Using Render's "Run Command" Feature**

1. In your Web Service dashboard, look for **"Run Command"** or **"Shell"** tab
2. If available, run:
   ```bash
   python manage.py create_superuser
   ```

**Option B: Add to build.sh (One-time)**

Temporarily add this to your `build.sh` (remove after first run):

```bash
# Create superuser if doesn't exist (one-time setup)
if [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    python manage.py create_superuser --noinput || true
fi
```

Then:
1. Push to GitHub
2. Wait for deployment
3. Remove the superuser creation from `build.sh`
4. Push again

---

## Method 2: Using Standalone Script

### Step 1: Add Environment Variables

Same as Method 1 - add to Render environment variables.

### Step 2: Run Script

If Render has a "Run Command" feature, run:
```bash
python create_superuser.py
```

---

## Method 3: Using Django Admin via Browser

### Step 1: Create Superuser Locally

1. **Clone your repository locally** (if not already)
2. **Set up environment variables**:
   ```bash
   export DJANGO_SUPERUSER_USERNAME=admin
   export DJANGO_SUPERUSER_EMAIL=admin@example.com
   export DJANGO_SUPERUSER_PASSWORD=your-password
   ```

3. **Run locally**:
   ```bash
   python manage.py create_superuser
   ```

### Step 2: Push to Production Database

**Option A: If using same database**
- The superuser will be in the database
- Just login at: `https://your-app.onrender.com/admin`

**Option B: Export/Import**
```bash
# Export from local
python manage.py dumpdata auth.User --indent 2 > superuser.json

# Import to production (if you have database access)
python manage.py loaddata superuser.json
```

---

## Method 4: Using Django's createsuperuser with --noinput

### Step 1: Add to build.sh (One-time)

Add this to `build.sh` temporarily:

```bash
# Create superuser if environment variables are set
if [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    python manage.py createsuperuser \
        --username "${DJANGO_SUPERUSER_USERNAME:-admin}" \
        --email "${DJANGO_SUPERUSER_EMAIL:-admin@example.com}" \
        --noinput || true
    
    # Set password
    python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.get(username='${DJANGO_SUPERUSER_USERNAME:-admin}')
user.set_password('$DJANGO_SUPERUSER_PASSWORD')
user.save()
EOF
fi
```

**Important:** Remove this after first deployment!

---

## Method 5: Using Render's Manual Deploy Hook

If Render supports manual deploy hooks, you can create a one-time script that runs during deployment.

---

## Recommended Approach

**For first-time setup:**

1. **Add environment variables** to Render:
   ```
   DJANGO_SUPERUSER_USERNAME=admin
   DJANGO_SUPERUSER_EMAIL=admin@example.com
   DJANGO_SUPERUSER_PASSWORD=your-secure-password
   ```

2. **Temporarily modify `build.sh`** to include:
   ```bash
   # Create superuser (remove after first run)
   if [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
       python manage.py create_superuser --noinput || true
   fi
   ```

3. **Push and deploy**:
   ```bash
   git add build.sh
   git commit -m "Add superuser creation"
   git push origin main
   ```

4. **After successful deployment**, remove the superuser creation from `build.sh`:
   ```bash
   # Remove the superuser creation lines from build.sh
   git add build.sh
   git commit -m "Remove superuser creation (already created)"
   git push origin main
   ```

5. **Login** at: `https://your-app.onrender.com/admin`

---

## Security Notes

- ✅ **Never commit passwords** to Git
- ✅ **Use environment variables** for all sensitive data
- ✅ **Remove superuser creation** from build.sh after first run
- ✅ **Use strong passwords** (at least 12 characters)
- ✅ **Change default username** from 'admin' to something unique

---

## Troubleshooting

### User Already Exists
The script will skip creation if user exists. This is safe to run multiple times.

### Password Not Set
Make sure `DJANGO_SUPERUSER_PASSWORD` is set in Render environment variables.

### Command Not Found
Make sure you've pushed the `billing/management/commands/create_superuser.py` file to GitHub.

---

## Files Created

1. `billing/management/commands/create_superuser.py` - Django management command
2. `create_superuser.py` - Standalone script
3. `create_superuser.sh` - Shell wrapper
4. `CREATE_SUPERUSER_GUIDE.md` - This guide

