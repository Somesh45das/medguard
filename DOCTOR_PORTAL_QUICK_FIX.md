# Doctor Portal - Quick Fix Guide

## Error: "no such column: users.doctor_id"

This error occurs because the database schema needs to be updated to include the new `doctor_id` column.

---

## Quick Fix (Run This)

```bash
python fix_database_for_doctor_portal.py
```

This script will:
1. ✅ Add `doctor_id` column to users table
2. ✅ Create a test doctor user account
3. ✅ Link the user to a doctor profile
4. ✅ Display all login credentials

---

## Manual Fix (If Script Fails)

### Option 1: Update Existing Database

```bash
python migrate_add_doctor_column.py
python create_doctor_user.py
```

### Option 2: Fresh Start (Recommended)

```bash
# 1. Stop the application (Ctrl+C)

# 2. Delete the old database
rm instance/hospital.db    # Linux/Mac
del instance\hospital.db   # Windows

# 3. Recreate database with sample data
python seed_data.py

# 4. Run the fix script
python fix_database_for_doctor_portal.py

# 5. Start the application
python run.py
```

---

## Verify It's Working

1. **Start the application:**
   ```bash
   python run.py
   ```

2. **Open browser:**
   ```
   http://localhost:5000/auth/login
   ```

3. **Login as doctor:**
   ```
   Email:    doctor@hospital.com
   Password: doctor123
   ```

4. **You should see:**
   - Doctor Dashboard with statistics
   - Navigation menu with doctor options
   - Today's appointments and queue

---

## What Changed?

### Database Schema
```sql
-- Added to users table:
ALTER TABLE users ADD COLUMN doctor_id INTEGER;
```

### User Model
```python
# Added doctor relationship
doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"))
doctor = db.relationship("Doctor", backref="user_account")

# Added helper method
def is_doctor(self):
    return self.role == "doctor"
```

---

## All Login Credentials

### Admin
- Email: `admin@hospital.com`
- Password: `admin123`
- Access: Full admin panel

### Patient
- Email: `test@patient.com`
- Password: `test123`
- Access: Patient portal

### Doctor
- Email: `doctor@hospital.com`
- Password: `doctor123`
- Access: Doctor portal

---

## Troubleshooting

### Error: "No doctors found in database"
**Solution:** Run `python seed_data.py` first

### Error: "Table users has no column named doctor_id"
**Solution:** Run `python fix_database_for_doctor_portal.py`

### Error: "Doctor user already exists"
**Solution:** This is fine, the script will update the existing user

### Error: "Cannot access doctor portal"
**Solution:** Make sure you're logged in with doctor@hospital.com

### Error: "No doctor profile linked"
**Solution:** Run `python fix_database_for_doctor_portal.py` again

---

## Files Created

### Migration Scripts
- `migrate_add_doctor_column.py` - Adds doctor_id column
- `create_doctor_user.py` - Creates doctor user account
- `fix_database_for_doctor_portal.py` - Complete fix (recommended)

### Doctor Portal Files
- `app/routes/doctor_portal.py` - All doctor routes
- `app/templates/doctor/*.html` - All doctor templates
- `app/models/user.py` - Updated with doctor support
- `app/services/auth_service.py` - Added @doctor_required

---

## Quick Test Checklist

After running the fix script:

- [ ] Application starts without errors
- [ ] Can login as doctor
- [ ] Redirected to doctor dashboard
- [ ] Can see today's appointments
- [ ] Can view queue
- [ ] Can view appointment details
- [ ] Can update appointment status
- [ ] Navigation menu shows doctor options

---

## Need Help?

If you're still having issues:

1. **Check the error message** - It will tell you what's wrong
2. **Try fresh start** - Delete database and recreate
3. **Verify seed data** - Make sure doctors exist in database
4. **Check user role** - User must have role="doctor"
5. **Check doctor link** - User must have doctor_id set

---

## Summary

The database schema was updated to support doctor users. Run the fix script, restart the application, and login with the doctor credentials. Everything should work perfectly!
