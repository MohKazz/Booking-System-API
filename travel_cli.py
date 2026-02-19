import argparse
from travel import create, read_all, insert_user, login_user

def main():
    parser = argparse.ArgumentParser(description="Travel Booking CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Subcommand: add-booking
    add_parser = subparsers.add_parser("add-booking", help="Add a new booking")
    add_parser.add_argument("--name", required=True, help="Customer name")
    add_parser.add_argument("--email", required=True, help="Customer email")
    add_parser.add_argument("--phone", type=int, required=True, help="Phone number")
    add_parser.add_argument("--destination", required=True, help="Destination")
    add_parser.add_argument("--travelers", type=int, required=True, help="Number of travelers")

    # Subcommand: list-bookings
    list_parser = subparsers.add_parser("list-bookings", help="List all bookings")
    list_parser.add_argument("--user_id", type=int, help="Filter bookings by user ID")
    list_parser.add_argument("--destination_id", type=int, help="Filter bookings by destination ID")
    list_parser.add_argument("--booking_id", type=int, help="Filter bookings by booking ID")
    list_parser.add_argument("--phone_number", type=int, help="Filter bookings by phone number")
    list_parser.add_argument("--customer_name", type=str, help="Filter bookings by customer name")
    list_parser.add_argument("--customer_email", type=str, help="Filter bookings by customer email")
    list_parser.add_argument("--num_travelers", type=int, help="Filter bookings by number of travelers")
    list_parser.add_argument("--traveler_names", type=str, help="Filter bookings by traveler names")
    list_parser.add_argument("--passport_number", type=str, help="Filter bookings by passport number")
    
    # Subcommand: insert_user
    register_parser = subparsers.add_parser("insert_user", help="Register a new user")
    register_parser.add_argument("--name", required=True, help="User's name")
    register_parser.add_argument("--email", required=True, help="User's email")
    register_parser.add_argument("--phone", type=int, required=True, help="User's phone number")
    register_parser.add_argument("--password", required=True, help="User's password")   

    args = parser.parse_args()

    if args.command == "add-booking":
        booking = {
            "customer_name": args.name,
            "customer_email": args.email,
            "phone_number": args.phone,
            "destination": args.destination,
            "num_travelers": args.travelers
        }
        booking_id, _ = create(booking)
        print(f"Booking created with ID: {booking_id}")

    elif args.command == "list-bookings":
        bookings = read_all().json 
        print("All Bookings:")
        for b in bookings:
            print(f"- ID {b['booking_id']}: {b['customer_name']} to {b['destination']} ({b['num_travelers']} travelers)")
    
    elif args.command == "insert_user":
        user_data = {
            "name": args.name,
            "email": args.email,
            "phone": args.phone,
            "password": args.password
                    }

        user_id = insert_user(user_data)
        print(f"User registered with ID: {user_id}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
#python travel_cli.py <command> [arguments]
