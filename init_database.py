"""
Database initialization script for production deployment.
Run this once after deploying with PostgreSQL.
"""
import os
import sys

def init_database():
    """Initialize database with tables and seed data."""
    print("🗄️  Initializing database...")
    
    # Import app
    from app import create_app, db
    from app.models import models, user
    
    app = create_app()
    
    with app.app_context():
        # Create all tables
        print("📋 Creating database tables...")
        db.create_all()
        print("✅ Tables created successfully!")
        
        # Check if database is empty
        from app.models.models import Department
        from app.models.user import User
        
        dept_count = Department.query.count()
        user_count = User.query.count()
        
        if dept_count == 0 and user_count == 0:
            print("\n🌱 Database is empty. Seeding with initial data...")
            from seed_data import seed
            seed()
            print("✅ Database seeded successfully!")
        else:
            print(f"\n📊 Database already has data:")
            print(f"   - Departments: {dept_count}")
            print(f"   - Users: {user_count}")
            print("   Skipping seed to avoid duplicates.")
        
        print("\n🎉 Database initialization complete!")
        print("\n📝 Default Admin Credentials:")
        print("   Email: admin@hospital.com")
        print("   Password: admin123")
        print("\n⚠️  IMPORTANT: Change the admin password after first login!")

if __name__ == "__main__":
    try:
        init_database()
    except Exception as e:
        print(f"\n❌ Error initializing database: {e}")
        print("\nTroubleshooting:")
        print("1. Check DATABASE_URL environment variable is set")
        print("2. Verify database connection string is correct")
        print("3. Ensure database server is accessible")
        sys.exit(1)
