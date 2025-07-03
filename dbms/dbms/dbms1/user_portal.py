import sqlite3

# Connect to the database
conn = sqlite3.connect('hospital_management_system.db')
cursor = conn.cursor()

def main():
    print("Welcome to the Hospital Management System")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    
    # In a real-world scenario, you would validate the username and password here.
    user_menu(username, password)

def user_menu(username, password):
    while True:
        print("\n--- User Portal ---")
        print("1. Book Appointment\n2. View Medicines\n3. View Room\n4. Logout")
        choice = input("Select an option: ")

        if choice == '1':
            book_appointment(username)
        elif choice == '2':
            view_medicines(username)
        elif choice == '3':
            view_room(username)
        elif choice == '4':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

def book_appointment(username):
    doctor_id = input("Enter the Doctor ID to book an appointment with: ")
    appointment_date = input("Enter appointment date (YYYY-MM-DD): ")
    appointment_time = input("Enter appointment time (HH:MM): ")
    
    try:
        # Insert appointment data
        cursor.execute(
            "INSERT INTO Appointment (patient_id, doctor_id, appointment_date, appointment_time) "
            "VALUES ((SELECT patient_id FROM Patient WHERE name=?), ?, ?, ?)", 
            (username, doctor_id, appointment_date, appointment_time)
        )
        conn.commit()
        print(f"Appointment booked successfully for {appointment_date} at {appointment_time}.")
    except sqlite3.Error as e:
        print(f"Error booking appointment: {e}")

def view_medicines(username):
    print("\n--- View Medicines ---")
    try:
        # Fetch the medicines prescribed to the user
        cursor.execute(
            "SELECT m.name, m.cost FROM Medicine m "
            "JOIN Prescription p ON m.medicine_id = p.medicine_id "
            "WHERE p.patient_id = (SELECT patient_id FROM Patient WHERE name=?)", 
            (username,)
        )
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                print(f"Medicine: {row[0]}, Cost: {row[1]}")
        else:
            print("No medicines found for this patient.")
    except sqlite3.Error as e:
        print(f"Error viewing medicines: {e}")

def view_room(username):
    print("\n--- View Room ---")
    try:
        # Fetch the room details for the user
        cursor.execute(
            "SELECT r.room_type, r.room_number, r.room_cost FROM Room r "
            "JOIN PatientRoom pr ON r.room_id = pr.room_id "
            "WHERE pr.patient_id = (SELECT patient_id FROM Patient WHERE name=?)", 
            (username,)
        )
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                print(f"Room Type: {row[0]}, Room Number: {row[1]}, Cost per Day: {row[2]}")
        else:
            print("No room information found for this patient.")
    except sqlite3.Error as e:
        print(f"Error viewing room information: {e}")

# Close the connection when done
def close_connection():
    conn.close()
    print("Database connection closed.")

if __name__ == "__main__":
    main()
    close_connection()