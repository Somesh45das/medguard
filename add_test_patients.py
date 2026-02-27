"""
Add 20-30 test patients with different diseases and appointments.
This will populate the system with realistic test data.
"""
import sys
import random
from datetime import date, datetime, timedelta, time
sys.path.insert(0, '.')

from app import create_app, db
from app.models.models import Patient, Doctor, Department, Appointment
from app.models.user import User
from werkzeug.security import generate_password_hash

app = create_app()

# Patient data with realistic names and diseases
PATIENT_DATA = [
    {"name": "Rajesh Kumar", "age": 45, "gender": "male", "phone": "9876543201", "disease": "Chest pain, shortness of breath"},
    {"name": "Priya Sharma", "age": 32, "gender": "female", "phone": "9876543202", "disease": "Severe headache, dizziness"},
    {"name": "Amit Patel", "age": 58, "gender": "male", "phone": "9876543203", "disease": "Diabetes checkup, high blood sugar"},
    {"name": "Sneha Reddy", "age": 28, "gender": "female", "phone": "9876543204", "disease": "Pregnancy checkup, 7 months"},
    {"name": "Vikram Singh", "age": 41, "gender": "male", "phone": "9876543205", "disease": "Back pain, difficulty walking"},
    {"name": "Anita Desai", "age": 65, "gender": "female", "phone": "9876543206", "disease": "Hypertension, regular checkup"},
    {"name": "Rahul Verma", "age": 8, "gender": "male", "phone": "9876543207", "disease": "Fever, cough, cold"},
    {"name": "Meera Iyer", "age": 52, "gender": "female", "phone": "9876543208", "disease": "Joint pain, arthritis"},
    {"name": "Suresh Nair", "age": 70, "gender": "male", "phone": "9876543209", "disease": "Heart palpitations, fatigue"},
    {"name": "Kavita Joshi", "age": 35, "gender": "female", "phone": "9876543210", "disease": "Skin rash, allergic reaction"},
    {"name": "Arjun Mehta", "age": 22, "gender": "male", "phone": "9876543211", "disease": "Sports injury, knee pain"},
    {"name": "Deepa Rao", "age": 48, "gender": "female", "phone": "9876543212", "disease": "Thyroid disorder, weight gain"},
    {"name": "Karan Malhotra", "age": 55, "gender": "male", "phone": "9876543213", "disease": "Chest infection, breathing issues"},
    {"name": "Pooja Gupta", "age": 29, "gender": "female", "phone": "9876543214", "disease": "Migraine, vision problems"},
    {"name": "Sanjay Kapoor", "age": 62, "gender": "male", "phone": "9876543215", "disease": "Prostate checkup, urinary issues"},
    {"name": "Lakshmi Pillai", "age": 5, "gender": "female", "phone": "9876543216", "disease": "Vaccination, routine checkup"},
    {"name": "Manoj Tiwari", "age": 38, "gender": "male", "phone": "9876543217", "disease": "Stomach pain, indigestion"},
    {"name": "Nisha Agarwal", "age": 44, "gender": "female", "phone": "9876543218", "disease": "Anxiety, stress management"},
    {"name": "Ravi Krishnan", "age": 51, "gender": "male", "phone": "9876543219", "disease": "Liver function test, jaundice"},
    {"name": "Sunita Bose", "age": 67, "gender": "female", "phone": "9876543220", "disease": "Osteoporosis, bone density"},
    {"name": "Anil Chopra", "age": 33, "gender": "male", "phone": "9876543221", "disease": "Ear infection, hearing loss"},
    {"name": "Geeta Saxena", "age": 40, "gender": "female", "phone": "9876543222", "disease": "Dental pain, cavity"},
    {"name": "Harish Yadav", "age": 12, "gender": "male", "phone": "9876543223", "disease": "Asthma, breathing difficulty"},
    {"name": "Indira Menon", "age": 56, "gender": "female", "phone": "9876543224", "disease": "Eye checkup, blurred vision"},
    {"name": "Jai Prakash", "age": 47, "gender": "male", "phone": "9876543225", "disease": "Kidney stones, abdominal pain"},
    {"name": "Kamala Devi", "age": 72, "gender": "female", "phone": "9876543226", "disease": "Memory loss, confusion"},
    {"name": "Lalit Kumar", "age": 25, "gender": "male", "phone": "9876543227", "disease": "Acne treatment, skin care"},
    {"name": "Madhuri Patil", "age": 36, "gender": "female", "phone": "9876543228", "disease": "Anemia, fatigue"},
    {"name": "Naveen Reddy", "age": 60, "gender": "male", "phone": "9876543229", "disease": "Stroke recovery, physiotherapy"},
    {"name": "Omkar Shah", "age": 15, "gender": "male", "phone": "9876543230", "disease": "Growth checkup, nutrition"},
]

