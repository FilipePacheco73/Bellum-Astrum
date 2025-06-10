from fastapi import FastAPI
from app.routes import ships, users, market, seed
from app.database.create_database import engine, Base 

# Create all tables in the database
# This is useful if you want the application to create tables on startup
# If you prefer to manage table creation manually (e.g., with Alembic or a script),
# you might remove this or make it conditional.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Space Battle Game API",
    description="API for managing game resources like Ships and Users.",
    version="0.1.0"
)

app.include_router(seed.router, prefix="/api/v1") # Using seed.router as defined in seed.py
app.include_router(ships.router, prefix="/api/v1") # Using ships.router as defined in ships.py
app.include_router(users.router, prefix="/api/v1") # Using users.router as defined in users.py
app.include_router(market.router, prefix="/api/v1") # Using market.router as defined in market.py

@app.get("/")
async def root():
    return {"message": "Welcome to the Space Battle Game API!"}