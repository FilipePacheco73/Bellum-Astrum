from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from backend.app.routes import ships, users, market, battle, logs, shipyard, work
from database import shutdown_database, check_database_health

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for FastAPI application.
    Manages database cleanup on shutdown.
    """
    # Startup - database is managed separately via setup.py scripts
    yield
    # Shutdown
    shutdown_database()

app = FastAPI(
    title="Space Battle Game API",
    description="API for managing game resources like Ships and Users with enhanced database management.",
    version="0.3.0",
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
    return {"message": "Welcome to the Space Battle Game API!"}

@app.get("/health")
async def health_check():
    """Health check endpoint to verify API and database status"""
    db_healthy = check_database_health()
    return {
        "status": "healthy" if db_healthy else "unhealthy",
        "api": "running",
        "database": "connected" if db_healthy else "disconnected"
    }