#!/bin/bash
# Deploy to Vercel without ML dependencies

echo "🚀 Deploying Smart Hospital to Vercel (Serverless Mode)"
echo "========================================================"

# Backup original requirements
echo "📦 Backing up requirements.txt..."
cp requirements.txt requirements-full.txt

# Use serverless requirements
echo "📦 Using serverless requirements..."
cp requirements-serverless.txt requirements.txt

# Commit changes
echo "📝 Committing changes..."
git add .
git commit -m "Deploy: Serverless mode without ML dependencies"

# Push to trigger Vercel deployment
echo "🚀 Pushing to GitHub (triggers Vercel auto-deploy)..."
git push

# Restore original requirements for local development
echo "📦 Restoring full requirements for local dev..."
cp requirements-full.txt requirements.txt

echo ""
echo "✅ Deployment initiated!"
echo ""
echo "Next steps:"
echo "1. Check Vercel dashboard: https://vercel.com/dashboard"
echo "2. Monitor deployment logs"
echo "3. Test your app at: https://your-app.vercel.app"
echo ""
echo "Note: ML features will use fallback mode (rule-based predictions)"
echo "For full ML: Deploy to Railway.app or Render.com instead"
echo ""
