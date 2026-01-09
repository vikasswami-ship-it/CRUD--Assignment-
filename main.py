from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import create_tables
from app.controllers.employee_controller import router as employee_router
from app.controllers.analytics_controller import router as analytics_router

# Application startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown"""
    # Startup
    print("Starting up...")
    create_tables()
    print("Database tables created/verified")
    yield
    # Shutdown
    print("Shutting down...")


# Create FastAPI application
app = FastAPI(
    title="Employee Management & Analytics API",
    description="REST API for employee management with analytics",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers
app.include_router(employee_router)
app.include_router(analytics_router)


# Health check endpoint
@app.get("/health", summary="Health check")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Employee Management API is running"}


# Root endpoint
@app.get("/", summary="API Information")
def root():
    """Root endpoint with API information"""
    return {
        "name": "Employee Management & Analytics API",
        "version": "1.0.0",
        "description": "REST API for employee management with analytics",
        "endpoints": {
            "health": "/health",
            "employees_crud": "/api/employees",
            "analytics": "/api/analytics"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
