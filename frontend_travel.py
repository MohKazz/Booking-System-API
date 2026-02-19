from flask import Flask, render_template, request, redirect, make_response, flash, session
from travel_api_shim import (  add_booking, list_bookings, get_booking,update_booking, delete_booking,register_user, login_user)
from datetime import timedelta

app = Flask(__name__)
# Set a secret key for session management so that Flask can securely sign the session cookie and protect against tampering.
app.secret_key = 'ijskldsgn@0&*'
app.permanent_session_lifetime = timedelta(minutes=30) # Set session lifetime to 30 minutes, incae the user is inactive for that long, the session will expire.

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user_data = {
            "name": request.form["name"],
            "email": request.form["email"],
            "phone": request.form["phone"],
            "password": request.form["password"]
        }
        response = register_user(user_data)
        if response.status_code == 201:
            return redirect("/login")
        elif response.status_code == 409:
            return redirect("/login")
    
    return render_template("travel/register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("travel/login.html")
    
    elif request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]
        user_id = login_user(email, password)

        if user_id:
            session["user_id"] = user_id
            session.permanent = True 
            return redirect("/")
        else:
            return redirect("/login")
    # If the request method is neither GET nor POST, return an error response
    return make_response("Invalid request", 400)



@app.route("/")
def homepage():
    if "user_id" not in session:
        return redirect("/login")
    
    bookings = list_bookings(user_id=session["user_id"])
    return render_template("travel/main.html", bookings=bookings)

@app.route("/destinations/")
def des():
    return render_template("travel/destinations.html")

@app.route("/profile/")
def profile():
    if "user_id" in session:
        user_id = session["user_id"]
        bookings = list_bookings(user_id=user_id)
        return render_template("travel/profile.html", bookings=bookings, user_id=user_id)
    else:
       
        return redirect("/login")
    
@app.route("/new/", methods=["GET", "POST"])
def new_booking():
    if "user_id" not in session:
        return redirect("/login")
        
    
    if request.method == "GET":
        return render_template("travel/new_booking.html")
    elif request.method == "POST":
        booking = {
            "destination": request.form["destination"],
            "num_travelers": int(request.form["num_travelers"]),
            "user_id": session["user_id"],
             "traveler_names": request.form.get("traveler_names"),  
             "passport_number": request.form.get("passport_number") 

        }
        booking["booking_id"] = add_booking(booking)
        return redirect("/")
    return make_response("Invalid request", 400)

@app.route("/edit/<int:booking_id>", methods=["GET", "POST"])
def edit_booking(booking_id):
    # confitional statements to check if user is logged in
    if "user_id" not in session:
        return redirect("/login")
    #denying access to others bookings
    booking = get_booking(booking_id)
    if booking["user_id"] != session["user_id"]:
     flash("access denied!")
     return redirect("/")

    if request.method == "GET":
        booking = get_booking(booking_id)
        return render_template("travel/edit_booking.html", booking=booking)
    elif request.method == "POST":
        booking = {
            "booking_id": booking_id,
            "traveler_names": request.form["traveler_names"],
            "destination": request.form["destination"],
            "num_travelers": int(request.form["num_travelers"]),
            "passport_number": request.form["passport_number"]
        }
        update_booking(booking)
        return redirect("/")
    return make_response("Invalid request", 400)

@app.route("/delete/<int:booking_id>")
def delete_booking_route(booking_id):
    # Checking if user is logged in
    if "user_id" not in session:
        return redirect("/login")
    # Denying access to others' bookings
    booking = get_booking(booking_id)
    if booking["user_id"] != session["user_id"]:
     flash("access denied!")
     return redirect("/")
    delete_booking(booking_id)
   
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()

    return redirect("/login")

if __name__ == "__main__":
    app.run(host="0.0.0.0",port="80",debug=True)
