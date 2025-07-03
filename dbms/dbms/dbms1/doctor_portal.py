import sqlite3

# Connect to the existing SQLite database
conn = sqlite3.connect('hospital_management_system.db')
cursor = conn.cursor()

def doctor_menu(doctor_id):
    while True:
        print("\n--- Doctor Portal ---")
        print("1. View Appointments\n2. Prescribe Medicines\n3. Assign Nurse\n4. View Billing\n5. Logout")
        choice = input("Select an option: ")

        if choice == '1':
            view_appointments(doctor_id)
        elif choice == '2':
            prescribe_medicines(doctor_id)
        elif choice == '3':
            assign_nurse(doctor_id)
        elif choice == '4':
            view_billing(doctor_id)
        elif choice == '5':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

def view_appointments(doctor_id):
    print("\n--- View Appointments ---")
    try:
        cursor.execute(
            "SELECT a.appointment_id, p.name, a.appointment_date, a.appointment_time "
            "FROM Appointment a "
            "JOIN Patient p ON a.patient_id = p.patient_id "
            "WHERE a.doctor_id = ?", 
            (doctor_id,)
        )
        
        rows = cursor.fetchall()
        
        if rows:
            for row in rows:
                print(f"Appointment ID: {row[0]}, Patient: {row[1]}, Date: {row[2]}, Time: {row[3]}")
        else:
            print("No appointments found for this doctor.")
    except sqlite3.Error as e:
        print(f"Error retrieving appointments: {e}")

def prescribe_medicines(doctor_id):
    print("\n--- Prescribe Medicines ---")
    patient_id = input("Enter Patient ID: ")
    medicine_id = input("Enter Medicine ID: ")
    try:
        cursor.execute(
            "INSERT INTO Prescription (patient_id, doctor_id, medicine_id) VALUES (?, ?, ?)", 
            (patient_id, doctor_id, medicine_id)
        )
        conn.commit()
        print(f"Medicine {medicine_id} prescribed to Patient {patient_id}.")
    except sqlite3.Error as e:
        print(f"Error prescribing medicine: {e}")

def assign_nurse(doctor_id):
    print("\n--- Assign Nurse ---")
    nurse_id = input("Enter Nurse ID: ")
    patient_id = input("Enter Patient ID: ")
    try:
        cursor.execute("UPDATE Room SET nurse_id = ? WHERE patient_id = ?", (nurse_id, patient_id))
        conn.commit()
        print(f"Nurse {nurse_id} assigned to Patient {patient_id}")
    except sqlite3.Error as e:
        print(f"Error assigning nurse: {e}")

def view_billing(doctor_id):
    print("\n--- View Billing ---")
    patient_id = input("Enter Patient ID: ")
    try:
        cursor.execute("SELECT total_cost, status, insurance_applied FROM Bill WHERE patient_id = ?", (patient_id,))
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                insurance_status = 'Applied' if row[2] else 'Not Applied'
                print(f"Total Cost: {row[0]}, Status: {row[1]}, Insurance: {insurance_status}")
        else:
            print("No billing information found for this patient.")
    except sqlite3.Error as e:
        print(f"Error retrieving billing information: {e}")