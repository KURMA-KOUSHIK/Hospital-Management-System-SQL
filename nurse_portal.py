import sqlite3

def nurse_portal(conn, cursor):
    print("Welcome to the Nurse Portal!")
    while True:
        print("\n1. View Patients\n2. View Appointments\n3. View/Insert/Update Medical Records\n4. View Rooms\n5. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            # View Patients (View permission)
            cursor.execute("SELECT * FROM Patient")
            records = cursor.fetchall()
            if records:
                for record in records:
                    print(record)
            else:
                print("No records found in Patients.")

        elif choice == "2":
            # View Appointments (View permission)
            cursor.execute("SELECT * FROM Appointment")
            records = cursor.fetchall()
            if records:
                for record in records:
                    print(record)
            else:
                print("No records found in Appointments.")

        elif choice == "3":
            # View/Insert/Update Medical Records (Insert/Update permission includes View)
            action = input("Do you want to view, insert, or update medical records? (view/insert/update): ").lower()
            if action == "view":
                cursor.execute("SELECT * FROM MedicalRecords")
                records = cursor.fetchall()
                if records:
                    for record in records:
                        print(record)
                else:
                    print("No records found in MedicalRecords.")
            elif action == "insert":
                patient_id = input("Enter Patient ID: ")
                visit_date = input("Enter visit date (YYYY-MM-DD): ")
                diagnosis = input("Enter diagnosis: ")
                treatment = input("Enter treatment: ")
                notes = input("Enter notes: ")

                cursor.execute("INSERT INTO MedicalRecords (patient_id, visit_date, diagnosis, treatment, notes) VALUES (?, ?, ?, ?, ?)", 
                               (patient_id, visit_date, diagnosis, treatment, notes))
                conn.commit()
                print("Medical record inserted successfully.")

            elif action == "update":
                patient_id = input("Enter the Patient ID to update medical record: ")
                cursor.execute("SELECT * FROM MedicalRecords WHERE patient_id=?", (patient_id,))
                existing_record = cursor.fetchone()

                if not existing_record:
                    print(f"Patient ID {patient_id} does not exist. Update operation canceled.")
                    continue

                available_columns = ['visit_date', 'diagnosis', 'treatment', 'notes']
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
                    update_values.append(patient_id)
                    query = f"UPDATE MedicalRecords SET {', '.join(update_fields)} WHERE patient_id=?"
                    cursor.execute(query, tuple(update_values))
                    conn.commit()
                    print("Medical record updated successfully.")
                else:
                    print("No valid columns selected for update.")

        elif choice == "4":
            # View Rooms (View permission)
            cursor.execute("SELECT * FROM Room")
            records = cursor.fetchall()
            if records:
                for record in records:
                    print(record)
            else:
                print("No records found in Rooms.")

        elif choice == "5":
            # Exit the portal
            break

        else:
            print("Invalid choice. Please try again.")
