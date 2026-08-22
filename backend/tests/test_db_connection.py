from agent.db import get_db_connection


connection = get_db_connection()

if connection.is_connected():
    print("MySQL connection successful!")

cursor = connection.cursor()

cursor.execute("SELECT DATABASE()")
database = cursor.fetchone()

print("Connected database:", database[0])

cursor.close()
connection.close()