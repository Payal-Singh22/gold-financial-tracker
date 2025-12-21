# Quick Guide: Create Superuser on Render (No Paid Shell Needed)

## ✅ Easiest Method: Automatic Creation During Deployment

### Step 1: Add Environment Variables on Render

1. Go to your **Web Service** dashboard: https://dashboard.render.com
2. Click on your web service
3. Go to **"Environment"** tab
4. Click **"Add Environment Variable"**
5. Add these **3 variables**:

```
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@yourdomain.com
DJANGO_SUPERUSER_PASSWORD=your-secure-password-here
```

**Important:** Use a strong password (at least 12 characters)!

### Step 2: Push Updated Code

The `build.sh` file has been updated to automatically create the superuser during deployment.

1. **Commit and push:**
   ```bash
   git add .
   git commit -m "Add automatic superuser creation"
   git push origin main
   ```

2. **Render will automatically deploy** and create the superuser

3. **Check build logs** - you should see:
   ```
   Creating superuser...
   Successfully created superuser: admin
   ```

### Step 3: Login

1. Go to: `https://your-app-name.onrender.com/admin`
2. Login with:
   - **Username:** `admin` (or whatever you set)
   - **Password:** The password you set in environment variables

### Step 4: Remove Auto-Creation (Optional)

After successful creation, you can remove the superuser creation from `build.sh`:

1. Edit `build.sh` and remove these lines:
   ```bash
   # Create superuser if environment variables are set (one-time setup)
   if [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
       echo "Creating superuser..."
       python manage.py create_superuser --noinput || echo "Superuser creation skipped (may already exist)"
   fi
   ```

2. Push again:
   ```bash
   git add build.sh
   git commit -m "Remove superuser auto-creation"
   git push origin main
   ```

**Note:** It's safe to leave it - it will skip if user already exists.

---

## Alternative: Manual Command (If Render Supports It)

If Render has a "Run Command" or "One-off Command" feature:

1. Set environment variables (same as above)
2. Run:
   ```bash
   python manage.py create_superuser --noinput
   ```

---

## Files Created

- ✅ `billing/management/commands/create_superuser.py` - Django management command
- ✅ `build.sh` - Updated to auto-create superuser
- ✅ `create_superuser.py` - Standalone script (alternative)
- ✅ `CREATE_SUPERUSER_GUIDE.md` - Detailed guide

---

## Security Checklist

- ✅ Password is stored in environment variables (not in code)
- ✅ Password is never committed to Git
- ✅ Command is idempotent (safe to run multiple times)
- ✅ Skips creation if user already exists

---

## Troubleshooting

### Superuser Already Exists
- This is normal - the command will skip creation
- You can login with existing credentials

### Password Not Working
- Check environment variables are set correctly
- Make sure you're using the correct username

### Command Not Found
- Make sure you've pushed `billing/management/commands/create_superuser.py` to GitHub
- Check build logs for errors

---

## Summary

**Just add 3 environment variables on Render and push your code - the superuser will be created automatically!** 🎉

