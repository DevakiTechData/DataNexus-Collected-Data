# DataNexus SLU Alumni Connect – Synthetic Dataset  
*Capstone Project | Saint Louis University (MS Information Systems)*  

## 📘 Overview  
This repository contains a **synthetic, ethically generated dataset** created for the capstone project **DataNexus SLU Alumni Connect Platform**.  
The project aims to analyze and visualize connections between **MS students, alumni, employers, and SLU administrators** using data-driven dashboards.  

The dataset mirrors SLU’s student–alumni–employer ecosystem from **2015 to 2025**, helping the university track:  
- Student visa/work phases (CPT, OPT, STEM-OPT)  
- Alumni employment outcomes  
- Employer partnerships and hiring trends  
- Event participation and engagement metrics  

All data in this repository is **synthetic** — no real or personal information is included.

---

## 🧩 Dataset Description  
The dataset follows a **relational structure** aligned with the project’s **Entity Relationship Diagram (ERD)**.  
Each table contains **1,000 records** and maintains referential integrity across all primary and foreign keys.

| Table | Description | Key Fields |
|-------|--------------|------------|
| **students.csv** | Current MS students, their programs, visa/work status, and internships | `Student_ID (PK)`, `Current_Employer_ID (FK)` |
| **alumni.csv** | SLU alumni records including graduation year, degree, location, and work phase | `Alumni_ID (PK)` |
| **employers.csv** | Employer details such as company name, industry, city, and partnership level | `Employer_ID (PK)` |
| **jobs.csv** | Job information connecting alumni to employers | `Job_ID (PK)`, `Alumni_ID (FK)`, `Employer_ID (FK)` |
| **events.csv** | University and employer event details (type, date, location) | `Event_ID (PK)` |
| **engagements.csv** | Records of alumni participation and feedback in events | `Engagement_ID (PK)`, `Alumni_ID (FK)`, `Event_ID (FK)` |
| **data_dictionary.csv** | Column-level metadata and example values for all six tables | — |

---

## 🧠 Data Model  
**Entity Relationships:**
Students → Employers (via Current_Employer_ID)
Alumni → Jobs (1-to-many)
Employers→ Jobs (1-to-many)
Alumni → Engagements (1-to-many)
Events → Engagements (1-to-many)


**Date Range:** 2015 – 2025  
**Collection Date:** October 2025  
**Data Type:** Structured, quantitative, synthetic  

---

## 🛠️ Generation Method  
The dataset was created using Python with the following libraries:
- [Faker](https://faker.readthedocs.io/) – generates realistic names, emails, companies, and locations  
- [NumPy](https://numpy.org/) – produces numeric and date distributions  
- [Pandas](https://pandas.pydata.org/) – manages tabular structures and exports CSVs  

A verification script was executed to confirm:
- ✅ 1,000 rows per table  
- ✅ Unique primary keys  
- ✅ Valid foreign-key relationships  

---

## 📂 Folder Structure
📁 DataNexus-SLU-Dataset/
│
├── students.csv
├── alumni.csv
├── employers.csv
├── jobs.csv
├── events.csv
├── engagements.csv
├── data_dictionary.csv
└── README.md


---

## 💡 Usage  
You can load these CSV files into:
- **Power BI / Tableau** for interactive dashboards  
- **MySQL / PostgreSQL** for relational modeling  
- **Python / Pandas** for analytics and visualization  

### Example (Python)
```python
import pandas as pd

students = pd.read_csv("students.csv")
alumni = pd.read_csv("alumni.csv")
jobs = pd.read_csv("jobs.csv")

print(students.head())

⚖️ License & Ethics

This dataset is synthetic and free for educational and research purposes.
It contains no personally identifiable information (PII).
© 2025 Devaki Bathalapalli | Saint Louis University

🙌 Acknowledgements

Course: IS 5960 – Masters Research Project

Department of Information Systems, Saint Louis University

Tools: Python 3.13 | Faker | NumPy | Pandas
