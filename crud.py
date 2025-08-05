from sqlalchemy.orm import Session
from database import Task

def get_tasks(db: Session):
    return db.query(Task).all()
