import streamlit as st
import requests
import pandas as pd
from urllib.parse import urljoin
import os
from dotenv import load_dotenv
load_dotenv()

st.title("To-Do App")

# API endpoint
url = "http://localhost:8000"

responce_home = requests.get(url = url)
if responce_home:
    st.text(responce_home.json()["message"])

# GET
st.subheader("Click to get your tasks")

if "show_tasks" not in st.session_state:
    st.session_state.show_tasks = False

b1, b2 = st.columns(2)
with b1:
    if st.button("Check Tasks"):
        st.session_state.show_tasks = True
with b2:
    if st.button("Hide Tasks"):
        st.session_state.show_tasks = False



if st.session_state.show_tasks:
    responce = requests.get(url = urljoin(url, "tasks")).json()
    df = pd.DataFrame(responce)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by = 'date')

    for date, group in df.groupby("date"):
        st.subheader(f"📅 {date.date()}")
        st.table(group[['title', 'description']].reset_index(drop=True))


st.text("Enter passcord to get more option")
# requests that need post requests:
passkey = st.text_input(label= "Enter Passkey", help="Ask Vishu if you don't know !!" )
headers_main = {
    "Content-Type": "application/json",
    "X-API-Key": passkey
}

if passkey != os.environ.get("API_KEY") and passkey:
    st.error("Invalid API key")
elif passkey == os.environ.get("API_KEY"):
    # Headers

    # Post
    st.subheader("Add Task")
    c1, c2, c3 = st.columns(3)
    with c1:
        task_date = st.date_input("Select Date*", key="add_task_date")
    with c2:
        task_title = st.text_input("Task Title*")
    with c3:
        # st.badge("optional")
        task_desc = st.text_input("Task Input")
    
    if task_date and task_title:

        payload = {
            "title": task_title,
            "description": task_desc,
            "date": task_date.isoformat()
        }
        if st.button("Add Task"):
            post_responce = requests.post(url = urljoin(url, "tasks"), headers=headers_main, json=payload)
            print(post_responce.json())
            if post_responce.status_code == 200:
                
                st.success("Task Added")
            else:
                st.error(post_responce.json()["message"])
            


    # PUT
    st.header("")
    st.subheader("Remove a task")

    col1, col2 = st.columns(2)

    with col1:
        put_date = st.date_input("Select Date*", key="remove_task_date")
    with col2:
        put_title = st.text_input("Task Title*", key="remove_task")

    
    if put_date and put_title:
        payload = {
            "date": put_date.isoformat(),
            "title": put_title
        }
        if st.button("Remove"):
            responce = requests.put(urljoin(url, "update"), headers=headers_main, json= payload)
            if responce.status_code == 200:
                st.success(responce.json()["message"])
            else:
                st.error(responce.json()["detail"])
    

    # Delete
    st.subheader("")
    st.subheader("Remove all tasks for the sellected day")
    del_date = st.date_input("Select Date*", key = "delete_task_date")

    if del_date:

        if st.button("Delete all Tasks"):
            responce = requests.delete(urljoin(url, "delete"), headers=headers_main, params={"date": del_date.isoformat()})
            # print(responce.json())
            if responce.status_code ==200:
                st.success(responce.json()["message"])
            else:
                st.error(responce.json()["detail"])

