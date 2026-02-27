"""
Database migration script to add doctor_id column to users table.
Run this to update your existing database schema.
"""
from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        # Check if column already exists
        result = db.session.execute(text("PRAGMA table_info(users)"))
        columns = [row[1] for row in result]
        
        if 'doctor_id' in columns:
            print("✓ Column 'doctor_id' already exists in users table")
        else:
            print("Adding 'doctor_id' column to users table...")
            
            # Add the doctor_id column
            db.session.execute(text(
                "ALTER TABLE users ADD COLUMN doctor_id INTEGER"
            ))
            
            # Add foreign key constraint (SQLite doesn't enforce this, but we add it for documentation)
            # Note: SQLite doesn't support adding foreign keys to existing tables
            # The relationship is defined in the model
            
            db.session.commit()
            print("✓ Successfully added 'doctor_id' column to users table")
        
        # Verify the change
        result = db.session.execute(text("PRAGMA table_info(users)"))
        print("\n" + "="*60)
        print("USERS TABLE SCHEMA:")
        print("="*60)
        for row in result:
            print(f"  {row[1]:20} {row[2]:15} {'NOT NULL' if row[3] else 'NULL':10}")
        print("="*60)
        
        print("\n✓ Database migration completed successfully!")
        print("\nYou can now:")
        print("1. Run the application: python run.py")
        print("2. Create doctor user: python create_doctor_user.py")
        print("3. Login as doctor: doctor@hospital.com / doctor123")
        
    except Exception as e:
        print(f"✗ Error during migration: {e}")
        db.session.rollback()
        raise