# Department to disease mapping
DISEASE_TO_DEPT = {
    "chest pain": "Cardiology",
    "heart": "Cardiology",
    "headache": "Neurology",
    "dizziness": "Neurology",
    "memory": "Neurology",
    "stroke": "Neurology",
    "diabetes": "General Medicine",
    "hypertension": "General Medicine",
    "fever": "General Medicine",
    "stomach": "General Medicine",
    "liver": "General Medicine",
    "pregnancy": "Gynecology",
    "back pain": "Orthopedics",
    "joint pain": "Orthopedics",
    "knee pain": "Orthopedics",
    "bone": "Orthopedics",
    "sports injury": "Orthopedics",
    "skin": "Dermatology",
    "acne": "Dermatology",
    "vaccination": "Pediatrics",
    "asthma": "Pediatrics",
    "growth": "Pediatrics",
    "ear": "ENT",
    "dental": "Dentistry",
    "eye": "Ophthalmology",
    "kidney": "General Medicine",
    "anxiety": "General Medicine",
    "anemia": "General Medicine",
}

def get_department_for_disease(disease):
    """Match disease to appropriate department."""
    disease_lower = disease.lower()
    for keyword, dept_name in DISEASE_TO_DEPT.items():
        if keyword in disease_lower:
            return dept_name
    return "General Medicine"  # Default

