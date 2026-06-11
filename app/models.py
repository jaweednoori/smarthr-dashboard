from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .database import Base
import enum

class LeaveStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    employees = relationship("Employee", back_populates="department")

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    job_title = Column(String)
    salary = Column(Float)
    hire_date = Column(Date)
    department_id = Column(Integer, ForeignKey("departments.id"))
    department = relationship("Department", back_populates="employees")
    leave_requests = relationship("LeaveRequest", back_populates="employee")

class LeaveRequest(Base):
    __tablename__ = "leave_requests"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    leave_type = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(Enum(LeaveStatus), default=LeaveStatus.pending)
    employee = relationship("Employee", back_populates="leave_requests")