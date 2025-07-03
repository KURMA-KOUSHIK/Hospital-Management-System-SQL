from user_portal import user_menu
from doctor_portal import doctor_menu
from receptionist_portal import receptionist_menu
from nurse_portal import nurse_menu
from billing_portal import billing_menu

# Predefined usernames and passwords for each portal
credentials = {
    'user': {'username': 'user123', 'password': 'userpass'},
    'doctor': {'username': 'doc123', 'password': 'docpass', 'doctor_id': 3},  # Added doctor_id here
    'receptionist': {'username': 'rec123', 'password': 'recpass'},
    'nurse': {'username': 'nurse123', 'password': 'nursepass'},
    'billing': {'username': 'bill123', 'password': 'billpass'}
}

def login(portal):
    username = credentials[portal]['username']
    password = credentials[portal]['password']
    print(f"Logging into {portal.capitalize()} Portal...\n")
    return username, password

def main():
    print("Welcome to the Hospital Management System")
    while True:
        print("\n1. User Portal\n2. Doctor Portal\n3. Receptionist Portal\n4. Nurse Portal\n5. Billing Portal\n6. Exit")
        choice = input("Select a portal: ")

        if choice == '1':
            username, password = login('user')
            user_menu(username, password)
        elif choice == '2':
            username, password = login('doctor')
            doctor_id = credentials['doctor']['doctor_id']  # Fetch the doctor_id here
            doctor_menu(doctor_id)  # Only pass doctor_id to the doctor_menu
        elif choice == '3':
            username, password = login('receptionist')
            receptionist_menu()
        elif choice == '4':
            username, password = login('nurse')
            nurse_menu(username, password)
        elif choice == '5':
            username, password = login('billing')
            billing_menu()
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()