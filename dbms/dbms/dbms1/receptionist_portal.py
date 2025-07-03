import sqlite3

conn = sqlite3.connect('hospital_management_system.db')
cursor = conn.cursor()

def receptionist_menu():
    while True:
        print("\n--- Receptionist Portal ---")
        print("1. Book Appointment for Patient\n2. Logout")
        choice = input("Select an option: ")

        if choice == '1':
            book_appointment_receptionist()
        elif choice == '2':
            print("Logging out...")
            break
        else:
            print("Invalid choice.")

def book_appointment_receptionist():
    patient_name = input("Enter Patient Name: ")
    doctor_id = input("Enter Doctor ID: ")
    date = input("Enter Appointment Date (YYYY-MM-DD): ")
    cursor.execute("INSERT INTO Appointment (patient_id, doctor_id, date) VALUES ((SELECT patient_id FROM Patient WHERE name=?), ?, ?)", (patient_name, doctor_id, date))
    conn.commit()
    print(f"Appointment booked for {patient_name} with Doctor {doctor_id} on {date}.")

