"""RepairHub FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, tickets, customers, inventory
from app.core.config import settings

app = FastAPI(
    title="RepairHub API",
    description="Multi-location electronics repair CRM + POS + inventory management",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(tickets.router, prefix="/api/v1/tickets", tags=["tickets"])
app.include_router(customers.router, prefix="/api/v1/customers", tags=["customers"])
app.include_router(inventory.router, prefix="/api/v1/inventory", tags=["inventory"])


@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}


@app.get("/")
async def root():
    """Root endpoint redirect to docs."""
    return {"message": "Welcome to RepairHub API", "docs": "/api/v1/docs"}
