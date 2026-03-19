import pyodbc

server   = 'socialwonserver.database.windows.net'
database = 'social_won_db_init'
username = 'owen'
password = 'social#1'
driver   = '{ODBC Driver 18 for SQL Server}'

try:
    connection = pyodbc.connect(
        f'DRIVER={driver};SERVER={server};DATABASE={database};'
        f'UID={username};PWD={password}'
    )
    print("Connection successful!")
except Exception as e:
    print("Connection failed:", e)
    raise         # stop if you can’t connect
# Create table if it doesn't exist
create_table_query = """
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'users')
BEGIN
    CREATE TABLE users (
        id INT PRIMARY KEY IDENTITY(1,1),
        email VARCHAR(255) NOT NULL,
        box_one VARCHAR(50),
        box_two VARCHAR(50),
        box_three VARCHAR(50)
    )
END
"""

c = connection.cursor()
# c.execute(create_table_query)
# connection.commit()
# print("Table 'users' is ready.")
# sql_insert_query = (
#     "INSERT INTO users (email, box_one, box_two, box_three) "
#     "VALUES (?, ?, ?, ?)"
# )
# record_for_insert = ("socialw@grinnell.edu", "0", "1", "1")

# c = connection.cursor()
# c.execute(sql_insert_query, record_for_insert)
# connection.commit()
# print(c.rowcount, "record inserted successfully!")

# sql_q = "SELECT * FROM users"
# c.execute(sql_q)
rows = c.fetchall()
for row in rows:
    print(row)

c.close()
connection.close()
print("ODBC connection is closed.")