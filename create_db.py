import sqlite3

def initialize_database():
    conn = sqlite3.connect("travel.db")
    cursor = conn.cursor()

    print("Creating tables if they don't exist...")

    cursor.execute("""DROP TABLE IF EXISTS destinations""")
    cursor.execute("""DROP TABLE IF EXISTS users""")
    cursor.execute("""DROP TABLE IF EXISTS booking""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS destination (
                   destination_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   destination TEXT 
    )
                  
    """)

    cursor.execute("""
    CREATE TABLE users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT ,
        phone_number  TEXT,
        customer_email TEXT,
         password TEXT NOT NULL              
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS booking (
        booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER ,
        num_travelers INTEGER,
        destination_id INTEGER ,
        traveler_names text , 
        passport_number text ,          
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (destination_id) REFERENCES destination(destination_id)   
    )
    """)

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == "__main__":
    initialize_database()