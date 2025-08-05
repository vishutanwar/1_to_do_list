from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator, Field
from datetime import datetime, date
from typing import List, Optional, Annotated


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


task_dict = {}
app = FastAPI()



@app.get("/")
def home():
    return JSONResponse(status_code= 200, content={"message": "This is home Page this application is to perform CRUD operations on your To-Do list which means you can Create, Read, Update and Delete TO-DO Tasks"})


# I will be using dictonary to store data, where key will be the date and value is list of tasks for that day. 

#see all tasks:

@app.get("/tasks")
def date_task(date: str = Query(default=None, description = "Date in DD-MM-YYYY format")):
    if date:
        try:
            parsed_date = datetime.strptime(date, "%d-%m-%Y").date()
        except ValueError:
            return JSONResponse(
                status_code= 422, content={"error": "Invalid date formate, Use DD-MM-YYYY"}
            )

        if parsed_date not in task_dict:
            return JSONResponse(status_code=200, content={"message":f"No tasks found for {parsed_date}"})
        else:
            return task_dict[parsed_date] # list of to-do for that day
    else:
        if task_dict:  # if not empty.
            return task_dict
            
        else:
            return JSONResponse(status_code=200, content={"message":"No tasks exists"}) 



# to add task
@app.post("/tasks")
def create(task:Tasks):


    if task.date in task_dict.keys():
        task_dict[task.date].append(task.tasks)
    else:
        task_dict[task.date] = task.tasks
    
    return JSONResponse(status_code=201, content="Your Tasks added to TO-DO List")


# update task, it wil eb used to delete tasks, means remove tasks which are deleted
@app.put("/update")
def update(task:str, date:str):
    try:
        parsed_date = datetime.strptime(date, "%d-%m-%Y").date()
        task_dict[parsed_date].remove(task)
        return JSONResponse(status_code= 201, content={"message":"Task Removed"})
    except Exception as e:
        return JSONResponse(status_code=404, content={"error": str(e)})


# it will be used to delete the all tasks under a specific date!!
@app.delete("/delete")
def update(date: str):
    try:
        parsed_date = datetime.strptime(date, "%d-%m-%Y").date()
        
    except ValueError:
        return JSONResponse(
            status_code= 422, content={"error": "Invalid date formate, Use DD-MM-YYYY"}
        )
    del task_dict[parsed_date]
    return JSONResponse(status_code= 201, content={"message":f"All task from {parsed_date} are deleted"})


