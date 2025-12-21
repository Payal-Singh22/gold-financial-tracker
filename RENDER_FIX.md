# Fix for "gunicorn: command not found" Error on Render

## Problem
```
./start.sh: line 9: gunicorn: command not found
```

## Solution

The issue is that `gunicorn` might not be in the PATH or installed correctly. I've updated the scripts to handle this.

### Updated Files

1. **build.sh** - Now verifies gunicorn is installed and reinstalls if needed
2. **start.sh** - Now uses `python -m gunicorn` as fallback if `gunicorn` command not found

### Alternative: Use Python Module Syntax

If the issue persists, you can also update `start.sh` to always use:

```bash
python -m gunicorn jewellery_billing.wsgi:application --bind 0.0.0.0:$PORT
```

### Steps to Fix

1. **Commit the updated files:**
   ```bash
   git add build.sh start.sh
   git commit -m "Fix gunicorn path issue for Render"
   git push origin main
   ```

2. **Render will automatically redeploy** with the new scripts

3. **If still failing**, try this alternative `start.sh`:

```bash
#!/usr/bin/env bash
set -o errexit
python manage.py migrate --noinput
python -m gunicorn jewellery_billing.wsgi:application --bind 0.0.0.0:$PORT
```

### Verify Requirements.txt

Make sure `requirements.txt` includes:
```
gunicorn==21.2.0
```

### Check Build Logs

After redeploy, check build logs for:
- ✅ "Successfully installed gunicorn"
- ✅ No errors during pip install

