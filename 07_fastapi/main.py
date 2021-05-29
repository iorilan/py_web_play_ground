from typing import List
import uvicorn
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException


from app import schemas, crud, models
from app.database import engine, SessionLocal
from fastapi.responses import JSONResponse
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.post("/todo", response_model=schemas.TODOInfo, status_code=201)
def create_todo(todo: schemas.TODOCreate, db: Session = Depends(get_db)):
    exist_todo = crud.get_todo_by(db, todo.title)
    if exist_todo:
        return JSONResponse(status_code=409, content={"message": "Same name already exists"})
    return crud.create_todo(db=db, entity=todo)

@app.get("/all", response_model=List[schemas.TODOInfo], status_code=200)
def get_all(db: Session = Depends(get_db)):
    return crud.get_all(db=db)

@app.put("/todo/{id}", response_model=schemas.TODOInfo, status_code=200)
def update_a_todo(id: int, todo_data: schemas.TODOUpdate, db: Session = Depends(get_db)):
    todo = crud.get_todo(db, id)
    if not todo:
        return JSONResponse(status_code=422, content={"message": "Item not found"})
    crud.update_todo(db, id, todo_data)
    updated_todo = crud.get_todo(db, id)
    return updated_todo

@app.delete("/todo/{id}", status_code=204)
def delete_a_todo(id: int, db: Session = Depends(get_db)):
    todo = crud.get_todo(db, id)
    if not todo:
        return JSONResponse(status_code=422, content={"message": "Item not found"})
    crud.delete_todo(db, id)
    return 

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8081)