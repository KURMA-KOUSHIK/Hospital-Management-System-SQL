import sqlite3

conn = sqlite3.connect('hospital_management_system.db')
cursor = conn.cursor()

def billing_menu():
    while True:
        print("\n--- Billing Portal ---")
        print("1. View Billing Information\n2. Mark as Paid\n3. Logout")
        choice = input("Select an option: ")

        if choice == '1':
            view_billing_info()
        elif choice == '2':
            mark_as_paid()
        elif choice == '3':
            print("Logging out...")
            break
        else:
            print("Invalid choice.")

def view_billing_info():
    patient_id = input("Enter Patient ID: ")
    cursor.execute("""
        SELECT b.bill_id, b.total_cost, b.status, b.insurance_applied, p.name
        FROM Bill b 
        JOIN Patient p ON b.patient_id = p.patient_id
        WHERE b.patient_id = ?
    """, (patient_id,))
    result = cursor.fetchone()

    if result:
        bill_id, total_cost, status, insurance_applied, patient_name = result
        insurance_status = 'Applied' if insurance_applied else 'Not Applied'
        print(f"\nBilling Information for Patient: {patient_name}")
        print(f"Bill ID: {bill_id}")
        print(f"Total Cost: {total_cost}")
        print(f"Status: {status}")
        print(f"Insurance: {insurance_status}")
    else:
        print("No billing information found for the given Patient ID.")

def mark_as_paid():
    patient_id = input("Enter Patient ID: ")
    cursor.execute("SELECT bill_id FROM Bill WHERE patient_id = ?", (patient_id,))
    result = cursor.fetchone()

    if result:
        bill_id = result[0]
        cursor.execute("UPDATE Bill SET status = 'Paid' WHERE bill_id = ?", (bill_id,))
        conn.commit()
        print(f"Bill ID: {bill_id} marked as 'Paid'.")
    else:
        print("No billing information found for the given Patient ID.")
