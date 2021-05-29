from sqlalchemy.orm import Session

from .models import TODO
from .schemas import TODOCreate, TODOInfo, TODOUpdate
import time

def get_all(db: Session):
    return db.query(TODO).all()

def get_todo(db: Session, id: int):
    return db.query(TODO).filter(TODO.id == id).first()

def get_todo_by(db: Session, title: str):
    return db.query(TODO).filter(TODO.title == title).first()

def create_todo(db: Session, entity: TODOCreate):
    todo = TODO(desc=entity.desc, created_at=time.time(), title=entity.title)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

def delete_todo(db: Session, id: int):
    todo = db.query(TODO).filter(TODO.id == id).first()
    db.delete(todo)
    db.commit()

def update_todo(db: Session, id:int, todo_data: TODOUpdate):
    todo = db.query(TODO).filter(TODO.id == id).first()
    todo.desc = todo_data.desc
    todo.title = todo_data.title
    db.commit()
    db.refresh(todo)