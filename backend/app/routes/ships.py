# app/routes/ships.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.app.database import create_schemas as models
from backend.app.database import create_database as database_config
from backend.app import schemas
from backend.app.crud import ship_crud

router = APIRouter(
    prefix="/ships",
    tags=["Ships"],
)

def get_db():
    """
    Dependency to get the database session.
    """
    db = database_config.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.ShipResponse)
def create_ship_route(ship: schemas.ShipCreate, db: Session = Depends(get_db)):
    return ship_crud.create_ship(db=db, ship=ship)

@router.get("/", response_model=list[schemas.ShipResponse])
def list_ships_route(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ships = ship_crud.get_ships(db=db, skip=skip, limit=limit)
    return ships

@router.get("/{ship_id}", response_model=schemas.ShipResponse)
def get_ship_route(ship_id: int, db: Session = Depends(get_db)):
    db_ship = ship_crud.get_ship(db=db, ship_id=ship_id)
    if db_ship is None:
        raise HTTPException(status_code=404, detail="Ship not found")
    return db_ship

@router.put("/{ship_id}", response_model=schemas.ShipResponse)
def update_ship_route(ship_id: int, ship_data: schemas.ShipCreate, db: Session = Depends(get_db)):
    db_ship = ship_crud.update_ship(db=db, ship_id=ship_id, ship_data=ship_data)
    if db_ship is None:
        raise HTTPException(status_code=404, detail="Ship not found or update failed")
    return db_ship

@router.delete("/{ship_id}")
def delete_ship_route(ship_id: int, db: Session = Depends(get_db)):
    if not ship_crud.delete_ship(db=db, ship_id=ship_id):
        raise HTTPException(status_code=404, detail="Ship not found")
    return {"detail": "Ship deleted"}