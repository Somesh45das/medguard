# 🚀 Deploy to Vercel - Quick Guide

## Option 1: Automated (Windows)

```bash
deploy-serverless.bat
```

## Option 2: Automated (Mac/Linux)

```bash
bash deploy-serverless.sh
```

## Option 3: Manual (Any OS)

### Step 1: Switch to Serverless Requirements
```bash
# Backup current requirements
copy requirements.txt requirements-full.txt

# Use serverless version
copy requirements-serverless.txt requirements.txt
```

### Step 2: Commit and Push
```bash
git add .
git commit -m "Fix: Deploy serverless without ML"
git push
```

### Step 3: Restore Full Requirements (for local dev)
```bash
copy requirements-full.txt requirements.txt
```

---

## What Happens Next

1. ✅ GitHub receives your push
2. ✅ Vercel detects changes (if connected)
3. ✅ Vercel builds with lightweight requirements
4. ✅ Deployment completes in ~2 minutes
5. ✅ Your app is live!

---

## Check Deployment Status

**Vercel Dashboard**: https://vercel.com/dashboard

**Your App**: https://your-project-name.vercel.app

---

## Troubleshooting

### If Vercel is not connected to GitHub:

1. Go to https://vercel.com/dashboard
2. Click "Add New Project"
3. Import your GitHub repository
4. Vercel will auto-deploy

### If deployment still fails:

Check logs:
```bash
vercel logs
```

Or manually deploy:
```bash
npm install -g vercel
vercel login
vercel --prod
```

---

## About the Line Ending Warning

The warning you saw:
```
warning: in the working copy of 'deploy-serverless.sh', 
LF will be replaced by CRLF the next time Git touches it
```

**This is normal on Windows!** It just means Git is converting line endings.

**Fixed by**: `.gitattributes` file (already created)

**Impact**: None - deployment works fine

---

## What Works After Deployment

✅ Patient booking  
✅ Admin management  
✅ Queue operations  
✅ SMS notifications  
✅ Authentication  
✅ All core features  

⚠️ ML predictions use fallback (60-70% accuracy)

---

## For Full ML (87% Accuracy)

Deploy to Railway instead:

```bash
npm install -g @railway/cli
railway login
railway up
```

Or use Render.com (free tier available)

---

**Ready?** Run `deploy-serverless.bat` now! 🚀
