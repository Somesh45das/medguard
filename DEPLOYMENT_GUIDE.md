# Complete Deployment Guide

## 🚀 Quick Deploy Options

### Option 1: Railway (RECOMMENDED - Easiest)

Railway is perfect for this Flask app with SQLite and ML models.

**Steps:**
1. Visit https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway auto-detects Python and deploys!
6. Set environment variable: `SECRET_KEY=your-secret-key-here`
7. Done! Your app is live.

**Why Railway?**
- ✅ Supports SQLite (persistent storage)
- ✅ Supports ML model files
- ✅ Free tier available
- ✅ Automatic HTTPS
- ✅ Easy database management

---

### Option 2: Render

**Steps:**
1. Visit https://render.com
2. Sign up and connect GitHub
3. Click "New" → "Web Service"
4. Select your repository
5. Configure:
   - **Name**: smart-hospital
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn wsgi:app`
6. Add environment variables:
   - `SECRET_KEY`: your-secret-key-here
   - `SESSION_COOKIE_SECURE`: True
7. Click "Create Web Service"

**Free Tier:**
- ✅ 750 hours/month free
- ✅ Automatic SSL
- ✅ Persistent disk (paid)

---

### Option 3: Heroku

**Prerequisites:**
```bash
# Install Heroku CLI
# Windows: Download from https://devcenter.heroku.com/articles/heroku-cli
# Mac: brew install heroku/brew/heroku
# Linux: curl https://cli-assets.heroku.com/install.sh | sh
```

**Steps:**
```bash
# Login to Heroku
heroku login

# Create app
heroku create smart-hospital-queue

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key-here
heroku config:set SESSION_COOKIE_SECURE=True

# Deploy
git push heroku main

# Open app
heroku open
```

**Note:** Heroku no longer has a free tier, but offers $5/month hobby plan.

---

### Option 4: PythonAnywhere

**Steps:**
1. Visit https://www.pythonanywhere.com
2. Sign up for free account
3. Go to "Web" tab
4. Click "Add a new web app"
5. Choose "Manual configuration" → Python 3.10
6. Upload your code via Files tab or Git
7. Configure WSGI file:
   ```python
   import sys
   path = '/home/yourusername/smart-hospital'
   if path not in sys.path:
       sys.path.append(path)
   
   from wsgi import app as application
   ```
8. Install requirements in Bash console:
   ```bash
   pip install -r requirements.txt
   ```
9. Reload web app

**Free Tier:**
- ✅ Always free
- ✅ Custom domain (paid)
- ⚠️ Limited CPU time

---

## ⚠️ Vercel Deployment (NOT RECOMMENDED)

Vercel is designed for serverless functions and doesn't work well with:
- SQLite databases (no persistent storage)
- ML model files
- Background jobs
- Session management

**If you must use Vercel:**
1. Migrate to PostgreSQL
2. Store ML models in cloud storage
3. Remove background jobs
4. See `VERCEL_DEPLOYMENT.md` for details

---

## 🐳 Docker Deployment

For advanced users who want full control:

**Create Dockerfile:**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create instance directory
RUN mkdir -p instance

# Expose port
EXPOSE 8000

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "wsgi:app"]
```

**Build and run:**
```bash
# Build image
docker build -t smart-hospital .

# Run container
docker run -p 8000:8000 -v $(pwd)/instance:/app/instance smart-hospital
```

**Deploy to:**
- Google Cloud Run
- AWS ECS/Fargate
- Azure Container Apps
- DigitalOcean App Platform

---

## 📋 Pre-Deployment Checklist

Before deploying, ensure:

- [ ] Change `SECRET_KEY` in config.py to a strong random value
- [ ] Set `SESSION_COOKIE_SECURE = True` for HTTPS
- [ ] Update `WTF_CSRF_ENABLED = True` (currently disabled for testing)
- [ ] Change default admin password
- [ ] Remove debug mode (`debug=False`)
- [ ] Set up proper logging
- [ ] Configure email service for password reset
- [ ] Test all features locally
- [ ] Backup database

---

## 🔧 Environment Variables

Set these in your deployment platform:

```bash
SECRET_KEY=your-very-secret-random-key-here
SESSION_COOKIE_SECURE=True
WTF_CSRF_ENABLED=True
FLASK_ENV=production
```

**Generate a secure SECRET_KEY:**
```python
import secrets
print(secrets.token_hex(32))
```

---

## 📊 Database Considerations

### SQLite (Current)
- ✅ Works on: Railway, Render (with persistent disk), Heroku, PythonAnywhere
- ❌ Doesn't work on: Vercel, AWS Lambda, Google Cloud Functions

### PostgreSQL (For Scale)
If you need to scale, migrate to PostgreSQL:

```python
# config.py
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
    f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'hospital.db')}"
```

Add to requirements.txt:
```
psycopg2-binary==2.9.9
```

---

## 🎯 Recommended Deployment Path

**For Quick Testing:**
1. Deploy to Railway (5 minutes)
2. Test all features
3. Share link with team

**For Production:**
1. Deploy to Render or Railway
2. Set up custom domain
3. Configure email service
4. Set up monitoring
5. Regular backups

---

## 📁 Files Created for Deployment

- ✅ `wsgi.py` - Production WSGI entry point
- ✅ `Procfile` - Heroku configuration
- ✅ `railway.json` - Railway configuration
- ✅ `vercel.json` - Vercel configuration (not recommended)
- ✅ `requirements.txt` - Updated with gunicorn

---

## 🚨 Common Issues

### Issue: "Application Error" on Heroku
**Solution:** Check logs with `heroku logs --tail`

### Issue: Database not persisting on Vercel
**Solution:** Vercel doesn't support SQLite. Use Railway instead.

### Issue: ML model not loading
**Solution:** Ensure model files are in repository and path is correct.

### Issue: CSRF token errors
**Solution:** Set `WTF_CSRF_ENABLED=True` and `SESSION_COOKIE_SECURE=True`

---

## 📞 Support

**Deployment Issues:**
- Railway: https://railway.app/help
- Render: https://render.com/docs
- Heroku: https://devcenter.heroku.com

**Application Issues:**
- Check logs in deployment platform
- Review `AUTHENTICATION_GUIDE.md`
- Check `TESTING_CHECKLIST.md`

---

## ✅ Post-Deployment

After successful deployment:

1. **Test Login:**
   - Admin: admin@hospital.com / admin123
   - Change admin password immediately!

2. **Test Features:**
   - Patient registration
   - Appointment booking
   - Admin dashboard
   - Doctor management

3. **Monitor:**
   - Check application logs
   - Monitor error rates
   - Track performance

4. **Secure:**
   - Change default passwords
   - Enable CSRF protection
   - Set up HTTPS
   - Configure firewall

---

## 🎉 Success!

Your Smart Hospital Queue & Appointment Optimizer is now live!

**Next Steps:**
- Share URL with team
- Train staff on admin portal
- Promote patient portal to patients
- Monitor usage and feedback

---

**Deployment Status:** Ready for Railway, Render, Heroku, or PythonAnywhere
**Recommended:** Railway (easiest and free)
