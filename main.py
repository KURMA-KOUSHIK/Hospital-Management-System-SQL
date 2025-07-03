import sqlite3
import getpass
from admin_portal import admin_portal
from doctor_portal import doctor_portal
from nurse_portal import nurse_portal
from receptionist_portal import receptionist_portal
from accountant_portal import accountant_portal

# Connect to the SQLite database
conn = sqlite3.connect('hospital.db')
cursor = conn.cursor()

# Enable foreign key constraints
cursor.execute("PRAGMA foreign_keys = ON;")

# Function to create necessary tables
def create_tables():
    # Create Doctor Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Doctor (
            doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            d_name TEXT NOT NULL,
            specialty TEXT NOT NULL,
            phone_number TEXT NOT NULL
        )
    ''')

    # Create Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            doctor_id INTEGER,
            FOREIGN KEY (doctor_id) REFERENCES Doctor(doctor_id)
        )
    ''')

    # Insert default users (roles other than Doctor)
    users = [
        ("admin", "admin123", "Admin", None),
        ("nurse", "nurse123", "Nurse", None),
        ("reception", "reception123", "Receptionist", None),
        ("accountant", "account123", "Accountant", None)
    ]

    cursor.executemany('''
        INSERT OR IGNORE INTO Users (username, password, role, doctor_id)
        VALUES (?, ?, ?, ?)
    ''', users)

    conn.commit()
    print("Tables created and default users inserted successfully.")

# Call function to create necessary tables
create_tables()

# Function for user login
def login():
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")

    cursor.execute("SELECT role FROM Users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()

    if result:
        print(f"Login successful! Role: {result[0]}")
        return result[0], username  # Return both role and username
    else:
        print("Invalid username or password.")
        return None, None

# Function for admin to create new users
def create_new_user():
    print("\n--- Admin: Create New User ---")

    # Step 1: Choose the role
    print("Select role for the new user:")
    print("1. Doctor")
    print("2. Nurse")
    print("3. Receptionist")
    print("4. Accountant")
    role_choice = input("Enter the role number: ")

    roles = {"1": "Doctor", "2": "Nurse", "3": "Receptionist", "4": "Accountant"}
    role = roles.get(role_choice, None)

    if role == "Doctor":
        # Step 2: Check if the doctor exists and create a user account
        create_doctor_user()
    elif role:
        # Step 3: For non-doctors (Nurse, Receptionist, Accountant), create a user without doctor_id
        username = input("Enter new user's username: ")
        password = getpass.getpass("Enter new user's password: ")
        confirm_password = getpass.getpass("Confirm new user's password: ")

        if password == confirm_password:
            try:
                # Non-doctor users don't have a doctor_id, so set it as NULL
                cursor.execute("INSERT INTO Users (username, password, role, doctor_id) VALUES (?, ?, ?, NULL)", 
                               (username, password, role))
                conn.commit()
                print(f"New user '{username}' created with role '{role}' successfully!")
            except sqlite3.IntegrityError:
                print("Username already exists. Try again with a different username.")
        else:
            print("Passwords do not match. Try again.")
    else:
        print("Invalid role selection.")

# Function to create a user account for an existing doctor
def create_doctor_user():
    print("\n--- Admin: Create User Account for Doctor ---")
    
    # Step 1: Get doctor ID
    doctor_id = input("Enter the doctor's ID: ")

    # Step 2: Check if the doctor exists in the Doctor table
    cursor.execute("SELECT d_name FROM Doctor WHERE doctor_id=?", (doctor_id,))
    doctor_record = cursor.fetchone()

    if doctor_record:
        # Doctor exists, display the doctor's name
        print(f"Doctor found: {doctor_record[0]}")

        # Step 3: Create a user account for this doctor
        username = input("Enter doctor's username: ")
        password = getpass.getpass("Enter doctor's password: ")
        confirm_password = getpass.getpass("Confirm doctor's password: ")

        if password == confirm_password:
            try:
                # Insert user into the Users table with the role 'Doctor' and associate the doctor_id
                cursor.execute("INSERT INTO Users (username, password, role, doctor_id) VALUES (?, ?, ?, ?)", 
                               (username, password, 'Doctor', doctor_id))
                conn.commit()
                print(f"New user account created for Doctor {doctor_record[0]} with username '{username}'.")
            except sqlite3.IntegrityError:
                print("Username already exists. Try again with a different username.")
        else:
            print("Passwords do not match. Try again.")
    else:
        # Doctor ID does not exist
        print(f"No doctor found with ID {doctor_id}.")

# Function to update user password
def update_password():
    username = input("Enter your username: ")
    current_password = getpass.getpass("Enter your current password: ")

    # Verify current password
    cursor.execute("SELECT password FROM Users WHERE username=?", (username,))
    result = cursor.fetchone()

    if result and result[0] == current_password:
        new_password = getpass.getpass("Enter your new password: ")
        confirm_password = getpass.getpass("Confirm your new password: ")

        # Check if new password matches confirmation
        if new_password == confirm_password:
            # Update password in the database
            cursor.execute("UPDATE Users SET password=? WHERE username=?", (new_password, username))
            conn.commit()
            print("Password updated successfully!")
        else:
            print("Passwords do not match. Try again.")
    else:
        print("Invalid current password. Try again.")

# Main menu to login, update password, or create new users (admin only)
def main_menu():
    while True:
        print("\n1. Login")
        print("2. Update Password")
        print("3. Create New User (Admin Only)")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            role, username = login()
            if role == "Admin":
                admin_portal(conn, cursor)
            elif role == "Doctor":
                doctor_portal(conn, cursor, username)
            elif role == "Nurse":
                nurse_portal(conn, cursor)
            elif role == "Receptionist":
                receptionist_portal(conn, cursor)
            elif role == "Accountant":
                accountant_portal(conn, cursor)
            else:
                print("Access denied or invalid role.")
        elif choice == "2":
            update_password()
        elif choice == "3":
            role, _ = login()
            if role == "Admin":
                create_new_user()
            else:
                print("Only Admin can create new users.")
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()

# Close the connection when done
conn.close()
