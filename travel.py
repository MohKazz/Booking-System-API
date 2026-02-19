import sqlite3
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
#connect to DB
def get_db_connection():
    conn = sqlite3.connect("travel.db")
    conn.row_factory = sqlite3.Row
    return conn
# Convert rows to dictionary
def row_to_dict(row):
    return {key: row[key] for key in row.keys()}


def register_user():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    # Check if user already exists
    cursor.execute("SELECT * FROM users WHERE customer_email = ?", (data["email"],))
    existing_user = cursor.fetchone()
    if existing_user:
        conn.close()
        return "User already exists", 409
    # Insert new user into the database if not exists
    cursor.execute("""
        INSERT INTO users (customer_name, phone_number, customer_email, password)
        VALUES (?, ?, ?, ?)
    """, (
        data["name"],
        data["phone"],
        data["email"],
        generate_password_hash(data["password"])
    ))
    conn.commit()
    conn.close()
    return "User registered", 201

def login_user():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, password FROM users WHERE customer_email = ?", (data["email"],))
    user = cursor.fetchone()
    conn.close()
    if user and check_password_hash(user["password"], data["password"]):
        return jsonify({"user_id": user["user_id"]}), 200
    return "Invalid credentials", 401

#crud operations
def create(booking):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Ensure user_id is present
    if "user_id" not in booking:
        conn.close()
        return "Missing user_id", 400
    user_id = booking["user_id"]

    # Reuse destination if it already exists
    cursor.execute("SELECT destination_id FROM destination WHERE destination = ?", (booking["destination"],))
    row = cursor.fetchone()

    if row:
        destination_id = row["destination_id"]
    else:
        cursor.execute("INSERT INTO destination (destination) VALUES (?)", (booking["destination"],))
        destination_id = cursor.lastrowid

    # Insert booking with reference to user and destination
    cursor.execute("""
        INSERT INTO booking (user_id, num_travelers, destination_id , traveler_names, passport_number)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, booking["num_travelers"], destination_id, booking.get("traveler_names"), booking.get("passport_number") ))

    # in this part you can first start wirting two queries that fills the first and second parent tabels(users and destinations) and then once thats done you can then wirte a querey that fills the third table. so when you try to fech data form the child table it will then have the foreign kees for the other talbes.
    conn.commit()
    booking_id = cursor.lastrowid #after inserting this gets the newly created booking's ID
    conn.close()
    return booking_id, 201




def read_all(user_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if user_id:
        cursor.execute("""
            SELECT 
                b.booking_id,
                u.customer_name,
                b.traveler_names,
                b.passport_number,
                u.phone_number,
                u.customer_email,
                b.num_travelers,
                d.destination
            FROM booking b
            JOIN users u ON b.user_id = u.user_id
            JOIN destination d ON b.destination_id = d.destination_id
            WHERE b.user_id = ?
        """, (user_id,))
        
    #for later use
    # else:
    #  cursor.execute("""
    # SELECT 
    #     b.booking_id,
    #     u.customer_name,
    #     u.phone_number,
    #     u.customer_email,
    #     b.num_travelers,
    #     d.destination
    # FROM booking b
    # JOIN users u ON b.user_id = u.user_id
    # JOIN destination d ON b.destination_id = d.destination_id        

    # """)
    rows = cursor.fetchall()
    conn.close()
    return jsonify([row_to_dict(row) for row in rows])




def read_one(booking_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT 
        b.booking_id,
        b.user_id,
        u.customer_name,
        u.phone_number,
        u.customer_email,
        b.passport_number,
        b.num_travelers,
        b.traveler_names,
        d.destination
    FROM booking b
    JOIN users u ON b.user_id = u.user_id
    JOIN destination d ON b.destination_id = d.destination_id
    WHERE b.booking_id = ? """, (booking_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return jsonify(row_to_dict(row))
    return "Booking not found", 404

def update(booking_id, booking):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT u.user_id, d.destination_id
    FROM booking b
    JOIN users u ON u.user_id = b.user_id
    JOIN destination d ON b.destination_id = d.destination_id
    WHERE b.booking_id = ? """, (booking_id,))
    result = cursor.fetchone()

    if not result:
        return "Booking not found", 404
    user_id = result['user_id']
    destination_id = result['destination_id']
    print(destination_id)
    cursor.execute( """ UPDATE booking SET num_travelers = ? WHERE booking_id = ? """, (booking["num_travelers"],booking_id) )
    cursor.execute( """ UPDATE destination SET destination = ? WHERE destination_id = ? """, (booking["destination"],destination_id) )
    cursor.execute( """ UPDATE booking SET traveler_names = ?, passport_number = ? WHERE booking_id = ? """, (booking["traveler_names"], booking["passport_number"],booking_id) )
    conn.commit()
    conn.close()
    return read_one(booking_id)

def delete(booking_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM booking WHERE booking_id = ?", (booking_id,))
    conn.commit()
    conn.close()
    return "Booking deleted", 204
