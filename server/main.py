import json
import sqlite3
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
# import user
from pydantic import BaseModel
import sqlite3
from datetime import datetime

from contextlib import asynccontextmanager
import asyncio

from api.sql_init import initialize_database
from models import User, UserInterestsUpdate, UserUpdate
from api.db_functions import *
from api.scraper import scrape_events, test_scraping
from api.interests import populate_interests
from daemon import run_daemon



@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.getenv("E2E_TESTING"):
        print("Initializing database")
        initialize_database()
        populate_interests()
        scrape_events()
        # test_scraping()

    task = asyncio.create_task(run_daemon(10))
    yield
    task.cancel()

initialize_database()
populate_interests()
scrape_events()
# test_scraping()
# Written following https://fastapi.tiangolo.com/tutorial/
app = FastAPI(lifespan=lifespan)

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
async def update_user(user_id: str, user_data: UserUpdate):
    conn = get_db()
    cursor = conn.cursor()
    if user_data.email is not None:
        cursor.execute("UPDATE users SET email=? WHERE id=?",
                       (user_data.email, user_id))
    if user_data.display_name is not None:
        cursor.execute("UPDATE users SET display_name=? WHERE id=?",
                       (user_data.display_name, user_id))
    if user_data.invite_times is not None:
        cursor.execute("UPDATE users SET invite_times=? WHERE id=?",
                       (json.dumps(user_data.invite_times), user_id))
    if user_data.theme is not None:
        cursor.execute("UPDATE users SET theme=? WHERE id=?",
                       (user_data.theme, user_id))
    conn.commit()
    conn.close()


# Get user interests
@app.get("/users/{user_id}/interests")
async def read_user_interests(user_id):
    interests = get_user_interests(user_id)
    if interests is None:
        raise HTTPException(status_code=404, detail="User not found")

    return interests

# Update user interests


@app.put("/users/{user_id}/interests")
async def update_user_interests(user_id: str, interests_data: UserInterestsUpdate):
    try:
        # Get user to verify they exist
        user = get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        conn = get_db()
        cursor = conn.cursor()

        # Validate interest IDs before modifying the join table
        if interests_data.interest_ids:
            placeholders = ",".join(["?" for _ in interests_data.interest_ids])
            cursor.execute(
                f"SELECT id FROM interests WHERE id IN ({placeholders})",
                tuple(interests_data.interest_ids),
            )
            valid_ids = {row[0] for row in cursor.fetchall()}
            missing_ids = [
                i for i in interests_data.interest_ids if i not in valid_ids]
            if missing_ids:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid interest_ids: {missing_ids}",
                )

        # Delete existing interests for this user
        cursor.execute(
            "DELETE FROM user_interests WHERE user_id = ?", (user_id,))

        # Add new interests
        for interest_id in interests_data.interest_ids:
            cursor.execute(
                "INSERT INTO user_interests (user_id, interest_id) VALUES (?, ?)",
                (user_id, interest_id)
            )
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get user events
@app.get("/users/{user_id}/events")
async def get_user_events(user_id: str):
    # Verify user exists
    user = get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get events that match user's interests
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT DISTINCT e.* FROM events e
        INNER JOIN event_interests ei ON e.id = ei.event_id
        INNER JOIN user_interests ui ON ei.interest_id = ui.interest_id
        WHERE ui.user_id = ?
        ORDER BY e.start_time
    ''', (user_id,))
    events = cursor.fetchall()
    conn.close()

    if not events:
        return []

    # Convert to list of dicts
    column_names = ["id", "creation_time_stamp", "title", "start_time", "end_time",
                    "location", "summary", "categories", "tags", "org_name", "frequency"]
    events_list = [dict(zip(column_names, row)) for row in events]
    return events_list


@app.get("/interests")
async def read_interests():
    return get_interests()

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

# gets root


@app.get("/")
async def root():
    return {"message": "Hi Mom!"}
