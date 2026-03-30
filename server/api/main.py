from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import user
from pydantic import BaseModel


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

# I'm not sure how many of these endpoints should be for a general user and for the current user, if we even need the general case?


# Create new user
@app.post("/user")
async def create_user():
    user = user.User()
    return user

# I have no idea if this is how we want to do auth but claude gave it to me this way
# def get_current_user(token: str = Depends(oauth2_scheme)):
#     payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#     return db.query(User).get(payload["sub"])

# # get current user
# @app.get("/users/me")
# def read_me(current_user: User = Depends(get_current_user)):
#     return current_user

# Get user object
@app.get("/user/{user_id}")
async def read_user(user_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update user object
@app.put("/user/{user_id}")
async def set_user(user_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (id) VALUES (?)", (user_id,))
    conn.close()
    pass

# Get user interests
@app.get("/user/{user_id}/interests")
async def read_user_interests(user_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT interests FROM users WHERE id = ?", (user_id,))
    interests = cursor.fetchone()
    conn.close()
    if not interests:
        raise HTTPException(status_code=404, detail="User not found")
    return interests

# Update user interests
@app.put("/user/{user_id}/interests")
async def set_user_interests(user_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO interests (id) VALUES (?)", (user_id,))
    conn.close()
    pass



# Get event
@app.get("/events/{event_id}")
async def read_event(event_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
    event = cursor.fetchone()
    conn.close()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

# Get events <--- this one I imagine is going to be pretty complex query params
@app.get("/events")
async def read_events():
    pass

#gets root
@app.get("/")
async def root():
    return {"message": "Hello, World!"}