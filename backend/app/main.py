from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from backend.app.routes import ships, users, market, battle, logs, shipyard, work
from backend.app.database import shutdown_database, check_database_health, init_database
from backend.app.version import get_cached_version, get_project_info

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for FastAPI application.
    Manages database initialization and cleanup.
    """
    # Startup - initialize database tables
    init_database()
    yield
    # Shutdown
    shutdown_database()

# Get dynamic project information
project_info = get_project_info()

app = FastAPI(
    title=project_info["api_title"],
    description=project_info["description"],
    version=project_info["version"],
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ships.router, prefix="/api/v1") # Using ships.router as defined in ships.py
app.include_router(users.router, prefix="/api/v1") # Using users.router as defined in users.py
app.include_router(market.router, prefix="/api/v1") # Using market.router as defined in market.py
app.include_router(battle.router, prefix="/api/v1")  # Using battle.router as defined in battle.py
app.include_router(shipyard.router, prefix="/api/v1")  # Using shipyard.router as defined in shipyard.py
app.include_router(logs.router, prefix="/api/v1")  # Using logs.router as defined in logs.py
app.include_router(work.router, prefix="/api/v1")  # Using work.router as defined in work.py


@app.get("/")
async def root():
    return {
        "message": f"Welcome to the {project_info['name']} API!",
        "version": project_info["version"],
        "author": project_info["author"]
    }

@app.get("/version")
async def get_version():
    """Version information endpoint"""
    return project_info

@app.get("/health")
async def health_check():
    """Health check endpoint to verify API and database status"""
    db_health = check_database_health()
    return {
        "status": "healthy" if db_health["status"] == "healthy" else "unhealthy",
        "api": "running",
        "version": project_info["version"],
        "database": db_health
    }