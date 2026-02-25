"""
Preprocess Medical Appointment No-Show Dataset.
Source: https://www.kaggle.com/datasets/joniarroba/noshowappointments

This script:
1. Loads the raw no-show dataset (110k+ records)
2. Cleans and engineers features
3. Prepares data for ML training
4. Saves processed dataset
"""
import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))


def load_noshow_data(filepath="data/raw/no_show.csv"):
    """Load the raw no-show dataset."""
    print(f"Loading dataset from: {filepath}")
    
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        print("\n📥 Please download the dataset from:")
        print("   https://www.kaggle.com/datasets/joniarroba/noshowappointments")
        print("   Save as: data/raw/no_show.csv")
        return None
    
    df = pd.read_csv(filepath)
    print(f"✅ Loaded {len(df):,} records")
    print(f"   Columns: {list(df.columns)}")
    return df


def clean_data(df):
    """Clean and validate the dataset."""
    print("\n[1/4] Cleaning data...")
    
    original_count = len(df)
    
    # Convert date columns to datetime
    df['ScheduledDay'] = pd.to_datetime(df['ScheduledDay'])
    df['AppointmentDay'] = pd.to_datetime(df['AppointmentDay'])
    
    # Remove invalid records
    # 1. Remove appointments scheduled after appointment day (data errors)
    df = df[df['ScheduledDay'] <= df['AppointmentDay']]
    
    # 2. Remove invalid ages (negative or > 120)
    df = df[(df['Age'] >= 0) & (df['Age'] <= 120)]
    
    # 3. Remove duplicate appointments
    df = df.drop_duplicates(subset=['AppointmentID'])
    
    removed = original_count - len(df)
    print(f"   Removed {removed:,} invalid records ({removed/original_count*100:.1f}%)")
    print(f"   Remaining: {len(df):,} records")
    
    return df


def engineer_features(df):
    """Create derived features for ML."""
    print("\n[2/4] Engineering features...")
    
    # 1. Booking gap (days between scheduling and appointment)
    df['booking_gap_days'] = (df['AppointmentDay'] - df['ScheduledDay']).dt.days
    
    # 2. Temporal features from AppointmentDay
    df['day_of_week'] = df['AppointmentDay'].dt.dayofweek  # 0=Monday, 6=Sunday
    df['month'] = df['AppointmentDay'].dt.month
    df['day_of_month'] = df['AppointmentDay'].dt.day
    df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
    df['is_monday'] = (df['day_of_week'] == 0).astype(int)
    
    # 3. Age groups
    df['age_group'] = pd.cut(
        df['Age'], 
        bins=[0, 12, 18, 35, 50, 65, 120],
        labels=['child', 'teen', 'young_adult', 'adult', 'senior', 'elderly']
    )
    df['is_elderly'] = (df['Age'] >= 65).astype(int)
    df['is_child'] = (df['Age'] <= 12).astype(int)
    
    # 4. Convert No-show to binary (0=showed, 1=no-show)
    df['no_show'] = (df['No-show'] == 'Yes').astype(int)
    
    # 5. Count previous no-shows per patient
    df = df.sort_values(['PatientId', 'AppointmentDay'])
    df['previous_no_shows'] = df.groupby('PatientId')['no_show'].cumsum() - df['no_show']
    
    # 6. Appointment count per patient (loyalty indicator)
    df['appointment_count'] = df.groupby('PatientId').cumcount() + 1
    
    # 7. Health risk score (sum of chronic conditions)
    df['health_risk_score'] = (
        df['Hipertension'] + 
        df['Diabetes'] + 
        df['Alcoholism'] + 
        df['Handcap']
    )
    
    # 8. Booking urgency (same day = 1, else 0)
    df['is_same_day'] = (df['booking_gap_days'] == 0).astype(int)
    df['is_short_notice'] = (df['booking_gap_days'] <= 3).astype(int)
    
    print(f"   Created {len([c for c in df.columns if c not in ['PatientId', 'AppointmentID', 'ScheduledDay', 'AppointmentDay', 'No-show']])} features")
    
    return df


def analyze_patterns(df):
    """Analyze no-show patterns for insights."""
    print("\n[3/4] Analyzing patterns...")
    
    no_show_rate = df['no_show'].mean() * 100
    print(f"\n   Overall No-Show Rate: {no_show_rate:.1f}%")
    
    # By age group
    print("\n   No-Show Rate by Age Group:")
    age_analysis = df.groupby('age_group')['no_show'].agg(['mean', 'count'])
    for age, row in age_analysis.iterrows():
        print(f"      {age:15s}: {row['mean']*100:5.1f}% (n={row['count']:,})")
    
    # By booking gap
    print("\n   No-Show Rate by Booking Gap:")
    gap_bins = [0, 1, 3, 7, 14, 30, 365]
    gap_labels = ['Same day', '1-3 days', '4-7 days', '1-2 weeks', '2-4 weeks', '1+ months']
    df['gap_category'] = pd.cut(df['booking_gap_days'], bins=gap_bins, labels=gap_labels)
    gap_analysis = df.groupby('gap_category')['no_show'].agg(['mean', 'count'])
    for gap, row in gap_analysis.iterrows():
        print(f"      {gap:15s}: {row['mean']*100:5.1f}% (n={row['count']:,})")
    
    # By SMS received
    print("\n   No-Show Rate by SMS Reminder:")
    sms_analysis = df.groupby('SMS_received')['no_show'].agg(['mean', 'count'])
    for sms, row in sms_analysis.iterrows():
        sms_label = "SMS sent" if sms == 1 else "No SMS"
        print(f"      {sms_label:15s}: {row['mean']*100:5.1f}% (n={row['count']:,})")
    
    # By day of week
    print("\n   No-Show Rate by Day of Week:")
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dow_analysis = df.groupby('day_of_week')['no_show'].agg(['mean', 'count'])
    for dow, row in dow_analysis.iterrows():
        print(f"      {days[dow]:15s}: {row['mean']*100:5.1f}% (n={row['count']:,})")
    
    return df


