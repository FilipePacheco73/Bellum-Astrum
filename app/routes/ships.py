from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app import models, database
from app.schemas import ShipCreate, ShipResponse

app = FastAPI()

# Dependência para obter a sessão do banco
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota: listar todas as naves
@app.get("/ships", response_model=list[ShipResponse])
def list_ships(db: Session = Depends(get_db)):
    return db.query(models.Ship).all()

# Rota: criar uma nova nave
@app.post("/ships", response_model=ShipResponse)
def create_ship(ship: ShipCreate, db: Session = Depends(get_db)):
    db_ship = models.Ship(**ship.dict())
    db.add(db_ship)
    db.commit()
    db.refresh(db_ship)
    return db_ship

# Rota: obter nave por ID
@app.get("/ships/{ship_id}", response_model=ShipResponse)
def get_ship(ship_id: int, db: Session = Depends(get_db)):
    ship = db.query(models.Ship).filter(models.Ship.id == ship_id).first()
    if not ship:
        raise HTTPException(status_code=404, detail="Ship not found")
    return ship

# Rota: atualizar nave
@app.put("/ships/{ship_id}", response_model=ShipResponse)
def update_ship(ship_id: int, ship_data: ShipCreate, db: Session = Depends(get_db)):
    ship = db.query(models.Ship).filter(models.Ship.id == ship_id).first()
    if not ship:
        raise HTTPException(status_code=404, detail="Ship not found")
    for key, value in ship_data.dict().items():
        setattr(ship, key, value)
    db.commit()
    db.refresh(ship)
    return ship

# Rota: deletar nave
@app.delete("/ships/{ship_id}")
def delete_ship(ship_id: int, db: Session = Depends(get_db)):
    ship = db.query(models.Ship).filter(models.Ship.id == ship_id).first()
    if not ship:
        raise HTTPException(status_code=404, detail="Ship not found")
    db.delete(ship)
    db.commit()
    return {"detail": "Ship deleted"}
