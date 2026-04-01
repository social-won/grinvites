from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
#import user
from pydantic import BaseModel
import sqlite3

class User(BaseModel):
    id: int
    email: str
    display_name: str
    calendar_type: str
    prefer_notify: int

class UserCreate(BaseModel):
    email: str
    display_name: str
    calendar_type: str
    prefer_notify: int


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

@app.post("/users")
async def create_user(user_data: UserCreate):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (email, display_name, calendar_type, prefer_notify)
        VALUES (?, ?, ?, ?)
    ''', (user_data.email, user_data.display_name, user_data.calendar_type, user_data.prefer_notify))
    
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    # Return the created user with the generated ID
    return User(
        id=user_id,
        email=user_data.email,
        display_name=user_data.display_name,
        calendar_type=user_data.calendar_type,
        prefer_notify=user_data.prefer_notify
    )

# I'm not sure how many of these endpoints should be for a general user and for the current user, if we even need the general case?

# Create new user
# @app.post("/user")
# async def create_user():
#     user = user.User()
#     return user

# # I have no idea if this is how we want to do auth but claude gave it to me this way
# # def get_current_user(token: str = Depends(oauth2_scheme)):
# #     payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
# #     return db.query(User).get(payload["sub"])

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
    cursor.execute("PRAGMA table_info(users)")
    table_info = cursor.fetchall()
    column_names = []
    for row in table_info:
        column_names.append(row[1])
    user = dict(zip(column_names, user))
    conn.close()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# # Update user object
# @app.put("/user/{user_id}")
# async def set_user(user_id):
#     conn = sqlite3.connect("database.db")
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO users (id) VALUES (?)", (user_id,))
#     conn.close()
#     pass

# # Get user interests
# @app.get("/user/{user_id}/interests")
# async def read_user_interests(user_id):
#     conn = sqlite3.connect("database.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT interests FROM users WHERE id = ?", (user_id,))
#     interests = cursor.fetchone()
#     conn.close()
#     if not interests:
#         raise HTTPException(status_code=404, detail="User not found")
#     return interests

# # Update user interests
# @app.put("/user/{user_id}/interests")
# async def set_user_interests(user_id):
#     conn = sqlite3.connect("database.db")
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO interests (id) VALUES (?)", (user_id,))
#     conn.close()
#     pass



# # Get event
# @app.get("/events/{event_id}")
# async def read_event(event_id):
#     conn = sqlite3.connect("database.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
#     event = cursor.fetchone()
#     conn.close()
#     if not event:
#         raise HTTPException(status_code=404, detail="Event not found")
#     return event

# # Get events <--- this one I imagine is going to be pretty complex query params
# @app.get("/events")
# async def read_events():
#     pass

#gets root
@app.get("/")
async def root():
    return {"message": "Account Created!"}