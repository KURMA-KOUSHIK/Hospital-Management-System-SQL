import sqlite3

def book_appointment(cursor, patient_id):
    print("Booking Appointment:")
    doctor_id = input("Enter doctor ID: ")

    cursor.execute('''
        INSERT INTO Appointment (patient_id, doctor_id, date)
        VALUES (?, ?, CURRENT_DATE)
    ''', (patient_id, doctor_id))
    cursor.connection.commit()
    print("Appointment booked successfully.")

def view_prescriptions(cursor, patient_id):
    print("Viewing Prescriptions:")
    cursor.execute('''
        SELECT name, cost FROM Medicine WHERE patient_id=?
    ''', (patient_id,))
    prescriptions = cursor.fetchall()

    if prescriptions:
        for medicine in prescriptions:
            print(f"Medicine: {medicine[0]}, Cost: {medicine[1]}")
    else:
        print("No prescriptions found.")

def pay_bill(cursor, patient_id):
    print("Paying Bill:")
    cursor.execute('''
        SELECT total_cost, status FROM Bill WHERE patient_id=?
    ''', (patient_id,))
    bill = cursor.fetchone()
    
    if bill:
        total_cost, status = bill
        if status == 'Pending':
            print(f"Total Cost: {total_cost}")
            confirm = input("Do you want to pay the bill? (yes/no): ")
            if confirm.lower() == 'yes':
                cursor.execute('''
                    UPDATE Bill SET status='Paid' WHERE patient_id=?
                ''', (patient_id,))
                cursor.connection.commit()
                print("Bill paid successfully.")
            else:
                print("Payment canceled.")
        else:
            print("Bill has already been paid.")
    else:
        print("No billing information found for this patient.")

def patient_menu(cursor, patient_id):
    while True:
        print("\n--- Patient Menu ---")
        print("1. Book Appointment")
        print("2. View Prescriptions")
        print("3. Pay Bill")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            book_appointment(cursor, patient_id)
        elif choice == "2":
            view_prescriptions(cursor, patient_id)
        elif choice == "3":
            pay_bill(cursor, patient_id)
        elif choice == "4":
            break
        else:
            print("Invalid choice.")
