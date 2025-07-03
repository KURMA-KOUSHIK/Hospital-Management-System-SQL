import sqlite3

conn = sqlite3.connect('hospital_management_system.db')
cursor = conn.cursor()

def nurse_menu(username, password):
    while True:
        print("\n--- Nurse Portal ---")
        print("1. Allot Room\n2. View Billing\n3. Logout")
        choice = input("Select an option: ")

        if choice == '1':
            allot_room(username)
        elif choice == '2':
            view_billing(username)
        elif choice == '3':
            print("Logging out...")
            break
        else:
            print("Invalid choice.")

def allot_room(username):
    print("\n--- Allot Room ---")
    patient_id = input("Enter Patient ID: ")
    room_type = input("Enter Room Type (Single/Shared): ")
    days = int(input("Enter Number of Days: "))
    cost_per_day = 1000 if room_type.lower() == 'single' else 500
    cursor.execute("INSERT INTO Room (patient_id, room_type, days, cost_per_day) VALUES (?, ?, ?, ?)", (patient_id, room_type, days, cost_per_day))
    conn.commit()
    print(f"Room allotted for Patient {patient_id} for {days} days at {cost_per_day} per day.")

def view_billing(username):
    print("\n--- View Billing ---")
    patient_id = input("Enter Patient ID: ")
    cursor.execute("SELECT total_cost, status, insurance_applied FROM Bill WHERE patient_id = ?", (patient_id,))
    rows = cursor.fetchall()
    for row in rows:
        insurance_status = 'Applied' if row[2] else 'Not Applied'
        print(f"Total Cost: {row[0]}, Status: {row[1]}, Insurance: {insurance_status}")

