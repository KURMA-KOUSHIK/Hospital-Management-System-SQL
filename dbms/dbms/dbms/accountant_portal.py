import sqlite3

def accountant_portal(conn, cursor):
    print("Welcome to the Accountant Portal!")
    while True:
        print("\n1. View Patients\n2. View Appointments\n3. View/Insert/Update Billing Records\n4. View Surgeries\n5. View Labs/Tests\n6. View Ambulance Services\n7. View Rooms\n8. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            # View Patients (View permission)
            cursor.execute("SELECT * FROM Patient")
            records = cursor.fetchall()
            if records:
                for record in records:
                    print(record)
            else:
                print("No patients found.")

        elif choice == "2":
            # View Appointments (View permission)
            cursor.execute("SELECT * FROM Appointment")
            records = cursor.fetchall()
            if records:
                for record in records:
                    print(record)
            else:
                print("No appointments found.")

        elif choice == "3":
            # View/Insert/Update Billing Records (Insert/Update permission includes View)
            action = input("Do you want to view, insert, or update a billing record? (view/insert/update): ").lower()
            if action == "view":
                billing_id = input("Enter Billing ID to view: ")
                cursor.execute("SELECT * FROM Bill WHERE bill_id=?", (billing_id,))
                record = cursor.fetchone()
                if record:
                    print(record)
                else:
                    print(f"No billing record found with ID {billing_id}.")
            elif action == "insert":
                patient_id = input("Enter Patient ID: ")
                total_cost = input("Enter Total Cost: ")
                room_id = input("Enter Room ID (optional, press Enter to skip): ")
                prescription_id = input("Enter Prescription ID (optional, press Enter to skip): ")
                insurance_id = input("Enter Insurance ID (optional, press Enter to skip): ")
                status = input("Enter Billing Status (e.g., Pending, Paid): ")

                # Optional values handling
                room_id = room_id if room_id else None
                prescription_id = prescription_id if prescription_id else None
                insurance_id = insurance_id if insurance_id else None

                cursor.execute('INSERT INTO Bill (patient_id, total_cost, room_id, prescription_id, insurance_id, status) VALUES (?, ?, ?, ?, ?, ?)', 
                               (patient_id, total_cost, room_id, prescription_id, insurance_id, status))
                conn.commit()
                print("Billing record inserted successfully.")
            elif action == "update":
                billing_id = input("Enter Billing ID to update: ")

                # Check if the billing_id exists
                cursor.execute("SELECT * FROM Bill WHERE bill_id=?", (billing_id,))
                existing_record = cursor.fetchone()

                if not existing_record:
                    print(f"Billing ID {billing_id} does not exist. Update operation canceled.")
                    continue

                available_columns = ['total_cost', 'status', 'room_id', 'prescription_id', 'insurance_id']
                print("Columns available for update:", available_columns)
                columns_to_update = input("Enter the columns you want to update (comma-separated): ").split(',')

                update_fields = []
                update_values = []

                for column in columns_to_update:
                    if column.strip() in available_columns:
                        new_value = input(f"Enter new value for {column.strip()}: ")
                        update_fields.append(f"{column.strip()}=?")
                        update_values.append(new_value)

                if update_fields:
                    update_values.append(billing_id)
                    query = f"UPDATE Bill SET {', '.join(update_fields)} WHERE bill_id=?"
                    cursor.execute(query, tuple(update_values))
                    conn.commit()
                    print("Billing record updated successfully.")
                else:
                    print("No valid columns selected for update.")

        elif choice == "4":
            # View Surgeries (View permission)
            cursor.execute("SELECT * FROM Surgeries")
            records = cursor.fetchall()
            if records:
                for record in records:
                    print(record)
            else:
                print("No surgeries found.")

        elif choice == "5":
            # View Labs/Tests (View permission)
            cursor.execute("SELECT * FROM LaboratoriesTests")
            records = cursor.fetchall()
            if records:
                for record in records:
                    print(record)
            else:
                print("No labs/tests found.")

        elif choice == "6":
            # View Ambulance Services (View permission)
            cursor.execute("SELECT * FROM AmbulanceServices")
            records = cursor.fetchall()
            if records:
                for record in records:
                    print(record)
            else:
                print("No ambulance services found.")

        elif choice == "7":
            # View Rooms (View permission)
            cursor.execute("SELECT * FROM Room")
            records = cursor.fetchall()
            if records:
                for record in records:
                    print(record)
            else:
                print("No rooms found.")

        elif choice == "8":
            # Exit
            break

        else:
            print("Invalid choice. Please try again.")
