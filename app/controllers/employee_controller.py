from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse

router = APIRouter(prefix="/api/employees", tags=["employees"])


@router.post(
    "/",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new employee"
)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    """Create a new employee"""
    # Check for existing email
    existing_email = db.query(Employee).filter(Employee.email == employee.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail=f"Employee with email '{employee.email}' already exists")

    # Check for existing mobile
    existing_mobile = db.query(Employee).filter(Employee.mobile == employee.mobile).first()
    if existing_mobile:
        raise HTTPException(status_code=400, detail=f"Employee with mobile '{employee.mobile}' already exists")

    # Create new employee
    db_employee = Employee(**employee.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)

    return EmployeeResponse.model_validate(db_employee)


@router.get(
    "/",
    response_model=List[EmployeeResponse],
    summary="Get all employees"
)
def get_all_employees(
    skip: int = 0,
    limit: int = 100,
    department: Optional[str] = None,
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all employees with optional filtering"""
    query = db.query(Employee)

    if department:
        query = query.filter(Employee.department.ilike(f"%{department}%"))

    if status_filter:
        query = query.filter(Employee.status == status_filter.upper())

    employees = query.offset(skip).limit(limit).all()

    return [EmployeeResponse.model_validate(emp) for emp in employees]


@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse,
    summary="Get employee by ID"
)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    """Get a specific employee by ID"""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()

    if not employee:
        raise HTTPException(status_code=404, detail=f"Employee with ID {employee_id} not found")

    return EmployeeResponse.model_validate(employee)


@router.put(
    "/{employee_id}",
    response_model=EmployeeResponse,
    summary="Update employee"
)
def update_employee(employee_id: int, employee_data: EmployeeUpdate, db: Session = Depends(get_db)):
    """Update an existing employee"""
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail=f"Employee with ID {employee_id} not found")

    # Check for duplicate email if being updated
    if employee_data.email and employee_data.email != db_employee.email:
        existing_email = db.query(Employee).filter(Employee.email == employee_data.email).first()
        if existing_email:
            raise HTTPException(status_code=400, detail=f"Employee with email '{employee_data.email}' already exists")

    # Check for duplicate mobile if being updated
    if employee_data.mobile and employee_data.mobile != db_employee.mobile:
        existing_mobile = db.query(Employee).filter(Employee.mobile == employee_data.mobile).first()
        if existing_mobile:
            raise HTTPException(status_code=400, detail=f"Employee with mobile '{employee_data.mobile}' already exists")

    # Update only provided fields
    update_data = employee_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            setattr(db_employee, field, value)

    db.commit()
    db.refresh(db_employee)

    return EmployeeResponse.model_validate(db_employee)


@router.delete(
    "/{employee_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete employee"
)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    """Delete an employee"""
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail=f"Employee with ID {employee_id} not found")

    db.delete(db_employee)
    db.commit()

    return {"message": f"Employee with ID {employee_id} deleted successfully", "id": employee_id}