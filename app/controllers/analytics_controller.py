from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.employee import Employee
from app.schemas.employee import EmployeeResponse

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get(
    "/employees-per-department",
    summary="Employees per department"
)
def get_employees_per_department(db: Session = Depends(get_db)):
    """Get total employees and details grouped by department"""
    try:
        # Get employees grouped by department with stats
        result = db.query(
            Employee.department,
            func.count(Employee.id).label('total_employees'),
            func.avg(Employee.salary).label('average_salary'),
            func.min(Employee.salary).label('min_salary'),
            func.max(Employee.salary).label('max_salary')
        ).group_by(Employee.department).all()

        departments = []
        for dept in result:
            # Get employees in this department
            employees = db.query(Employee).filter(Employee.department == dept.department).all()

            departments.append({
                "department": dept.department,
                "total_employees": dept.total_employees,
                "average_salary": round(float(dept.average_salary), 2) if dept.average_salary else 0,
                "min_salary": float(dept.min_salary) if dept.min_salary else 0,
                "max_salary": float(dept.max_salary) if dept.max_salary else 0,
                "employees": [EmployeeResponse.model_validate(emp) for emp in employees]
            })

        return {"departments": departments}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting department analytics: {str(e)}")


@router.get(
    "/salary-extremes-per-department",
    summary="Highest and lowest salaried employees per department"
)
def get_salary_extremes(db: Session = Depends(get_db)):
    """Get the highest and lowest paid employees for each department"""
    try:
        departments = db.query(Employee.department).distinct().all()

        result = []
        for dept in departments:
            dept_name = dept[0]

            # Get highest paid employee in department
            highest = db.query(Employee).filter(
                Employee.department == dept_name
            ).order_by(Employee.salary.desc()).first()

            # Get lowest paid employee in department
            lowest = db.query(Employee).filter(
                Employee.department == dept_name
            ).order_by(Employee.salary.asc()).first()

            result.append({
                "department": dept_name,
                "highest_paid": EmployeeResponse.model_validate(highest) if highest else None,
                "lowest_paid": EmployeeResponse.model_validate(lowest) if lowest else None
            })

        return {"departments": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting salary extremes: {str(e)}")


@router.get(
    "/average-salary-per-department",
    summary="Average salary per department"
)
def get_average_salary(db: Session = Depends(get_db)):
    """Get the average salary for each department"""
    try:
        result = db.query(
            Employee.department,
            func.avg(Employee.salary).label('average_salary'),
            func.count(Employee.id).label('employee_count')
        ).group_by(Employee.department).order_by(func.avg(Employee.salary).desc()).all()

        return {
            "departments": [
                {
                    "department": dept.department,
                    "average_salary": round(float(dept.average_salary), 2) if dept.average_salary else 0,
                    "employee_count": dept.employee_count
                }
                for dept in result
            ]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting average salaries: {str(e)}")


@router.get(
    "/active-vs-inactive",
    summary="Active vs inactive employees"
)
def get_active_vs_inactive(db: Session = Depends(get_db)):
    """Get count and details of active and inactive employees"""
    try:
        total_count = db.query(Employee).count()

        if total_count == 0:
            return {
                "total": 0,
                "active": {"count": 0, "percentage": 0, "employees": []},
                "inactive": {"count": 0, "percentage": 0, "employees": []}
            }

        active_employees = db.query(Employee).filter(Employee.status == "ACTIVE").all()
        inactive_employees = db.query(Employee).filter(Employee.status == "INACTIVE").all()

        active_count = len(active_employees)
        inactive_count = len(inactive_employees)

        return {
            "total": total_count,
            "active": {
                "count": active_count,
                "percentage": round((active_count / total_count) * 100, 2),
                "employees": [EmployeeResponse.model_validate(emp) for emp in active_employees]
            },
            "inactive": {
                "count": inactive_count,
                "percentage": round((inactive_count / total_count) * 100, 2),
                "employees": [EmployeeResponse.model_validate(emp) for emp in inactive_employees]
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting active/inactive stats: {str(e)}")


@router.get(
    "/employees-by-designation",
    summary="Employees sorted by designation"
)
def get_employees_by_designation(db: Session = Depends(get_db)):
    """Get all employees grouped and sorted by designation"""
    try:
        designations = db.query(Employee.designation).distinct().all()

        result = []
        for designation in designations:
            designation_name = designation[0]
            employees = db.query(Employee).filter(Employee.designation == designation_name).all()

            result.append({
                "designation": designation_name,
                "count": len(employees),
                "employees": [EmployeeResponse.model_validate(emp) for emp in employees]
            })

        return {"designations": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting designation analytics: {str(e)}")


@router.get(
    "/comprehensive",
    summary="Comprehensive analytics"
)
def get_comprehensive_analytics(db: Session = Depends(get_db)):
    """Get a comprehensive analytics report"""
    try:
        total_employees = db.query(Employee).count()
        total_salary = db.query(func.sum(Employee.salary)).scalar() or 0
        avg_salary = db.query(func.avg(Employee.salary)).scalar() or 0

        # Department stats
        dept_stats = db.query(
            func.count(Employee.id).label('total_departments')
        ).distinct(Employee.department).count()

        return {
            "summary": {
                "total_employees": total_employees,
                "total_departments": dept_stats,
                "total_salary": float(total_salary),
                "average_salary": round(float(avg_salary), 2) if avg_salary else 0
            },
            "status_breakdown": get_active_vs_inactive(db),
            "department_breakdown": get_employees_per_department(db),
            "salary_analysis": get_average_salary(db)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting comprehensive analytics: {str(e)}")
