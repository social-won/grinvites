# import sqlite3
# import sql_init
# from user import User

# def teardown_test_db():
#     import os
#     if os.path.exists("test_database.db"):
#         os.remove("test_database.db")

# # Run setup before tests (pytest fixture alternative)
# db_init = sql_init.init_db()  # Initialize the test database

# # Test the root endpoint
# def test_root():
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"message": "Hello, World!"}

# # Test creating a user (note: your current implementation creates an empty User object)
# def test_create_user():
#     response = client.post("/user")
#     assert response.status_code == 200
#     # Assert based on your User class (e.g., check if it returns a dict with email/interests)
#     data = response.json()
#     assert "email" in data  # Assuming User.__dict__ or similar is returned

# # Test reading a user (requires a user in DB)
# def test_read_user():
#     # First, insert a test user into the DB
#     conn = sqlite3.connect("test_database.db")
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO users (id, email, interests) VALUES (?, ?, ?)", (1, "test@example.com", "music"))
#     conn.commit()
#     conn.close()
    
#     response = client.get("/user/1")
#     assert response.status_code == 200
#     data = response.json()
#     assert data[1] == "test@example.com"  # Adjust based on your DB schema

# # Test reading a non-existent user
# def test_read_user_not_found():
#     response = client.get("/user/999")
#     assert response.status_code == 404
#     assert "User not found" in response.json()["detail"]

# # Test updating a user (your current impl just inserts; adapt as needed)
# def test_set_user():
#     response = client.put("/user/2")
#     assert response.status_code == 200  # Or whatever your endpoint returns

# # Test reading user interests
# def test_read_user_interests():
#     # Insert test data
#     conn = sqlite3.connect("test_database.db")
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO users (id, interests) VALUES (?, ?)", (3, "sports"))
#     conn.commit()
#     conn.close()
    
#     response = client.get("/user/3/interests")
#     assert response.status_code == 200
#     assert response.json() == ("sports",)  # Based on fetchone()

# # Test updating user interests
# def test_set_user_interests():
#     response = client.put("/user/4/interests")
#     assert response.status_code == 200

# # Test reading an event (requires event in DB)
# def test_read_event():
#     conn = sqlite3.connect("test_database.db")
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO events (id, name) VALUES (?, ?)", (1, "Concert"))
#     conn.commit()
#     conn.close()
    
#     response = client.get("/events/1")
#     assert response.status_code == 200
#     assert response.json() == (1, "Concert")

# # Test reading events (your endpoint is a stub; add logic and test accordingly)
# def test_read_events():
#     response = client.get("/events")
#     assert response.status_code == 200
#     # Assert based on what you implement

# # tests
# test_user = User(email="test@example.com", interests=["mathSEPC", "Frisbee"])
# test_root()

# # Clean up after all tests
# teardown_test_db()