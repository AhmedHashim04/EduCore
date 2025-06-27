import json
from datetime import datetime, timedelta
import random

output = []

# Password hash for all users
PASSWORD_HASH = "pbkdf2_sha256$260000$gnZ1i7Y8W3o0KJ9x$abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGH="

# =====================
# 1. User Generation (50)
# =====================
for i in range(1, 51):
    user_type = 1 if i <= 5 else (2 if i <= 15 else (3 if i <= 45 else 4))
    output.append({
        "model": "users.User",
        "pk": i,
        "fields": {
            "password": PASSWORD_HASH,
            "username": f"user_{i}",
            "email": f"user_{i}@example.edu",
            "first_name": f"First_{i}",
            "last_name": f"Last_{i}",
            "user_type": user_type
        }
    })

# =====================
# 2. Department (5)
# =====================
departments = [
    {"name": "Computer Science", "code": "CS"},
    {"name": "Mathematics", "code": "MATH"},
    {"name": "Physics", "code": "PHY"},
    {"name": "Biology", "code": "BIO"},
    {"name": "Chemistry", "code": "CHEM"}
]
for i, dept in enumerate(departments):
    output.append({
        "model": "academics.Department",
        "pk": i + 1,
        "fields": {
            "name": dept["name"],
            "code": dept["code"],
            "description": f"Department of {dept['name']}",
            "head_of_department": None,
            "established_date": f"{1990 + i}-01-01",
            "website": f"https://{dept['code'].lower()}.example.edu",
            "budget_code": f"{dept['code']}-BUDGET",
            "contact_email": f"{dept['code'].lower()}@example.edu"
        }
    })

# =====================
# 3. Programs (10)
# =====================
programs = [
    {"name": "Computer Science BSc", "degree": "BSc", "dept": 1},
    {"name": "Data Science MSc", "degree": "MSc", "dept": 1},
    {"name": "Pure Mathematics", "degree": "BSc", "dept": 2},
    # Add 7 more programs...
]
for i, prog in enumerate(programs):
    output.append({
        "model": "academics.Program",
        "pk": i + 1,
        "fields": {
            "name": prog["name"],
            "code": f"{prog['degree']}-{i+1:03d}",
            "department": prog["dept"],
            "degree": prog["degree"],
            "duration": 4 if "BSc" in prog["degree"] else 2,
            "description": f"{prog['name']} program",
            "total_credits": 120 if "BSc" in prog["degree"] else 60,
            "accreditation_status": True,
            "accreditation_expiry": "2030-12-31"
        }
    })

# =====================
# 4. Semesters (6)
# =====================
semesters = []
for year in [2023, 2024]:
    for season in ["Fall", "Spring", "Summer"]:
        semesters.append({
            "year": year,
            "season": season,
            "start": f"{year}-{['08','01','05'][['Fall','Spring','Summer'].index(season)]}-01",
            "end": f"{year}-{['12','05','08'][['Fall','Spring','Summer'].index(season)]}-15"
        })

for i, sem in enumerate(semesters):
    output.append({
        "model": "academics.Semester",
        "pk": i + 1,
        "fields": {
            "year": sem["year"],
            "semester": sem["season"],
            "start_date": sem["start"],
            "end_date": sem["end"],
            "registration_start": f"{sem['year']}-01-01",
            "registration_end": f"{sem['year']}-02-01",
            "is_current": (i == len(semesters) - 1)  # Last is current
        }
    })

# Continue generation for other models following similar patterns...

# =====================
# Final Output
# =====================
with open("fixture_large.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"Generated {len(output)} records")