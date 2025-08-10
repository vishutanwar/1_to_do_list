# API Documentation for Todo List Application

## Base URL
```
http://localhost:8000
```

## Authentication
All protected endpoints require an API key in the request header:
```
X-API-Key: your_api_key_here
```

## Endpoints Overview

| Method | Endpoint | Description | Authentication Required |
|--------|----------|-------------|------------------------|
| GET | `/` | Home page | ❌ No |
| GET | `/tasks` | Get all tasks or filter by date | ❌ No |
| POST | `/tasks` | Create a new task | ✅ Yes |
| PUT | `/update` | Delete a specific task | ✅ Yes |
| DELETE | `/delete` | Delete all tasks for a specific date | ✅ Yes |

---

## 1. Home Page
**GET** `/`

### Description
Returns a welcome message about the application.

### Request
```bash
curl http://localhost:8000/
```

### Response
```json
{
  "message": "This is home Page this application is to perform CRUD operations on your To-Do list which means you can Create, Read, Update and Delete TO-DO Tasks"
}
```

---

## 2. Get Tasks
**GET** `/tasks`

### Description
Retrieve all tasks or filter tasks by a specific date.

### Parameters
| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `date` | string | ❌ No | Date in DD-MM-YYYY format | "25-12-2024" |

### Request Examples

#### Get all tasks:
```bash
curl http://localhost:8000/tasks
```

#### Get tasks for a specific date:
```bash
curl http://localhost:8000/tasks?date=25-12-2024
```

### Response Examples

#### Success (with tasks):
```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, bread, eggs",
    "date": "2024-12-25"
  },
  {
    "id": 2,
    "title": "Call mom",
    "description": "Wish her happy birthday",
    "date": "2024-12-25"
  }
]
```

#### Success (no tasks):
```json
[]
```

#### Error (invalid date format):
```json
{
  "detail": "Invalid date format. Use DD-MM-YYYY"
}
```

---

## 3. Create Task
**POST** `/tasks`

### Description
Create a new task in the todo list.

### Authentication
✅ **Required**: Include API key in header
```
X-API-Key: your_api_key_here
```

### Request Body
```json
{
  "title": "Task title",
  "description": "Task description (optional)",
  "date": "2024-12-25"
}
```

### Request Example
```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key_here" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, bread, eggs",
    "date": "2024-12-25"
  }'
```

### Response Examples

#### Success:
```json
{
  "id": 3,
  "title": "Buy groceries",
  "description": "Milk, bread, eggs",
  "date": "2024-12-25"
}
```

#### Error (unauthorized):
```json
{
  "detail": "Invalid API key"
}
```

#### Error (server error):
```json
{
  "detail": "Something went wrong while creating task."
}
```

---

## 4. Delete Specific Task
**PUT** `/update`

### Description
Delete a specific task by title and date.

### Authentication
✅ **Required**: Include API key in header
```
X-API-Key: your_api_key_here
```

### Request Body
```json
{
  "title": "Task title to delete",
  "date": "2024-12-25"
}
```

### Request Example
```bash
curl -X PUT http://localhost:8000/update \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key_here" \
  -d '{
    "title": "Buy groceries",
    "date": "2024-12-25"
  }'
```

### Response Examples

#### Success:
```json
{
  "message": "Task removed successfully."
}
```

#### Error (task not found):
```json
{
  "detail": "Task not found with the given date and title."
}
```

#### Error (unauthorized):
```json
{
  "detail": "Invalid API key"
}
```

---

## 5. Delete All Tasks for a Date
**DELETE** `/delete`

### Description
Delete all tasks for a specific date.

### Authentication
✅ **Required**: Include API key in header
```
X-API-Key: your_api_key_here
```

### Parameters
| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `date` | date | ✅ Yes | Date in YYYY-MM-DD format | "2024-12-25" |

### Request Example
```bash
curl -X DELETE "http://localhost:8000/delete?date=2024-12-25" \
  -H "X-API-Key: your_api_key_here"
```

### Response Examples

#### Success:
```json
{
  "message": "All tasks on 2024-12-25 deleted successfully."
}
```

#### Error (no tasks found):
```json
{
  "detail": "No tasks found on 2024-12-25"
}
```

#### Error (unauthorized):
```json
{
  "detail": "Invalid API key"
}
```

---

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 201 | Created (for POST requests) |
| 401 | Unauthorized (invalid API key) |
| 404 | Not found |
| 422 | Validation error (invalid date format) |
| 500 | Server error |

---

## Date Format Notes

- **GET /tasks**: Use DD-MM-YYYY format for the `date` parameter
- **POST /tasks**: Use YYYY-MM-DD format in the request body
- **PUT /update**: Use YYYY-MM-DD format in the request body
- **DELETE /delete**: Use YYYY-MM-DD format for the `date` parameter

---

## Python Examples for Streamlit

### Making API calls in your Streamlit app:

```python
import requests
import streamlit as st

# API configuration
BASE_URL = "http://localhost:8000"
API_KEY = "your_api_key_here"

# Get all tasks
def get_all_tasks():
    response = requests.get(f"{BASE_URL}/tasks")
    if response.status_code == 200:
        return response.json()
    return []

# Get tasks for a specific date
def get_tasks_by_date(date_str):
    response = requests.get(f"{BASE_URL}/tasks", params={"date": date_str})
    if response.status_code == 200:
        return response.json()
    return []

# Create a new task
def create_task(title, description, date):
    headers = {"X-API-Key": API_KEY}
    data = {
        "title": title,
        "description": description,
        "date": date
    }
    response = requests.post(f"{BASE_URL}/tasks", json=data, headers=headers)
    return response.status_code == 201

# Delete a specific task
def delete_task(title, date):
    headers = {"X-API-Key": API_KEY}
    data = {
        "title": title,
        "date": date
    }
    response = requests.put(f"{BASE_URL}/update", json=data, headers=headers)
    return response.status_code == 200

# Delete all tasks for a date
def delete_all_tasks_for_date(date):
    headers = {"X-API-Key": API_KEY}
    response = requests.delete(f"{BASE_URL}/delete", params={"date": date}, headers=headers)
    return response.status_code == 200
```

---

## Testing Your API

1. **Start your FastAPI server:**
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Test endpoints using curl or Postman**

3. **Check API documentation at:**
   ```
   http://localhost:8000/docs
   ```

---

## Common Issues and Solutions

### Issue: "Invalid API key"
- **Solution**: Make sure your API key matches the one in your `.env` file
- **Check**: Verify the `API_KEY` environment variable is set correctly

### Issue: "Connection refused"
- **Solution**: Make sure your FastAPI server is running on port 8000
- **Check**: Run `uvicorn app.main:app --reload`

### Issue: Date format errors
- **Solution**: Use the correct date format for each endpoint
- **Remember**: GET requests use DD-MM-YYYY, POST/PUT/DELETE use YYYY-MM-DD
