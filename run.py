"""
Application entry point.
Start the Smart Hospital Queue & Appointment Optimizer.
"""
import os
import sys


def main():
    """Initialize and run the application."""
    print("=" * 60)
    print("  🏥 Smart Hospital Queue & Appointment Optimizer")
    print("=" * 60)

    # Step 1: Train ML model if not exists
    from config import Config
    if not os.path.exists(Config.ML_MODEL_PATH):
        print("\n📊 ML model not found. Training now...")
        from app.ml.train_model import train_crowd_model
        train_crowd_model()
    else:
        print("\n✅ ML model loaded.")

    # Step 2: Create the Flask app
    from app import create_app
    app = create_app()

    # Step 3: Check if database needs seeding
    with app.app_context():
        from app.models.models import Department
        from app import db
        if Department.query.count() == 0:
            print("\n🌱 Empty database detected. Running seeder...")
            # Import and run seed
            from seed_data import seed
            seed()

    # Step 4: Run the server
    print("\n🚀 Starting server at http://127.0.0.1:5000")
    print("   Press Ctrl+C to stop.\n")
    app.run(debug=True, host="127.0.0.1", port=5000)


if __name__ == "__main__":
    main()
