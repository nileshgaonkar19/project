from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from . import models, crud, schemas
from .database import engine, SessionLocal
from fastapi import Query

#create table
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/") 
async def working():
    return {"Message": "Its Working!!"}

@app.get("/users", response_model=schemas.paginated_user_response)
async def get_users(
    pageno: int = Query(..., gt=0, description="Page number must be greater than 0"),
    pagesize: int = Query(..., gt=0, le=100, description="Page size must be between 1 and 100"),
    name: str = Query(None, description="Optional name filter"),
    db: Session = Depends(get_db)
):
    offset = (pageno - 1) * pagesize
    return crud.get_users(db, of=offset, limit=pagesize, name=name)
