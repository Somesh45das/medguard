# Vercel Deployment Guide

## Important Notes

⚠️ **This Flask application has limitations on Vercel:**

1. **SQLite Database**: Vercel's serverless functions are stateless. SQLite won't persist data between requests.
2. **File Storage**: ML model files (`.pkl`) may not work properly in serverless environment.
3. **Background Jobs**: APScheduler and background tasks won't work on Vercel.

## Recommended Deployment Options

### Option 1: Railway (RECOMMENDED)
Railway supports Flask apps with persistent storage:

1. Visit https://railway.app
2. Connect your GitHub repository
3. Railway will auto-detect Flask
4. Set environment variables:
   ```
   SECRET_KEY=your-secret-key-here
   ```
5. Deploy!

### Option 2: Render
1. Visit https://render.com
2. Create new Web Service
3. Connect GitHub repo
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `gunicorn wsgi:app`
6. Add environment variables
7. Deploy!

### Option 3: Heroku
1. Install Heroku CLI
2. Create `Procfile`:
   ```
   web: gunicorn wsgi:app
   ```
3. Deploy:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### Option 4: PythonAnywhere
1. Upload code to PythonAnywhere
2. Configure WSGI file
3. Set up virtual environment
4. Reload web app

## If You Must Use Vercel

### Prerequisites
1. This app needs modifications for Vercel
2. Replace SQLite with PostgreSQL/MySQL
3. Store ML models in cloud storage (S3, etc.)
4. Remove background jobs

### Files Created for Vercel
- `wsgi.py` - WSGI entry point
- `vercel.json` - Vercel configuration

### Required Changes for Vercel

#### 1. Database
Replace SQLite with PostgreSQL:

```python
# config.py
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
```

Add to requirements.txt:
```
psycopg2-binary==2.9.9
```

#### 2. ML Models
Store models in cloud storage:
- Upload `.pkl` files to S3/Google Cloud Storage
- Load models from cloud at runtime
- Or retrain on first request

#### 3. Remove Background Jobs
Comment out APScheduler in requirements.txt:
```
# APScheduler==3.10.4
```

#### 4. Environment Variables
Set in Vercel dashboard:
- `SECRET_KEY`
- `DATABASE_URL` (PostgreSQL connection string)
- `SESSION_COOKIE_SECURE=True`

### Deployment Steps for Vercel

1. **Prepare Repository**
   ```bash
   git add vercel.json wsgi.py
   git commit -m "Add Vercel configuration"
   git push origin main
   ```

2. **Connect to Vercel**
   - Go to https://vercel.com
   - Import your GitHub repository
   - Vercel will detect Python

3. **Configure**
   - Framework Preset: Other
   - Build Command: (leave empty)
   - Output Directory: (leave empty)
   - Install Command: `pip install -r requirements.txt`

4. **Add Environment Variables**
   - Go to Project Settings → Environment Variables
   - Add all required variables

5. **Deploy**
   - Click Deploy
   - Wait for build to complete

## Current Limitations on Vercel

❌ SQLite database (data won't persist)
❌ ML model files (may not load)
❌ Background jobs (APScheduler)
❌ File uploads (no persistent storage)
❌ Session management (may have issues)

## What Will Work on Vercel

✅ Basic routing
✅ Template rendering
✅ Form handling
✅ API endpoints
✅ Authentication (with external DB)

## Recommended: Use Railway Instead

Railway is better suited for this application:

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize
railway init

# Deploy
railway up
```

Railway provides:
- Persistent storage
- PostgreSQL database
- Better Python support
- Background jobs support
- File storage

## Alternative: Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wsgi:app"]
```

Deploy to:
- Google Cloud Run
- AWS ECS
- Azure Container Apps
- DigitalOcean App Platform

## Summary

**For this Flask app with SQLite and ML models:**
1. ✅ Railway (Best option)
2. ✅ Render
3. ✅ Heroku
4. ✅ PythonAnywhere
5. ⚠️ Vercel (Requires major modifications)

**Current Status:**
- `wsgi.py` created ✅
- `vercel.json` created ✅
- But app needs database migration for Vercel ⚠️

**Recommendation:** Deploy to Railway or Render for best results without code changes.
