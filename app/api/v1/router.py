"""API v1 router - Aggregates all v1 endpoints."""

from fastapi import APIRouter

from app.api.v1.auth.router import router as auth_router

# Create main v1 router
api_v1_router = APIRouter()

# Include sub-routers
api_v1_router.include_router(auth_router)

# Future routers:
# api_v1_router.include_router(consultations_router)
# api_v1_router.include_router(my_router)
