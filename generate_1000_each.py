# DataNexus SLU Synthetic Dataset (exact 1000 rows per table)
# Data Source: Synthetic (Faker, NumPy, Pandas)
# Collection Date: October 2025
# Date Range: 2015–2025

import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

SEED = 20251019
random.seed(SEED)
np.random.seed(SEED)
fake = Faker("en_US")

N = 1000  # <-- EXACT ROWS per table

majors = [
    "Computer Science","Information Systems","Data Science","Cybersecurity","Business Analytics",
    "Software Engineering","Electrical Engineering","Finance","Marketing","Biostatistics"
]
degrees = ["BS","BA","MS","MBA","PhD"]
industries = ["Technology","Finance","Healthcare","Consulting","Education","Retail","Manufacturing","Government","Non-Profit","Energy"]
technologies = ["Java","Python","JavaScript","SQL","AWS","Azure","GCP","Snowflake","Tableau","Power BI","Salesforce","Docker","Kubernetes","React","Node.js",".NET","C++","R","Spark","Hadoop"]
roles = ["Software Engineer","Data Analyst","Data Engineer","Business Analyst","QA Engineer","SDET","Product Manager","DevOps Engineer","ML Engineer","Security Analyst","Salesforce Developer"]
job_portals = ["LinkedIn","Handshake","Indeed","Company Site","Referral","Glassdoor","Campus Career Fair"]
event_types = ["Career Fair","Workshop","Seminar","Hackathon","Alumni Meetup","Webinar","Employer Info Session"]

states = ["MO","IL","CA","TX","NY","MA","WA","FL","CO","NC","AZ","GA","OH","PA","MI"]
cities_by_state = {
    "MO": ["St. Louis","Kansas City","Columbia","Springfield","Chesterfield","Clayton"],
    "IL": ["Chicago","Springfield","Urbana","Naperville","Peoria"],
    "CA": ["San Francisco","San Jose","Los Angeles","San Diego","Irvine"],
    "TX": ["Austin","Dallas","Houston","San Antonio","Plano"],
    "NY": ["New York","Buffalo","Rochester","Albany","White Plains"],
    "MA": ["Boston","Cambridge","Worcester","Somerville"],
    "WA": ["Seattle","Bellevue","Redmond","Tacoma"],
    "FL": ["Miami","Orlando","Tampa","Jacksonville"],
    "CO": ["Denver","Boulder","Colorado Springs","Fort Collins"],
    "NC": ["Raleigh","Charlotte","Durham","Cary"],
    "AZ": ["Phoenix","Tempe","Scottsdale","Tucson"],
    "GA": ["Atlanta","Alpharetta","Savannah"],
    "OH": ["Columbus","Cleveland","Cincinnati"],
    "PA": ["Philadelphia","Pittsburgh","Harrisburg"],
    "MI": ["Detroit","Ann Arbor","Grand Rapids"]
}

def rand_city_state():
    st = random.choice(states)
    return random.choice(cities_by_state[st]), st

def random_date(start_year=2015, end_year=2025):
    start = datetime(start_year,1,1)
    end = datetime(end_year,12,31)
    delta = end - start
    return (start + timedelta(days=random.randint(0, delta.days))).date().isoformat()

# ---------- Alumni (1000) ----------
alumni_rows = []
for i in range(1, N+1):
    grad_year = random.randint(2015, 2025)
    years_since = 2025 - grad_year
    if years_since <= 0:
        phase = "CPT"
    elif years_since == 1:
        phase = random.choice(["OPT","CPT"])
    elif years_since <= 3:
        phase = random.choice(["OPT","STEM-OPT"])
    else:
        phase = "Full-Time"

    first, last = fake.first_name(), fake.last_name()
    city, state = rand_city_state()
    alumni_rows.append({
        "Alumni_ID": i,
        "First_Name": first,
        "Last_Name": last,
        "SLU_Email": f"{first.lower()}.{last.lower()}{random.randint(1,999)}@slu.edu",
        "Personal_Email": f"{first.lower()}.{last.lower()}{random.randint(1,999)}@{random.choice(['gmail.com','outlook.com','yahoo.com'])}",
        "Degree": random.choice(degrees),
        "Major": random.choice(majors),
        "Graduation_Year": grad_year,
        "Visa_Phase": phase,  # CPT/OPT/STEM-OPT/Full-Time
        "City": city,
        "State": state,
        "Country": "USA"
    })
alumni_df = pd.DataFrame(alumni_rows)

