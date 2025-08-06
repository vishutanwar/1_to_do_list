from fastapi import FastAPI, HTTPException, Path, Query, Depends, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator, Field
from datetime import datetime, date
from typing import List, Optional, Annotated
from sqlalchemy.orm import Session

from database import get_db, Task as TaskModel
from schemas import TaskCreate, TaskResponse

class Tasks(BaseModel):
    date: date
    tasks: List[str]

    @field_validator("date", mode="before")  # before means first it will be processed before assigning to date variable
    def parce_custom_date(cls, value):
        try:
            return datetime.strptime(value, "%d-%m-%Y").date()
        except ValueError:
            raise ValueError("Date must be in DD-MM-YYYY format")

        
class Day(BaseModel):
    date: Annotated[Optional[str], Field(default=None)]

    @field_validator("date", mode="before")  # before means first it will be processed before assigning to date variable
    def parce_custom_date(cls, value):
        try:
            return datetime.strptime(value, "%d-%m-%Y").date()
        except ValueError:
            raise ValueError("Date must be in DD-MM-YYYY format")


app = FastAPI()



@app.get("/")
def home():
    return JSONResponse(status_code= 200, content={"message": "This is home Page this application is to perform CRUD operations on your To-Do list which means you can Create, Read, Update and Delete TO-DO Tasks"})


# I will be using dictonary to store data, where key will be the date and value is list of tasks for that day. 

#see all tasks:

@app.get("/tasks", response_model=List[TaskResponse])
def get_tasks(date: Optional[str] = Query(default=None, description="Date in DD-MM-YYYY format"), db: Session = Depends(get_db)):
    query = db.query(TaskModel)

    if date:
        try:
            parsed_date = datetime.strptime(date, "%d-%m-%Y").date()
        except ValueError:
            raise HTTPException(status_code=422, detail="Invalid date format. Use DD-MM-YYYY")
        
        query = query.filter(TaskModel.date == parsed_date)

    tasks = query.all()

    if not tasks:
        return []

    return tasks



# to add task
@app.post("/tasks", response_model=TaskResponse)
def create(task:TaskCreate, db: Session = Depends(get_db)):
    try:
        db_task = TaskModel(
            date=task.date,
            title=task.title,
            description=task.description
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)

        return JSONResponse(status_code=201, content="Your Tasks added to TO-DO List")

    except Exception as e:
        print(f"Error while creating task: {e}")
        raise HTTPException(status_code=500, detail="Something went wrong while creating task.")


# update task, it wil eb used to delete tasks, means remove tasks which are deleted
@app.put("/update")
def remove_task(title: str = Body(...), date: date = Body(...), db: Session = Depends(get_db)):
    try:
        task = db.query(TaskModel).filter(TaskModel.date == date, TaskModel.title == title).first()

        if not task:
            raise HTTPException(status_code=404, detail="Task not found with the given date and title.")

        db.delete(task)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Task removed successfully."})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error removing task: {str(e)}")


# it will be used to delete the all tasks under a specific date!!
@app.delete("/delete")
def delete_tasks_by_date(date: date = Query(...), db: Session = Depends(get_db)):
    try:
        tasks = db.query(TaskModel).filter(TaskModel.date == date).all()

        if not tasks:
            raise HTTPException(status_code=404, detail=f"No tasks found on {date}")

        for task in tasks:
            db.delete(task)
        db.commit()

        return JSONResponse(status_code=200, content={"message": f"All tasks on {date} deleted successfully."})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting tasks: {str(e)}")

