from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
import re


class EmployeeBase(BaseModel):
    """Base schema for Employee with common fields"""
    name: str = Field(..., min_length=2, max_length=255, description="Full name of the employee")
    email: EmailStr = Field(..., description="Unique email address")
    mobile: str = Field(..., min_length=10, max_length=20, description="Unique mobile number")
    department: str = Field(..., min_length=2, max_length=100, description="Department name")
    designation: str = Field(..., min_length=2, max_length=100, description="Job title")
    salary: float = Field(..., gt=0, description="Monthly salary (must be positive)")
    date_of_joining: datetime = Field(..., description="Employee joining date")
    status: str = Field(default="ACTIVE", description="Employee status (ACTIVE or INACTIVE)")
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Validate email format"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError('Invalid email format')
        return v
    
    @field_validator('mobile')
    @classmethod
    def validate_mobile(cls, v: str) -> str:
        """Validate mobile format (10-20 digits with optional + and -)"""
        mobile_pattern = r'^[+]?[0-9\-]{10,20}$'
        if not re.match(mobile_pattern, v):
            raise ValueError('Invalid mobile format (10-20 digits, may include + or -)')
        # Remove any spaces
        return v.replace(" ", "")
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Validate status field"""
        if v not in ["ACTIVE", "INACTIVE"]:
            raise ValueError('Status must be either ACTIVE or INACTIVE')
        return v.upper()


class EmployeeCreate(EmployeeBase):
    """Schema for creating a new employee"""
    pass


class EmployeeUpdate(BaseModel):
    """Schema for updating an employee"""
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    email: Optional[EmailStr] = None
    mobile: Optional[str] = Field(None, min_length=10, max_length=20)
    department: Optional[str] = Field(None, min_length=2, max_length=100)
    designation: Optional[str] = Field(None, min_length=2, max_length=100)
    salary: Optional[float] = Field(None, gt=0)
    date_of_joining: Optional[datetime] = None
    status: Optional[str] = None
    
    @field_validator('mobile')
    @classmethod
    def validate_mobile(cls, v: Optional[str]) -> Optional[str]:
        """Validate mobile format if provided"""
        if v is None:
            return v
        mobile_pattern = r'^[+]?[0-9\-]{10,20}$'
        if not re.match(mobile_pattern, v):
            raise ValueError('Invalid mobile format (10-20 digits, may include + or -)')
        return v.replace(" ", "")
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        """Validate status field if provided"""
        if v is None:
            return v
        if v not in ["ACTIVE", "INACTIVE"]:
            raise ValueError('Status must be either ACTIVE or INACTIVE')
        return v.upper()


class EmployeeResponse(EmployeeBase):
    """Schema for employee response with additional fields"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
