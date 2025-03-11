from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import teams, services, runtime_components, search

# Create FastAPI app
app = FastAPI(
    title="WOW - Who Owns What",
    description="API for querying software services ownership by DevOps teams",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(teams.router)
app.include_router(services.router)
app.include_router(runtime_components.router)
app.include_router(search.router)

@app.get("/")
async def root():
    return {"message": "Welcome to WOW API - Who Owns What"}