# dictionaries for quick lookups
grad_year_map = dict(zip(alumni_df.Alumni_ID, alumni_df.Graduation_Year))

# ---------- Employers (1000) ----------
domains = ["techcorp.com","finvista.com","healthplus.org","consultex.com","edulabs.edu","retailmax.com","manufab.io","govservices.gov","greenenergy.co","nonprofit.org"]
employer_rows = []
for i in range(1, N+1):
    company = fake.unique.company()
    city, state = rand_city_state()
    employer_rows.append({
        "Employer_ID": i,
        "Company_Name": company,
        "Industry": random.choice(industries),
        "City": city,
        "State": state,
        "Country": "USA",
        "Partnership_Level": random.choice(["Prospect","Bronze","Silver","Gold","Strategic"]),
        "Contact_Name": fake.name(),
        "Contact_Email": f"hr@{random.choice(domains)}",
        "Contact_Phone": fake.phone_number()
    })
employers_df = pd.DataFrame(employer_rows)

# ---------- Events (1000) ----------
event_rows = []
for i in range(1, N+1):
    etype = random.choice(event_types)
    city, state = rand_city_state()
    event_rows.append({
        "Event_ID": i,
        "Event_Name": f"{etype} {fake.word().capitalize()}",
        "Event_Type": etype,
        "Organizer": random.choice(["SLU Career Services","SLU Alumni Association","Employer Relations","Computer Science Dept.","Business School","External Employer"]),
        "Event_Date": random_date(2015, 2025),
        "Category": random.choice(["University","Employer"]),
        "Location_City": city,
        "Location_State": state
    })
events_df = pd.DataFrame(event_rows)

# quick event-year lookup
event_year_map = dict(zip(events_df.Event_ID, events_df.Event_Date.str[:4].astype(int)))

# ---------- Jobs (1000) ----------
# Pick exactly N random alumni and employers (with replacement allowed)
job_rows = []
for job_id in range(1, N+1):
    alum_id = random.randint(1, N)                      # 1..1000
    emp_id  = random.randint(1, N)                      # 1..1000
    grad = grad_year_map[alum_id]
    start_year = max(grad - 1, 2015)
    start_date = random_date(start_year, 2025)
    salary = int(np.clip(np.random.normal(95000, 20000), 45000, 220000))
    job_rows.append({
        "Job_ID": job_id,
        "Alumni_ID": alum_id,
        "Employer_ID": emp_id,
        "Role": random.choice(roles),
        "Technology": ", ".join(random.sample(technologies, k=random.choice([1,2,3]))),
        "Job_Portal": random.choice(job_portals),
        "Salary_USD": salary,
        "Start_Date": start_date
    })
jobs_df = pd.DataFrame(job_rows)

# ---------- Engagements (1000) ----------
# For each row, pick an alumni and an event consistent with timeline when possible
eng_rows = []
for eng_id in range(1, N+1):
    alum_id = random.randint(1, N)
    grad = grad_year_map[alum_id]
    # Prefer events that are not too far before enrollment (grad-2)
    # Try up to 5 times to find a suitable event; otherwise fallback to any event
    chosen_event = None
    for _ in range(5):
        ev_id = random.randint(1, N)
        if event_year_map[ev_id] >= grad - 2:
            chosen_event = ev_id
            break
    if chosen_event is None:
        chosen_event = random.randint(1, N)

    eng_rows.append({
        "Engagement_ID": eng_id,
        "Alumni_ID": alum_id,
        "Event_ID": chosen_event,
        "Participation_Score": int(np.clip(np.random.normal(80, 15), 20, 100)),
        "Feedback_Text": random.choice([
            "Great networking opportunity","Informative session","Helpful for interviews",
            "Met potential employers","Good alumni connections","Relevant content","Average experience"
        ])
    })
engagements_df = pd.DataFrame(eng_rows)

# ---------- Students (1000) ----------
students_rows = []
programs = [
    "MS Information Systems","MS Computer Science","MBA","MS Data Science",
    "MS Cybersecurity","MS Analytics","MS Software Engineering"
]
visa_statuses = ["F1","CPT","OPT","STEM-OPT"]

