# PostgreSQL Database Setup for Vercel

## ✅ Code Changes Complete

I've updated your code to support PostgreSQL:
- ✅ `config.py` - Now supports both PostgreSQL and SQLite
- ✅ `requirements.txt` - Added `psycopg2-binary`
- ✅ `requirements-vercel.txt` - Added PostgreSQL driver

## 🗄️ Option 1: Vercel Postgres (Recommended for Vercel Deployment)

### Step 1: Create Vercel Postgres Database

1. **Go to Vercel Dashboard**
   - Visit https://vercel.com/dashboard
   - Select your project `medguard`

2. **Navigate to Storage Tab**
   - Click on "Storage" in the top menu
   - Click "Create Database"

3. **Select Postgres**
   - Choose "Postgres"
   - Select region (choose closest to your users)
   - Click "Create"

4. **Get Connection String**
   - After creation, you'll see database details
   - Copy the `POSTGRES_URL` connection string
   - It looks like: `postgres://user:pass@host:5432/dbname`

### Step 2: Add Environment Variable

1. **In Vercel Project Settings**
   - Go to Settings → Environment Variables
   - Click "Add New"
   - Name: `POSTGRES_URL`
   - Value: (paste your connection string)
   - Select all environments (Production, Preview, Development)
   - Click "Save"

2. **Alternative Variable Names**
   - You can also use `DATABASE_URL`
   - The code supports both

### Step 3: Redeploy

1. **Trigger Redeploy**
   - Go to Deployments tab
   - Click on latest deployment
   - Click "Redeploy"
   - Or push a new commit to trigger deployment

2. **Database Tables Auto-Created**
   - The `wsgi.py` file automatically creates tables
   - No manual migration needed

### Step 4: Seed Initial Data

After deployment, you need to add the admin user and sample data.

**Option A: Use Vercel CLI**
```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Link project
vercel link

# Run seed script
vercel env pull .env.local
python seed_data.py
```

**Option B: Create Admin via API**
Create a temporary route to seed data (remove after use):

```python
# Add to api/index.py temporarily
@app.route('/seed-database-once')
def seed_once():
    from seed_data import seed
    seed()
    return "Database seeded!"
```

Visit: `https://your-app.vercel.app/seed-database-once`

---

## 🗄️ Option 2: Supabase (Free PostgreSQL)

Supabase offers free PostgreSQL with 500MB storage.

### Step 1: Create Supabase Project

1. **Sign Up**
   - Go to https://supabase.com
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Name: `medguard`
   - Database Password: (create strong password)
   - Region: (choose closest)
   - Click "Create Project"

3. **Get Connection String**
   - Go to Project Settings → Database
   - Find "Connection string" section
   - Copy the "URI" format
   - Replace `[YOUR-PASSWORD]` with your actual password

### Step 2: Add to Vercel

1. **In Vercel Dashboard**
   - Settings → Environment Variables
   - Add: `DATABASE_URL` = your Supabase connection string
   - Save and redeploy

---

## 🗄️ Option 3: Neon (Free Serverless Postgres)

Neon offers free serverless PostgreSQL.

### Step 1: Create Neon Database

1. **Sign Up**
   - Go to https://neon.tech
   - Sign up with GitHub

2. **Create Project**
   - Click "Create Project"
   - Name: `medguard`
   - Region: (choose closest)
   - Click "Create"

3. **Get Connection String**
   - Copy the connection string shown
   - Format: `postgresql://user:pass@host/dbname`

### Step 2: Add to Vercel

1. **Environment Variable**
   - In Vercel: Settings → Environment Variables
   - Add: `DATABASE_URL` = your Neon connection string
   - Redeploy

---

## 🗄️ Option 4: Railway Postgres (Free)

Railway offers free PostgreSQL with your app.

### Step 1: Deploy to Railway Instead

1. **Go to Railway**
   - Visit https://railway.app
   - Sign up with GitHub

2. **New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `medguard`

3. **Add PostgreSQL**
   - Click "New" → "Database" → "Add PostgreSQL"
   - Railway automatically connects it

4. **Done!**
   - Railway handles everything
   - Database URL automatically set
   - App deployed with working database

---

## 🧪 Testing Database Connection

After setting up database, test it:

### Method 1: Check Logs

1. **Vercel Dashboard**
   - Go to your deployment
   - Click "View Function Logs"
   - Look for database connection messages

### Method 2: Test Endpoint

Create a test route:

```python
# Add to api/index.py
@app.route('/test-db')
def test_db():
    from app.models.models import Department
    count = Department.query.count()
    return f"Database connected! Departments: {count}"
```

Visit: `https://your-app.vercel.app/test-db`

---

## 📊 Database Comparison

| Provider | Free Tier | Storage | Setup Time | Best For |
|----------|-----------|---------|------------|----------|
| Vercel Postgres | No (paid) | Varies | 2 min | Vercel apps |
| Supabase | Yes | 500MB | 3 min | Any app |
| Neon | Yes | 3GB | 3 min | Serverless |
| Railway | Yes | 1GB | 2 min | Full apps |

---

## 🚀 Recommended Setup Path

### For Vercel Deployment:

**Best Option: Supabase (Free)**
1. Create Supabase account
2. Create project and get connection string
3. Add to Vercel environment variables
4. Redeploy
5. Seed database

**Time Required:** 5-10 minutes

### For Easiest Setup:

**Best Option: Railway (Free)**
1. Deploy entire app to Railway
2. Add PostgreSQL database (one click)
3. Everything works automatically
4. No configuration needed

**Time Required:** 2 minutes

---

## 🔧 Troubleshooting

### Error: "relation does not exist"
**Solution:** Tables not created. Redeploy or run migrations.

### Error: "could not connect to server"
**Solution:** Check connection string format and credentials.

### Error: "SSL required"
**Solution:** Add `?sslmode=require` to connection string.

### Error: "password authentication failed"
**Solution:** Verify password in connection string.

---

## 📝 Next Steps After Database Setup

1. **Seed Database**
   - Run seed script to add admin user
   - Add sample departments and doctors

2. **Test Login**
   - Try logging in with: admin@hospital.com / admin123

3. **Test Features**
   - Patient registration
   - Appointment booking
   - Admin dashboard

4. **Change Admin Password**
   - Login as admin
   - Change default password immediately

---

## ✅ Summary

**What We Did:**
- ✅ Updated code to support PostgreSQL
- ✅ Added database driver (psycopg2-binary)
- ✅ Made config flexible (SQLite local, Postgres production)

**What You Need to Do:**
1. Choose database provider (Supabase recommended for free)
2. Create database
3. Add connection string to Vercel
4. Redeploy
5. Seed database

**Estimated Time:** 10 minutes total

**Result:** Fully functional app with persistent database! 🎉

---

## 🆘 Need Help?

If you get stuck:
1. Check Vercel deployment logs
2. Verify connection string format
3. Test database connection separately
4. Consider using Railway (easier setup)

**Quick Win:** Deploy to Railway instead - database included automatically!
