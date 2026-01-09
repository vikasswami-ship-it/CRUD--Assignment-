# Employee Management & Analytics API

A comprehensive REST API built with FastAPI for managing employee data with advanced analytics capabilities.

## Features

- Complete CRUD operations for employee management
- Advanced analytics and reporting
- Department-wise insights
- Salary analytics
- Status tracking (Active/Inactive)
- Input validation and error handling

## Tech Stack

- **FastAPI** - Modern web framework for building APIs
- **SQLAlchemy** - SQL toolkit and ORM
- **PostgreSQL** - Database
- **Pydantic** - Data validation
- **Python 3.8+**

## Setup

1. Clone the repository:
```bash
git clone https://github.com/vikasswami-ship-it/CRUD--Assignment-.git
cd CRUD--Assignment-
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

4. Update database credentials in `.env`

5. Run the application:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## API Endpoints

### Health Check

#### Get API Health Status
- **Endpoint:** `/health`
- **Method:** `GET`
- **Description:** Check if the API is running
- **Example Request:**
```bash
curl http://localhost:8000/health
```
- **Example Response:**
```json
{
  "status": "healthy",
  "message": "Employee Management API is running"
}
```

---

## Employee Management Endpoints

### 1. Create Employee
- **Endpoint:** `/api/employees/`
- **Method:** `POST`
- **Description:** Create a new employee record
- **Example Request:**
```bash
curl -X POST "http://localhost:8000/api/employees/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "mobile": "1234567890",
    "department": "Engineering",
    "designation": "Software Engineer",
    "salary": 75000,
    "status": "ACTIVE"
  }'
```
- **Example Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john.doe@example.com",
  "mobile": "1234567890",
  "department": "Engineering",
  "designation": "Software Engineer",
  "salary": 75000.0,
  "status": "ACTIVE",
  "created_at": "2026-01-09T10:30:00",
  "updated_at": "2026-01-09T10:30:00"
}
```

### 2. Get All Employees
- **Endpoint:** `/api/employees/`
- **Method:** `GET`
- **Description:** Retrieve all employees with optional filtering
- **Query Parameters:**
  - `skip` (optional): Number of records to skip (default: 0)
  - `limit` (optional): Maximum records to return (default: 100)
  - `department` (optional): Filter by department name
  - `status_filter` (optional): Filter by status (ACTIVE/INACTIVE)
- **Example Request:**
```bash
curl "http://localhost:8000/api/employees/?department=Engineering&status_filter=ACTIVE"
```
- **Example Response:**
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com",
    "mobile": "1234567890",
    "department": "Engineering",
    "designation": "Software Engineer",
    "salary": 75000.0,
    "status": "ACTIVE",
    "created_at": "2026-01-09T10:30:00",
    "updated_at": "2026-01-09T10:30:00"
  }
]
```

### 3. Get Employee by ID
- **Endpoint:** `/api/employees/{employee_id}`
- **Method:** `GET`
- **Description:** Retrieve a specific employee by their ID
- **Example Request:**
```bash
curl "http://localhost:8000/api/employees/1"
```
- **Example Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john.doe@example.com",
  "mobile": "1234567890",
  "department": "Engineering",
  "designation": "Software Engineer",
  "salary": 75000.0,
  "status": "ACTIVE",
  "created_at": "2026-01-09T10:30:00",
  "updated_at": "2026-01-09T10:30:00"
}
```