for i in range(1, N+1):
    first, last = fake.first_name(), fake.last_name()
    city, state = rand_city_state()
    enroll_year = random.randint(2018, 2024)
    grad_year = enroll_year + random.choice([1,2,3])
    # 30% have internships (links to Employers table by FK)
    emp_id = random.randint(1, N) if random.random() < 0.30 else None
    internship_role = random.choice([
        "Data Analyst Intern","Software Intern","QA Intern",
        "Research Assistant","DevOps Intern"
    ]) if emp_id else None
    internship_start = random_date(enroll_year, grad_year) if emp_id else None

    students_rows.append({
        "Student_ID": i,
        "First_Name": first,
        "Last_Name": last,
        "SLU_Email": f"{first.lower()}.{last.lower()}{random.randint(1,999)}@slu.edu",
        "Program": random.choice(programs),
        "Major": random.choice(majors),
        "Enrollment_Year": enroll_year,
        "Expected_Graduation_Year": grad_year,
        "Visa_Status": random.choice(visa_statuses),
        "City": city,
        "State": state,
        "Country": "USA",
        "Current_Employer_ID": emp_id,          # FK to Employers.Employer_ID (nullable)
        "Internship_Role": internship_role,
        "Internship_Start_Date": internship_start
    })

students_df = pd.DataFrame(students_rows)

# ---------- Save CSVs ----------
alumni_df.to_csv("alumni.csv", index=False)
employers_df.to_csv("employers.csv", index=False)
events_df.to_csv("events.csv", index=False)
jobs_df.to_csv("jobs.csv", index=False)
engagements_df.to_csv("engagements.csv", index=False)
students_df.to_csv("students.csv", index=False)


# ---------- Data Dictionary ----------
def dtype_of(s): return str(s.dtype)
rows = []
for name, df in [
    ("alumni", alumni_df), ("employers", employers_df), ("events", events_df),
    ("jobs", jobs_df), ("engagements", engagements_df), ("students", students_df)
]:
    for col in df.columns:
        ex = df[col].dropna().astype(str).head(1).values[0] if not df[col].dropna().empty else ""
        rows.append({"Table":name,"Column":col,"Dtype":str(df[col].dtype),"Example":ex,"Description":""})
pd.DataFrame(rows).to_csv("data_dictionary.csv", index=False)

print("Done. Created alumni.csv, employers.csv, events.csv, jobs.csv, engagements.csv, data_dictionary.csv (all 1000 rows).")

# ---------- DATA VERIFICATION ----------
import os

base = os.path.expanduser("~")

print("\n\n=== DATA VERIFICATION REPORT ===")

tables = {
    "students": pd.read_csv(os.path.join(base,"students.csv")),
    "alumni": pd.read_csv(os.path.join(base,"alumni.csv")),
    "employers": pd.read_csv(os.path.join(base,"employers.csv")),
    "jobs": pd.read_csv(os.path.join(base,"jobs.csv")),
    "events": pd.read_csv(os.path.join(base,"events.csv")),
    "engagements": pd.read_csv(os.path.join(base,"engagements.csv")),
}

print("→ Row counts (expect 1000 each)")
for name, df in tables.items():
    print(f"{name:12s}: {df.shape[0]} rows")

print("\n→ Primary key uniqueness")
pk_map = {
    "students": "Student_ID",
    "alumni": "Alumni_ID",
    "employers": "Employer_ID",
    "jobs": "Job_ID",
    "events": "Event_ID",
    "engagements": "Engagement_ID",
}
for name, df in tables.items():
    pk = pk_map[name]
    print(f"{name:12s} ({pk}) unique ->", df[pk].is_unique)

print("\n→ Foreign key integrity")
a = tables["alumni"]
e = tables["employers"]
v = tables["events"]
j = tables["jobs"]
g = tables["engagements"]
s = tables["students"]

print("Jobs.Alumni_ID ⊆ Alumni.Alumni_ID ->", j["Alumni_ID"].isin(a["Alumni_ID"]).all())
print("Jobs.Employer_ID ⊆ Employers.Employer_ID ->", j["Employer_ID"].isin(e["Employer_ID"]).all())
print("Engagements.Alumni_ID ⊆ Alumni.Alumni_ID ->", g["Alumni_ID"].isin(a["Alumni_ID"]).all())
print("Engagements.Event_ID ⊆ Events.Event_ID ->", g["Event_ID"].isin(v["Event_ID"]).all())

valid_students_fk = s["Current_Employer_ID"].dropna().astype(int).isin(e["Employer_ID"]).all()
print("Students.Current_Employer_ID ⊆ Employers.Employer_ID (where not null) ->", valid_students_fk)

print("\n=== SAMPLE PREVIEW ===")
for name, df in tables.items():
    print(f"\n{name.upper()} sample:")
    print(df.head(3))
