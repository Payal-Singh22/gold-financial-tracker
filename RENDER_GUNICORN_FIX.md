# Fix: "gunicorn: command not found" on Render

## Problem
```
./start.sh: line 9: gunicorn: command not found
```

## Root Cause
Gunicorn might not be in the system PATH even though it's installed via pip.

## Solution Applied

### 1. Updated `start.sh`
Now uses `python -m gunicorn` as fallback if `gunicorn` command is not found:

```bash
if command -v gunicorn &> /dev/null; then
    gunicorn jewellery_billing.wsgi:application --bind 0.0.0.0:$PORT
else
    python -m gunicorn jewellery_billing.wsgi:application --bind 0.0.0.0:$PORT
fi
```

### 2. Updated `build.sh`
Added verification to ensure gunicorn is installed:

```bash
python -c "import gunicorn" 2>/dev/null || pip install gunicorn==21.2.0
```

## Alternative Solution (Simpler)

If the above doesn't work, you can simplify `start.sh` to always use Python module syntax:

```bash
#!/usr/bin/env bash
set -o errexit
python manage.py migrate --noinput
python -m gunicorn jewellery_billing.wsgi:application --bind 0.0.0.0:$PORT
```

## Steps to Fix

1. **Commit the updated files:**
   ```bash
   git add build.sh start.sh
   git commit -m "Fix gunicorn command not found error"
   git push origin main
   ```

2. **Render will automatically redeploy** with the new scripts

3. **Check the logs** - you should see:
   - ✅ Migrations running
   - ✅ Gunicorn starting successfully
   - ✅ Server listening on port

## Verify

After redeploy, check:
- ✅ Build completes successfully
- ✅ No "gunicorn: command not found" error
- ✅ Application starts and is accessible

## If Still Failing

Try this minimal `start.sh`:

```bash
#!/usr/bin/env bash
python manage.py migrate --noinput
exec python -m gunicorn jewellery_billing.wsgi:application --bind 0.0.0.0:$PORT
```

The `exec` command replaces the shell process with gunicorn, which can help with signal handling.