def save_processed_data(df, output_path="data/processed/no_show_processed.csv"):
    """Save the processed dataset."""
    print(f"\n[4/4] Saving processed data...")
    
    # Create output directory
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Select relevant columns for ML
    ml_columns = [
        # Identifiers
        'PatientId', 'AppointmentID', 'AppointmentDay',
        
        # Target variable
        'no_show',
        
        # Patient features
        'Gender', 'Age', 'age_group', 'is_elderly', 'is_child',
        'Scholarship', 'health_risk_score',
        'previous_no_shows', 'appointment_count',
        
        # Appointment features
        'booking_gap_days', 'is_same_day', 'is_short_notice',
        'day_of_week', 'month', 'is_weekend', 'is_monday',
        'SMS_received',
        
        # Medical conditions
        'Hipertension', 'Diabetes', 'Alcoholism', 'Handcap',
        
        # Location
        'Neighbourhood'
    ]
    
    df_ml = df[ml_columns].copy()
    df_ml.to_csv(output_path, index=False)
    
    print(f"   ✅ Saved {len(df_ml):,} records to: {output_path}")
    print(f"   Columns: {len(ml_columns)}")
    print(f"   File size: {os.path.getsize(output_path) / 1024 / 1024:.1f} MB")
    
    return df_ml


def generate_summary_report(df, output_path="data/processed/no_show_summary.txt"):
    """Generate a summary report."""
    print("\n[BONUS] Generating summary report...")
    
    with open(output_path, 'w') as f:
        f.write("=" * 70 + "\n")
        f.write("   MEDICAL APPOINTMENT NO-SHOW DATASET - SUMMARY REPORT\n")
        f.write("=" * 70 + "\n\n")
        
        f.write(f"Dataset Size: {len(df):,} records\n")
        f.write(f"Date Range: {df['AppointmentDay'].min().date()} to {df['AppointmentDay'].max().date()}\n")
        f.write(f"Unique Patients: {df['PatientId'].nunique():,}\n")
        f.write(f"Overall No-Show Rate: {df['no_show'].mean()*100:.2f}%\n\n")
        
        f.write("Feature Statistics:\n")
        f.write("-" * 70 + "\n")
        f.write(f"  Average Age: {df['Age'].mean():.1f} years\n")
        f.write(f"  Average Booking Gap: {df['booking_gap_days'].mean():.1f} days\n")
        f.write(f"  SMS Reminder Rate: {df['SMS_received'].mean()*100:.1f}%\n")
        f.write(f"  Weekend Appointments: {df['is_weekend'].mean()*100:.1f}%\n")
        f.write(f"  Patients with Hypertension: {df['Hipertension'].mean()*100:.1f}%\n")
        f.write(f"  Patients with Diabetes: {df['Diabetes'].mean()*100:.1f}%\n\n")
        
        f.write("Key Insights:\n")
        f.write("-" * 70 + "\n")
        
        # Insight 1: SMS impact
        sms_impact = df.groupby('SMS_received')['no_show'].mean()
        if len(sms_impact) == 2:
            reduction = (sms_impact[0] - sms_impact[1]) / sms_impact[0] * 100
            f.write(f"  1. SMS reminders reduce no-shows by {reduction:.1f}%\n")
        
        # Insight 2: Booking gap
        same_day = df[df['is_same_day'] == 1]['no_show'].mean()
        long_gap = df[df['booking_gap_days'] > 30]['no_show'].mean()
        f.write(f"  2. Same-day appointments: {same_day*100:.1f}% no-show rate\n")
        f.write(f"     Long-gap (>30 days): {long_gap*100:.1f}% no-show rate\n")
        
        # Insight 3: Age factor
        elderly_rate = df[df['is_elderly'] == 1]['no_show'].mean()
        young_rate = df[df['Age'] < 35]['no_show'].mean()
        f.write(f"  3. Elderly patients (65+): {elderly_rate*100:.1f}% no-show rate\n")
        f.write(f"     Young patients (<35): {young_rate*100:.1f}% no-show rate\n")
        
        # Insight 4: Repeat no-shows
        repeat = df[df['previous_no_shows'] > 0]['no_show'].mean()
        first_time = df[df['previous_no_shows'] == 0]['no_show'].mean()
        f.write(f"  4. Patients with previous no-shows: {repeat*100:.1f}% rate\n")
        f.write(f"     First-time patients: {first_time*100:.1f}% rate\n")
        
        f.write("\n" + "=" * 70 + "\n")
    
    print(f"   ✅ Summary saved to: {output_path}")


def main():
    """Main preprocessing pipeline."""
    print("\n" + "=" * 70)
    print("   MEDICAL APPOINTMENT NO-SHOW DATASET PREPROCESSING")
    print("=" * 70 + "\n")
    
    # Load data
    df = load_noshow_data()
    if df is None:
        return
    
    # Clean data
    df = clean_data(df)
    
    # Engineer features
    df = engineer_features(df)
    
    # Analyze patterns
    df = analyze_patterns(df)
    
    # Save processed data
    df_ml = save_processed_data(df)
    
    # Generate summary report
    generate_summary_report(df)
    
    print("\n" + "=" * 70)
    print("   ✅ PREPROCESSING COMPLETE!")
    print("=" * 70)
    print("\nNext steps:")
    print("  1. Review: data/processed/no_show_summary.txt")
    print("  2. Train model: python app/ml/train_noshow_model.py")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
