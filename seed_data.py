"""
Database seeder – creates sample departments, doctors, patients, and appointments.
Run this after starting the app for the first time.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from datetime import date, time, datetime, timedelta
import random
from app import create_app, db
from app.models.models import Department, Doctor, Patient, Appointment, Notification
from app.models.user import User


def seed():
    """Populate the database with sample data."""
    app = create_app()
    with app.app_context():
        print("🌱 Seeding database...")

        # Clear existing data
        db.drop_all()
        db.create_all()

        # ---- Create Admin User ----
        admin = User(
            name="Admin User",
            email="admin@hospital.com",
            phone="+91-9999999999",
            role="admin",
            is_active=True,
            is_verified=True
        )
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.flush()
        print(f"   ✅ Admin user created (email: admin@hospital.com, password: admin123)")

        # ---- Departments ----
        departments_data = [
            ("General Medicine", 1, 60, 12),
            ("Pediatrics", 1, 40, 15),
            ("Orthopedics", 2, 35, 20),
            ("Cardiology", 2, 30, 18),
            ("Dermatology", 3, 25, 10),
            ("ENT", 3, 30, 12),
        ]
        departments = []
        for name, floor, cap, avg_time in departments_data:
            dept = Department(
                name=name, floor=floor, max_capacity=cap, avg_consultation_min=avg_time
            )
            db.session.add(dept)
            departments.append(dept)

        db.session.flush()
        print(f"   ✅ {len(departments)} departments created")

        # ---- Doctors ----
        doctors_data = [
            ("Aisha Sharma", "General Physician", 1, 12, 12, 40, time(8,0), time(16,0), 4.5),
            ("Rajesh Patel", "General Physician", 1, 8, 15, 35, time(9,0), time(17,0), 4.2),
            ("Priya Mehta", "Internal Medicine", 1, 15, 10, 45, time(8,0), time(14,0), 4.8),
            ("Vikram Singh", "Pediatrician", 2, 10, 15, 30, time(8,0), time(16,0), 4.6),
            ("Sunita Reddy", "Child Specialist", 2, 6, 18, 25, time(10,0), time(18,0), 4.3),
            ("Deepak Gupta", "Orthopedic Surgeon", 3, 20, 20, 25, time(9,0), time(17,0), 4.7),
            ("Neha Kapoor", "Orthopedist", 3, 7, 15, 30, time(8,0), time(15,0), 4.1),
            ("Amit Joshi", "Cardiologist", 4, 18, 20, 20, time(9,0), time(17,0), 4.9),
            ("Kavita Nair", "Heart Specialist", 4, 12, 18, 22, time(10,0), time(18,0), 4.4),
            ("Rahul Verma", "Dermatologist", 5, 9, 10, 35, time(8,0), time(16,0), 4.3),
            ("Meera Das", "Skin Specialist", 5, 5, 12, 30, time(9,0), time(17,0), 4.0),
            ("Suresh Kumar", "ENT Specialist", 6, 14, 12, 30, time(8,0), time(16,0), 4.5),
        ]
        doctors = []
        for name, spec, dept_id, exp, avg, max_p, s_start, s_end, rating in doctors_data:
            doc = Doctor(
                name=name,
                specialization=spec,
                department_id=dept_id,
                experience_years=exp,
                avg_consultation_min=avg,
                max_patients_per_day=max_p,
                shift_start=s_start,
                shift_end=s_end,
                rating=rating,
            )
            db.session.add(doc)
            doctors.append(doc)

        db.session.flush()
        print(f"   ✅ {len(doctors)} doctors created")

        # ---- Patients ----
        first_names = [
            "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh",
            "Ayaan", "Krishna", "Ishaan", "Ananya", "Diya", "Myra", "Sara",
            "Aadhya", "Ira", "Aanya", "Pari", "Riya", "Kiara", "Mohan",
            "Lakshmi", "Ganesh", "Saraswati", "Ram", "Sita", "Karthik",
            "Meena", "Suresh", "Kamala",
        ]
        patients = []
        for i, name in enumerate(first_names):
            p = Patient(
                patient_id=f"P-{date.today().strftime('%Y%m%d')}-{i+1:03d}",
                name=name,
                age=random.randint(2, 85),
                gender=random.choice(["Male", "Female"]),
                phone=f"+91-{random.randint(7000000000, 9999999999)}",
                is_emergency=random.random() < 0.1,
            )
            db.session.add(p)
            patients.append(p)

        db.session.flush()
        print(f"   ✅ {len(patients)} patients created")

        # ---- Create Test User with Patient Record ----
        test_patient = Patient(
            patient_id=f"P-{date.today().strftime('%Y%m%d')}-999",
            name="Test Patient",
            age=30,
            gender="Male",
            phone="+91-8888888888",
            email="test@patient.com",
            is_emergency=False
        )
        db.session.add(test_patient)
        db.session.flush()
        
        test_user = User(
            name="Test Patient",
            email="test@patient.com",
            phone="+91-8888888888",
            role="user",
            is_active=True,
            is_verified=True,
            patient_id=test_patient.id
        )
        test_user.set_password("test123")
        db.session.add(test_user)
        db.session.flush()
        print(f"   ✅ Test user created (email: test@patient.com, password: test123)")

        # ---- Today's Appointments ----
        today = date.today()
        statuses = ["scheduled", "scheduled", "scheduled", "checked_in", "completed"]
        appointments = []
        for i in range(20):
            patient = random.choice(patients)
            doctor = random.choice(doctors)
            hour = random.randint(8, 17)
            minute = random.choice([0, 15, 30, 45])
            appt_time = time(hour, minute)
            end_time = (datetime.combine(today, appt_time) + timedelta(minutes=15)).time()

            apt = Appointment(
                appointment_number=f"APT-{today.strftime('%Y%m%d')}-{i+1:03d}",
                patient_id=patient.id,
                doctor_id=doctor.id,
                department_id=doctor.department_id,
                appointment_date=today,
                appointment_time=appt_time,
                slot_end_time=end_time,
                status=random.choice(statuses),
                estimated_wait_min=random.randint(5, 45),
                symptoms=random.choice([
                    "Fever and cough", "Headache", "Back pain",
                    "Skin rash", "Ear pain", "Chest discomfort",
                    "General checkup", "Follow-up visit",
                    "Joint pain", "Breathing difficulty",
                ]),
            )
            db.session.add(apt)
            appointments.append(apt)

        db.session.flush()
        print(f"   ✅ {len(appointments)} appointments created")

        # ---- Notifications ----
        notifs = [
            ("🏥 System Started", "Smart Hospital Queue system is online.", "success"),
            ("📊 ML Model Ready", "Crowd prediction model loaded successfully.", "info"),
            ("⚠️ High Crowd Alert", "General Medicine department experiencing high crowd.", "warning"),
        ]
        for title, msg, ntype in notifs:
            db.session.add(Notification(title=title, message=msg, type=ntype))

        db.session.commit()
        print("\n   🎉 Database seeded successfully!")
        print(f"   📊 {len(departments)} departments, {len(doctors)} doctors,")
        print(f"      {len(patients)} patients, {len(appointments)} appointments")


if __name__ == "__main__":
    seed()