### 4. Update Employee
- **Endpoint:** `/api/employees/{employee_id}`
- **Method:** `PUT`
- **Description:** Update an existing employee record (partial updates supported)
- **Example Request:**
```bash
curl -X PUT "http://localhost:8000/api/employees/1" \
  -H "Content-Type: application/json" \
  -d '{
    "salary": 85000,
    "designation": "Senior Software Engineer"
  }'
```
- **Example Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john.doe@example.com",
  "mobile": "1234567890",
  "department": "Engineering",
  "designation": "Senior Software Engineer",
  "salary": 85000.0,
  "status": "ACTIVE",
  "created_at": "2026-01-09T10:30:00",
  "updated_at": "2026-01-09T11:15:00"
}
```

### 5. Delete Employee
- **Endpoint:** `/api/employees/{employee_id}`
- **Method:** `DELETE`
- **Description:** Delete an employee record
- **Example Request:**
```bash
curl -X DELETE "http://localhost:8000/api/employees/1"
```
- **Example Response:**
```json
{
  "message": "Employee with ID 1 deleted successfully",
  "id": 1
}
```

---

## Analytics Endpoints

### 6. Employees Per Department
- **Endpoint:** `/api/analytics/employees-per-department`
- **Method:** `GET`
- **Description:** Get employee count and statistics grouped by department, including all employee details
- **Example Request:**
```bash
curl "http://localhost:8000/api/analytics/employees-per-department"
```
- **Example Response:**
```json
{
  "departments": [
    {
      "department": "Engineering",
      "total_employees": 5,
      "average_salary": 78000.0,
      "min_salary": 65000.0,
      "max_salary": 95000.0,
      "employees": [
        {
          "id": 1,
          "name": "John Doe",
          "email": "john.doe@example.com",
          "mobile": "1234567890",
          "department": "Engineering",
          "designation": "Software Engineer",
          "salary": 75000.0,
          "status": "ACTIVE",
          "created_at": "2026-01-09T10:30:00",
          "updated_at": "2026-01-09T10:30:00"
        }
      ]
    }
  ]
}
```

### 7. Salary Extremes Per Department
- **Endpoint:** `/api/analytics/salary-extremes-per-department`
- **Method:** `GET`
- **Description:** Get the highest and lowest paid employees for each department
- **Example Request:**
```bash
curl "http://localhost:8000/api/analytics/salary-extremes-per-department"
```
- **Example Response:**
```json
{
  "departments": [
    {
      "department": "Engineering",
      "highest_paid": {
        "id": 2,
        "name": "Jane Smith",
        "email": "jane.smith@example.com",
        "mobile": "9876543210",
        "department": "Engineering",
        "designation": "Tech Lead",
        "salary": 95000.0,
        "status": "ACTIVE",
        "created_at": "2026-01-09T10:30:00",
        "updated_at": "2026-01-09T10:30:00"
      },
      "lowest_paid": {
        "id": 3,
        "name": "Bob Wilson",
        "email": "bob.wilson@example.com",
        "mobile": "5551234567",
        "department": "Engineering",
        "designation": "Junior Developer",
        "salary": 65000.0,
        "status": "ACTIVE",
        "created_at": "2026-01-09T10:30:00",
        "updated_at": "2026-01-09T10:30:00"
      }
    }
  ]
}
```

### 8. Average Salary Per Department
- **Endpoint:** `/api/analytics/average-salary-per-department`
- **Method:** `GET`
- **Description:** Get the average salary for each department with employee count
- **Example Request:**
```bash
curl "http://localhost:8000/api/analytics/average-salary-per-department"
```
- **Example Response:**
```json
{
  "departments": [
    {
      "department": "Engineering",
      "average_salary": 78000.0,
      "employee_count": 5
    },
    {
      "department": "HR",
      "average_salary": 55000.0,
      "employee_count": 3
    }
  ]
}
```

### 9. Active vs Inactive Employees
- **Endpoint:** `/api/analytics/active-vs-inactive`
- **Method:** `GET`
- **Description:** Get count and details of active and inactive employees with percentages
- **Example Request:**
```bash
curl "http://localhost:8000/api/analytics/active-vs-inactive"
```
- **Example Response:**
```json
{
  "total": 10,
  "active": {
    "count": 8,
    "percentage": 80.0,
    "employees": [
      {
        "id": 1,
        "name": "John Doe",
        "email": "john.doe@example.com",
        "mobile": "1234567890",
        "department": "Engineering",
        "designation": "Software Engineer",
        "salary": 75000.0,
        "status": "ACTIVE",
        "created_at": "2026-01-09T10:30:00",
        "updated_at": "2026-01-09T10:30:00"
      }
    ]
  },
  "inactive": {
    "count": 2,
    "percentage": 20.0,
    "employees": [...]
  }
}
```

### 10. Employees by Designation
- **Endpoint:** `/api/analytics/employees-by-designation`
- **Method:** `GET`
- **Description:** Get all employees grouped and sorted by designation
- **Example Request:**
```bash
curl "http://localhost:8000/api/analytics/employees-by-designation"
```
- **Example Response:**
```json
{
  "designations": [
    {
      "designation": "Software Engineer",
      "count": 4,
      "employees": [
        {
          "id": 1,
          "name": "John Doe",
          "email": "john.doe@example.com",
          "mobile": "1234567890",
          "department": "Engineering",
          "designation": "Software Engineer",
          "salary": 75000.0,
          "status": "ACTIVE",
          "created_at": "2026-01-09T10:30:00",
          "updated_at": "2026-01-09T10:30:00"
        }
      ]
    }
  ]
}
```

### 11. Comprehensive Analytics
- **Endpoint:** `/api/analytics/comprehensive`
- **Method:** `GET`
- **Description:** Get a comprehensive analytics report with summary, status breakdown, department breakdown, and salary analysis
- **Example Request:**
```bash
curl "http://localhost:8000/api/analytics/comprehensive"
```
- **Example Response:**
```json
{
  "summary": {
    "total_employees": 10,
    "total_departments": 3,
    "total_salary": 650000.0,
    "average_salary": 65000.0
  },
  "status_breakdown": {
    "total": 10,
    "active": {
      "count": 8,
      "percentage": 80.0,
      "employees": [...]
    },
    "inactive": {
      "count": 2,
      "percentage": 20.0,
      "employees": [...]
    }
  },
  "department_breakdown": {
    "departments": [...]
  },
  "salary_analysis": {
    "departments": [...]
  }
}
```

---

## Data Validation

### Employee Schema

**Required Fields:**
- `name` (string, 2-100 characters)
- `email` (valid email format, unique)
- `mobile` (10 digits, unique)
- `department` (string, 2-50 characters)
- `designation` (string, 2-50 characters)
- `salary` (positive number)
- `status` (ACTIVE or INACTIVE)

**Auto-generated Fields:**
- `id` (integer, auto-increment)
- `created_at` (timestamp)
- `updated_at` (timestamp)

---

## Error Handling

The API returns appropriate HTTP status codes:

- `200` - Success
- `201` - Created
- `400` - Bad Request (validation errors, duplicate entries)
- `404` - Not Found
- `500` - Internal Server Error

**Example Error Response:**
```json
{
  "detail": "Employee with email 'john.doe@example.com' already exists"
}
```

---

## Database Schema

### Employee Table
```sql
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    mobile VARCHAR(10) UNIQUE NOT NULL,
    department VARCHAR(50) NOT NULL,
    designation VARCHAR(50) NOT NULL,
    salary NUMERIC(10, 2) NOT NULL,
    status VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```


## Author

Vikas Swami
