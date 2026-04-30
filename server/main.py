import json
import sqlite3
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
#import user
from pydantic import BaseModel
from typing import List
import sqlite3
from datetime import datetime

from contextlib import asynccontextmanager
import asyncio

from api.sql_init import initialize_database
from models import User, UserInterestsUpdate
from api.db_functions import add_user, get_db, get_user


if os.getenv("E2E_TESTING"):
    initialize_database()
# Written following https://fastapi.tiangolo.com/tutorial/
app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/users", status_code=201)
async def create_user(user_data: User):
    try:
       add_user(user_data)
    except sqlite3.OperationalError as e:
      raise HTTPException(status_code=500, detail=str(e))
    

# I'm not sure how many of these endpoints should be for a general user and for the current user, if we even need the general case?

# # I have no idea if this is how we want to do auth but claude gave it to me this way
# # def get_current_user(token: str = Depends(oauth2_scheme)):
# #     payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
# #     return db.query(User).get(payload["sub"])

# # get current user
# @app.get("/users/me")
# def read_me(current_user: User = Depends(get_current_user)):
#     return current_user

# Get user object
@app.get("/users/{user_id}")
async def read_user(user_id):
    user = get_user(user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

# Update user object
@app.put("/users/{user_id}")
async def update_user(user_id, user_data: User):
    #TODO: Refactor this to db_functions.py
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email=?, display_name=?, invite_times=? WHERE id=?", 
                   (user_data.email, user_data.display_name, json.dumps(user_data.invite_times), user_id))
    conn.commit()
    conn.close()
    

# Get user interests
@app.get("/users/{user_id}/interests")
async def read_user_interests(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT interests FROM users WHERE id = ?", (user_id,))
    interests_pulled = cursor.fetchall()
    interests = []
    for row in interests_pulled:
        interests.append(row[1])
    user = dict(zip(interests, user))
    conn.close()
    if not interests:
        raise HTTPException(status_code=404, detail="User not found")
    return interests

# Update user interests
@app.put("/users/{user_id}/interests")
async def update_user_interests(user_id: int, interests_data: UserInterestsUpdate):
    conn = get_db()
    cursor = conn.cursor()
    # Delete existing interests for the user
    #cursor.execute("DELETE FROM user_interests WHERE user_id = ?", (user_id,))
    # Insert new interests
    for interest_id in interests_data.interest_ids:
        cursor.execute("INSERT INTO user_interests (user_id, interest_id) VALUES (?, ?)", (user_id, interest_id))
    conn.commit()
    conn.close()
    return {"message": "User interests updated successfully"}



# Get event object
@app.get("/events/{event_id}")
async def read_event(event_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
    event_info = cursor.fetchall()
    event = []
    for row in event_info:
        event.append(row[1])
    event = dict(zip(event_info, event))
    conn.close()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

# # Get events <--- this one I imagine is going to be pretty complex query params
# @app.get("/events")
# async def read_events():
#     pass

#gets root
@app.get("/")
async def root():
    return {"message": "Account Created!"}