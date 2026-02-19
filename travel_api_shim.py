import requests
import json
import os

BASE_URL = os.environ.get("API_BASE_URL", "http://127.0.0.1:82/api")

def register_user(user_data):
    response = requests.post(f"{BASE_URL}/register", json=user_data)
    return response

def login_user(email, password):
    response = requests.post(f"{BASE_URL}/login", json={"email": email, "password": password})
    #Check if the response is successful and contains a user_id
    if response.status_code == 200:
        return response.json()["user_id"]
    return None

def add_booking(booking):
    response = requests.post(f"{BASE_URL}/bookings", json=booking)
    return response


def list_bookings(user_id=None):
    url = f"{BASE_URL}/bookings"
    if user_id:
        url += f"?user_id={user_id}"
    response = requests.get(url)
    return json.loads(response.text)


def get_booking(booking_id):
    response = requests.get(f"{BASE_URL}/bookings/{booking_id}")
    return json.loads(response.text)


def update_booking(booking):
    response = requests.put(f"{BASE_URL}/bookings/{booking['booking_id']}", json=booking
    )

    if response.status_code == 200 and response.text.strip():
        return json.loads(response.text)
    else:
        print("Update failed or empty response:", response.status_code, response.text)
        print("RESPONSE STATUS:", response.status_code)
        print("RESPONSE TEXT:", repr(response.text))

        return None


def delete_booking(booking_id):
       response=  requests.delete(f"{BASE_URL}/bookings/{booking_id}")
       print(response)
       return response
