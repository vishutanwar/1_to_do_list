from pydantic import BaseModel
from datetime import date
from typing import Optional

class TaskCreate(BaseModel):
    title: str
    description: str = ""
    date: date

class TaskUpdate(BaseModel):
    title: str
    description: str
    status: bool

class TaskResponse(BaseModel):
    id: int
    title:str
    description:Optional[str]
    date: date


    class Config:
        from_attributes = True
