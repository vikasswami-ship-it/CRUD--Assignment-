from sqlalchemy import Column, Integer, String, Float, DateTime, CheckConstraint
from sqlalchemy.sql import func
from app.database import Base


class Employee(Base):
    """Employee database model using SQLAlchemy ORM"""
    
    __tablename__ = "employees"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Basic Information
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    mobile = Column(String(20), nullable=False, unique=True)
    
    # Department and Role
    department = Column(String(100), nullable=False, index=True)
    designation = Column(String(100), nullable=False)
    
    # Salary
    salary = Column(Float, nullable=False)
    
    # Employment Details
    date_of_joining = Column(DateTime, nullable=False)
    status = Column(String(20), nullable=False, default="ACTIVE")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Constraints
    __table_args__ = (
        CheckConstraint("salary > 0", name="check_salary_positive"),
        CheckConstraint("status IN ('ACTIVE', 'INACTIVE')", name="check_status_valid"),
    )
    
    def __repr__(self):
        return f"<Employee(id={self.id}, name={self.name}, email={self.email})>"