def create_test_patients():
    """Create test patients with appointments."""
    with app.app_context():
        print("=" * 70)
        print("   CREATING TEST PATIENTS WITH APPOINTMENTS")
        print("=" * 70)
        
        # Get all departments and doctors
        departments = {d.name: d for d in Department.query.all()}
        doctors_by_dept = {}
        for dept_name, dept in departments.items():
            doctors_by_dept[dept_name] = Doctor.query.filter_by(
                department_id=dept.id,
                is_available=True
            ).all()
        
        if not departments:
            print("❌ No departments found. Run seed_data.py first!")
            return
        
        print(f"\n✅ Found {len(departments)} departments")
        print(f"✅ Found {sum(len(d) for d in doctors_by_dept.values())} doctors")
        
        # Create patients and appointments
        created_patients = 0
        created_appointments = 0
        
        today = date.today()
        
        for patient_data in PATIENT_DATA:
            # Check if patient already exists
            existing = Patient.query.filter_by(phone=patient_data["phone"]).first()
            if existing:
                print(f"⚠️  Patient {patient_data['name']} already exists, skipping...")
                continue
            
            # Create patient
            # Generate unique patient_id
            patient_count = Patient.query.count()
            patient_id = f"P-{today.strftime('%Y%m%d')}-{patient_count + 1:03d}"
            
            patient = Patient(
                patient_id=patient_id,
                name=patient_data["name"],
                age=patient_data["age"],
                gender=patient_data["gender"],
                phone=patient_data["phone"],
                email=f"patient{patient_data['phone'][-4:]}@test.com",
                blood_group=random.choice(["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]),
                medical_history=f"Previous conditions: {patient_data['disease']}",
                is_emergency=any(word in patient_data["disease"].lower() for word in ["severe", "emergency", "chest pain"])
            )
            db.session.add(patient)
            db.session.flush()  # Get patient ID
            
            # Create user account for patient
            user = User(
                email=f"patient{patient_data['phone'][-4:]}@test.com",
                password_hash=generate_password_hash("test123"),
                name=patient_data["name"],
                phone=patient_data["phone"],
                role="patient"
            )
            db.session.add(user)
            db.session.flush()
            
            # Link patient to user (if User model has patient_id field)
            user.patient = patient
            
            created_patients += 1
            
            # Determine department based on disease
            dept_name = get_department_for_disease(patient_data["disease"])
            if dept_name not in departments:
                dept_name = "General Medicine"
            
            department = departments[dept_name]
            doctors = doctors_by_dept.get(dept_name, [])
            
            if not doctors:
                # Fallback to any available doctor
                doctors = Doctor.query.filter_by(is_available=True).all()
            
            if not doctors:
                print(f"⚠️  No doctors available for {patient_data['name']}")
                continue
            
            doctor = random.choice(doctors)
            
            # Create 1-3 appointments for each patient
            num_appointments = random.randint(1, 3)
            
            for i in range(num_appointments):
                # Mix of past, today, and future appointments
                if i == 0:
                    # First appointment - today or future
                    appt_date = today + timedelta(days=random.randint(0, 7))
                    status = random.choice(["scheduled", "confirmed", "waiting"])
                elif i == 1:
                    # Second appointment - past
                    appt_date = today - timedelta(days=random.randint(1, 30))
                    status = random.choice(["completed", "no_show"])
                else:
                    # Third appointment - future
                    appt_date = today + timedelta(days=random.randint(8, 30))
                    status = "scheduled"
                
                # Random time between 9 AM and 5 PM
                hour = random.randint(9, 16)
                minute = random.choice([0, 15, 30, 45])
                appt_time = time(hour, minute)
                end_time = time(hour, minute + 15) if minute < 45 else time(hour + 1, 0)
                
                # Generate appointment number
                appt_count = Appointment.query.filter_by(appointment_date=appt_date).count()
                appt_number = f"APT-{appt_date.strftime('%Y%m%d')}-{appt_count + 1:03d}"
                
                # Calculate priority score based on age and symptoms
                priority_score = 5.0  # Base score
                if patient.age > 60:
                    priority_score += 2.0
                if patient.age < 10:
                    priority_score += 1.5
                if any(word in patient_data["disease"].lower() for word in ["severe", "pain", "emergency", "chest"]):
                    priority_score += 2.5
                
                appointment = Appointment(
                    appointment_number=appt_number,
                    patient_id=patient.id,
                    doctor_id=doctor.id,
                    department_id=department.id,
                    appointment_date=appt_date,
                    appointment_time=appt_time,
                    slot_end_time=end_time,
                    symptoms=patient_data["disease"],
                    status=status,
                    priority_score=min(priority_score, 10.0),
                    estimated_wait_min=random.randint(10, 45) if status in ["waiting", "scheduled"] else 0
                )
                db.session.add(appointment)
                created_appointments += 1
            
            print(f"✅ Created: {patient_data['name']:25} | {dept_name:20} | {num_appointments} appointments")
        
        # Commit all changes
        db.session.commit()
        
        print("\n" + "=" * 70)
        print(f"   SUMMARY")
        print("=" * 70)
        print(f"✅ Created {created_patients} patients")
        print(f"✅ Created {created_appointments} appointments")
        print(f"✅ Total patients in system: {Patient.query.count()}")
        print(f"✅ Total appointments in system: {Appointment.query.count()}")
        print("\n" + "=" * 70)
        print("   TEST DATA READY!")
        print("=" * 70)
        print("\nYou can now:")
        print("1. View admin dashboard: http://127.0.0.1:5000/admin/")
        print("2. View queue: http://127.0.0.1:5000/admin/queue/")
        print("3. Check patient status with any phone: 9876543201 to 9876543230")
        print("4. Login as any patient: patient3201@test.com to patient3230@test.com")
        print("   Password: test123")

if __name__ == "__main__":
    create_test_patients()
