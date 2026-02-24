"""
Generate synthetic historical crowd data for ML training.
"""
import random
import pandas as pd
import numpy as np
from datetime import date, timedelta


def generate_crowd_data(num_days: int = 365, num_departments: int = 6) -> pd.DataFrame:
    """
    Generate realistic synthetic crowd data.

    Simulates 1 year of hospital OPD data with realistic patterns:
    - Monday surge
    - Morning peaks (9-11 AM)
    - Afternoon peaks (2-4 PM)
    - Weekend reduction
    - Seasonal flu patterns
    - Holiday effects
    """
    random.seed(42)
    np.random.seed(42)

    records = []
    start_date = date.today() - timedelta(days=num_days)

    # Define some holidays
    holidays = set()
    for m in range(1, 13):
        holidays.add(date(start_date.year, m, 1))
        holidays.add(date(start_date.year, m, 15))

    for day_offset in range(num_days):
        current_date = start_date + timedelta(days=day_offset)
        day_of_week = current_date.weekday()
        month = current_date.month
        is_holiday = current_date in holidays
        is_weekend = day_of_week >= 5

        for dept_id in range(1, num_departments + 1):
            for hour in range(8, 21):  # 8 AM to 8 PM
                # Base patient count
                base = 15

                # Department variation
                dept_factor = 1.0 + (dept_id % 3) * 0.2

                # Time of day effect
                if 9 <= hour <= 11:
                    time_factor = 1.8
                elif 14 <= hour <= 16:
                    time_factor = 1.5
                elif hour == 8 or hour >= 18:
                    time_factor = 0.4
                elif 12 <= hour <= 13:
                    time_factor = 0.7  # Lunch dip
                else:
                    time_factor = 1.0

                # Day of week effect
                if day_of_week == 0:
                    day_factor = 1.5  # Monday rush
                elif day_of_week == 4:
                    day_factor = 1.2  # Friday
                elif is_weekend:
                    day_factor = 0.3
                else:
                    day_factor = 1.0

                # Seasonal effect
                if month in [11, 12, 1, 2]:
                    season_factor = 1.4  # Flu season
                elif month in [6, 7]:
                    season_factor = 1.15  # Monsoon diseases
                else:
                    season_factor = 1.0

                # Holiday effect
                holiday_factor = 0.2 if is_holiday else 1.0

                # Temperature
                temp = 25 + 10 * np.sin(2 * np.pi * (month - 1) / 12)
                temp += random.uniform(-3, 3)

                # Calculate patient count
                count = int(
                    base
                    * dept_factor
                    * time_factor
                    * day_factor
                    * season_factor
                    * holiday_factor
                    + random.gauss(0, 3)
                )
                count = max(0, count)

                # Determine crowd level
                if count <= 10:
                    level = "low"
                    level_code = 0
                elif count <= 25:
                    level = "medium"
                    level_code = 1
                elif count <= 40:
                    level = "high"
                    level_code = 2
                else:
                    level = "critical"
                    level_code = 3

                # Average wait time
                avg_wait = count * random.uniform(1.5, 3.0)

                # Weather
                weather_options = ["clear", "cloudy", "rainy", "hot", "cold"]
                if month in [6, 7, 8]:
                    weather = random.choice(["rainy", "cloudy", "clear"])
                elif month in [12, 1, 2]:
                    weather = random.choice(["cold", "clear", "cloudy"])
                else:
                    weather = random.choice(["clear", "hot", "cloudy"])

                # Feature engineering
                is_morning_peak = 1 if 9 <= hour <= 11 else 0
                is_afternoon_peak = 1 if 14 <= hour <= 16 else 0
                is_flu_season = 1 if month in [11, 12, 1, 2] else 0
                is_monday = 1 if day_of_week == 0 else 0

                records.append(
                    {
                        "department_id": dept_id,
                        "log_date": current_date,
                        "hour": hour,
                        "day_of_week": day_of_week,
                        "month": month,
                        "is_holiday": int(is_holiday),
                        "is_weekend": int(is_weekend),
                        "is_monday": is_monday,
                        "is_morning_peak": is_morning_peak,
                        "is_afternoon_peak": is_afternoon_peak,
                        "is_flu_season": is_flu_season,
                        "temperature": round(temp, 1),
                        "weather": weather,
                        "patient_count": count,
                        "avg_wait_time": round(avg_wait, 1),
                        "crowd_level": level,
                        "crowd_level_code": level_code,
                    }
                )

    df = pd.DataFrame(records)
    print(f"Generated {len(df)} records")
    print(f"Crowd level distribution:\n{df['crowd_level'].value_counts()}")
    return df


if __name__ == "__main__":
    df = generate_crowd_data()
    df.to_csv("crowd_data.csv", index=False)
    print("Saved to crowd_data.csv")
