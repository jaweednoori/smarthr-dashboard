from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from ... import models
from .database import engine, get_db, SessionLocal
from faker import Faker
import random
from datetime import date, timedelta

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="SmartHR Dashboard API")

fake = Faker()

DEPARTMENTS = ["Engineering", "Human Resources", "Finance", "Marketing", "Operations"]
JOB_TITLES = {
    "Engineering": ["Software Engineer", "DevOps Engineer", "QA Engineer", "Tech Lead"],
    "Human Resources": ["HR Specialist", "Recruiter", "HRMIS Analyst", "HR Manager"],
    "Finance": ["Accountant", "Financial Analyst", "Payroll Specialist", "CFO"],
    "Marketing": ["Marketing Specialist", "Content Writer", "SEO Analyst", "Brand Manager"],
    "Operations": ["Operations Manager", "Logistics Coordinator", "Analyst", "Director"],
}

def seed_data():
    db = SessionLocal()
    if db.query(models.Department).count() > 0:
        db.close()
        return
    dept_objects = []
    for dept_name in DEPARTMENTS:
        dept = models.Department(name=dept_name)
        db.add(dept)
        dept_objects.append(dept)
    db.commit()
    for dept in dept_objects:
        db.refresh(dept)
    for _ in range(50):
        dept = random.choice(dept_objects)
        title = random.choice(JOB_TITLES[dept.name])
        hire_date = fake.date_between(start_date="-5y", end_date="today")
        emp = models.Employee(
            full_name=fake.name(),
            email=fake.unique.email(),
            job_title=title,
            salary=round(random.uniform(40000, 120000), 2),
            hire_date=hire_date,
            department_id=dept.id,
        )
        db.add(emp)
    db.commit()
    employees = db.query(models.Employee).all()
    leave_types = ["Annual Leave", "Sick Leave", "Maternity Leave", "Unpaid Leave"]
    for emp in random.sample(employees, 20):
        start = fake.date_between(start_date="-1y", end_date="today")
        end = start + timedelta(days=random.randint(1, 14))
        leave = models.LeaveRequest(
            employee_id=emp.id,
            leave_type=random.choice(leave_types),
            start_date=start,
            end_date=end,
            status=random.choice(list(models.LeaveStatus)),
        )
        db.add(leave)
    db.commit()
    db.close()

seed_data()

@app.get("/")
def root():
    return {"message": "SmartHR Dashboard API is running!"}

@app.get("/employees")
def get_employees(db: Session = Depends(get_db)):
    return db.query(models.Employee).all()

@app.get("/employees/{employee_id}")
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    emp = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

@app.get("/departments")
def get_departments(db: Session = Depends(get_db)):
    return db.query(models.Department).all()

@app.get("/analytics/headcount")
def headcount_by_department(db: Session = Depends(get_db)):
    results = db.query(
        models.Department.name,
        func.count(models.Employee.id).label("count")
    ).join(models.Employee).group_by(models.Department.name).all()
    return [{"department": r[0], "count": r[1]} for r in results]

@app.get("/analytics/leave-summary")
def leave_summary(db: Session = Depends(get_db)):
    results = db.query(
        models.LeaveRequest.status,
        func.count(models.LeaveRequest.id).label("count")
    ).group_by(models.LeaveRequest.status).all()
    return [{"status": r[0], "count": r[1]} for r in results]

@app.get("/leave-requests")
def get_leave_requests(db: Session = Depends(get_db)):
    return db.query(models.LeaveRequest).all()