import sqlite3

def receptionist_portal(conn, cursor):
    print("Welcome to the Receptionist Portal!")
    while True:
        print("\n1. Insert Patient\n2. Insert Appointment\n3. Insert Billing\n4. View/Update Appointment\n5. Delete Appointment\n6. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            # Insert Patient
            name = input("Name: ")
            age = input("Age: ")
            gender = input("Gender: ")
            dob = input("Date of Birth (YYYY-MM-DD): ")
            phone_number = input("Phone Number: ")
            
            cursor.execute('INSERT INTO Patient (name, age, gender, dob, phone_number) VALUES (?, ?, ?, ?, ?)', 
                           (name, age, gender, dob, phone_number))
            conn.commit()
            print("Patient added successfully.")

        elif choice == "2":
            # Insert Appointment
            patient_id = input("Enter Patient ID: ")
            doctor_id = input("Enter Doctor ID: ")
            date = input("Enter Appointment Date (YYYY-MM-DD): ")

            # Ensure both the patient and doctor exist
            cursor.execute("SELECT * FROM Patient WHERE patient_id=?", (patient_id,))
            patient_exists = cursor.fetchone()
            cursor.execute("SELECT * FROM Doctor WHERE doctor_id=?", (doctor_id,))
            doctor_exists = cursor.fetchone()

            if not patient_exists:
                print(f"Patient ID {patient_id} does not exist. Appointment creation failed.")
                continue
            if not doctor_exists:
                print(f"Doctor ID {doctor_id} does not exist. Appointment creation failed.")
                continue
            
            cursor.execute('INSERT INTO Appointment (patient_id, doctor_id, date) VALUES (?, ?, ?)', 
                           (patient_id, doctor_id, date))
            conn.commit()
            print("Appointment created successfully.")

        elif choice == "3":
            # Insert Billing
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
            print("Billing record created successfully.")

        elif choice == "4":
            # View/Update Appointment
            action = input("Do you want to view or update an appointment? (view/update): ").lower()
            if action == "view":
                appointment_id = input("Enter Appointment ID to view: ")
                cursor.execute("SELECT * FROM Appointment WHERE appointment_id=?", (appointment_id,))
                record = cursor.fetchone()
                if record:
                    print(record)
                else:
                    print(f"No appointment found with ID {appointment_id}.")
            elif action == "update":
                appointment_id = input("Enter Appointment ID to update: ")
                cursor.execute("SELECT * FROM Appointment WHERE appointment_id=?", (appointment_id,))
                existing_record = cursor.fetchone()

                if not existing_record:
                    print(f"Appointment ID {appointment_id} does not exist. Update operation canceled.")
                    continue

                available_columns = ['date']
                print("Columns available for update:", available_columns)
                column_to_update = input("Enter the column you want to update: ").strip()

                if column_to_update in available_columns:
                    new_value = input(f"Enter new value for {column_to_update}: ")
                    query = f"UPDATE Appointment SET {column_to_update}=? WHERE appointment_id=?"
                    cursor.execute(query, (new_value, appointment_id))
                    conn.commit()
                    print("Appointment updated successfully.")
                else:
                    print("Invalid column selected for update.")

        elif choice == "5":
            # Delete Appointment
            appointment_id = input("Enter Appointment ID to delete: ")
            cursor.execute("SELECT * FROM Appointment WHERE appointment_id=?", (appointment_id,))
            existing_record = cursor.fetchone()

            if not existing_record:
                print(f"Appointment ID {appointment_id} does not exist. Deletion operation canceled.")
                continue

            cursor.execute('DELETE FROM Appointment WHERE appointment_id=?', (appointment_id,))
            conn.commit()
            print("Appointment deleted successfully.")

        elif choice == "6":
            # Exit the portal
            break

        else:
            print("Invalid choice. Please try again.")
