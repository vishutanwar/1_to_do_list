from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, FutureDate
from datetime import datetime
from typing import List, Annotated


class Tasks(BaseModel):
    date: FutureDate = Field(..., title="Date of tasks", description="Date under which Tasks Exists")
    tasks: List[str] = Field(..., title="List of tasks", description=" This is list of tasks that needs to complete")


class Date(BaseModel):
    date: Annotated[FutureDate, Field(..., title="Date of tasks", description="Date under which Tasks Exists")]

task_dict = {}
app = FastAPI()

# function to check is the date is valid or not !!
# def is_valid_date(date: str):
#     try:
#         datetime.strptime(date, "%d/%m/%Y")
#         return True
#     except:
#         False


@app.get("/")
def home():
    return JSONResponse(status_code= 200, content={"message": "This is home Page this application is to perform CRUD operations on your To-Do list which means you can Create, Read, Update and Delete TO-DO Tasks"})
    # return "This is home Page\nthis application is to perform CRUD operations on your To-Do list which means you can Create, Read, Update and Delete TO-DO Tasks"

# I will be using dictonary to store data, where key will be the date and value is list of tasks for that day. 

#see all tasks:

@app.get("/list_task")
def date_task(date: Date = Path(description= "This is date it is used as path Parimiter")):
    if date:
        # if not is_valid_date(date):
        #     raise HTTPException(status_code=400, detail="Date is not in Valid formate, add DD/MM/YYYY, formate")

        if date not in task_dict:
            return JSONResponse(status_code=200, content={"message":f"We do not have any Tasks for {date}"})
        else:
            return task_dict[date] # list of to-do for that day
    else:
        if task_dict:  # if not empty
            return task_dict
            
        else:
            return JSONResponse(status_code=200, content={"message":"No tasks exists"}) 



# to add task
@app.post("/create")
def create(task:Tasks):
    # if not is_valid_date(task.date):
    #     raise HTTPException(status_code=400, detail="Date is not in Valid formate, add DD/MM/YYYY, formate")


    if task.date in task_dict.keys():
        task_dict[task.date].append(task.tasks)
    else:
        task_dict[task.date] = task.tasks
    
    return JSONResponse(status_code=201, content="Your Tasks added to TO-DO List")



@app.put("/update")
def update(task: Tasks):
    task_dict[task.date].remove(task.tasks)
    return JSONResponse(status_code= 201, content={"message":"Task Removed"})

@app.delete("/delete")
def update(date: Date):
    del task_dict[date.date]
    return JSONResponse(status_code= 201, content={"message":f"All task from {date.date} are deleted"})


