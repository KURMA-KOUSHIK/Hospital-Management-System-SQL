import sqlite3

def doctor_portal(conn, cursor, username):
    # Fetch doctor's ID from the Users table using the logged-in username
    cursor.execute("SELECT doctor_id FROM Users WHERE username=? AND role='Doctor'", (username,))
    doctor_record = cursor.fetchone()

    if not doctor_record:
        print("Doctor not found in the database or no doctor ID associated with this username.")
        return

    doctor_id = doctor_record[0]  # Get the doctor's ID
    print(f"Welcome to the Doctor Portal, Dr. {username}!")

    while True:
        print("\n1. View My Patients\n2. View Appointments\n3. View Billing\n4. View/Insert/Update Medicine\n5. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            # View patients associated with this doctor through appointments
            cursor.execute("""
                SELECT p.*
                FROM Patient p
                JOIN Appointment a ON p.patient_id = a.patient_id
                WHERE a.doctor_id = ?
            """, (doctor_id,))
            records = cursor.fetchall()

            if records:
                for record in records:
                    print(record)
            else:
                print("No patients found for this doctor.")

        elif choice == "2":
            # View Appointments for this doctor
            cursor.execute("SELECT * FROM Appointment WHERE doctor_id=?", (doctor_id,))
            records = cursor.fetchall()
            if records:
                for record in records:
                    print(record)
            else:
                print("No appointments found for this doctor.")

        elif choice == "3":
            # View Billing for patients under this doctor's care
            cursor.execute("""
                SELECT b.*
                FROM Bill b
                JOIN Appointment a ON b.patient_id = a.patient_id
                WHERE a.doctor_id = ?
            """, (doctor_id,))
            records = cursor.fetchall()
            if records:
                for record in records:
                    print(record)
            else:
                print("No billing records found for your patients.")

        elif choice == "4":
            # View/Insert/Update Medicine for this doctor's patients
            action = input("Do you want to view, insert, or update medicine records? (view/insert/update): ").lower()

            if action == "view":
                cursor.execute("""
                    SELECT m.*
                    FROM Medicine m
                    JOIN Appointment a ON m.patient_id = a.patient_id
                    WHERE a.doctor_id = ?
                """, (doctor_id,))
                records = cursor.fetchall()
                if records:
                    for record in records:
                        print(record)
                else:
                    print("No medicine records found for your patients.")

            elif action == "insert":
                patient_id = input("Enter Patient ID: ")

                # Check if the patient is under this doctor's care
                cursor.execute("SELECT * FROM Appointment WHERE patient_id=? AND doctor_id=?", (patient_id, doctor_id))
                appointment_record = cursor.fetchone()

                if appointment_record:
                    name = input("Enter medicine name: ")
                    cost = input("Enter medicine cost: ")

                    cursor.execute("""
                        INSERT INTO Medicine (name, cost, patient_id, doctor_id)
                        VALUES (?, ?, ?, ?)""",
                        (name, cost, patient_id, doctor_id))
                    conn.commit()
                    print("Medicine record inserted successfully.")
                else:
                    print("You do not have permission to add medicine for this patient.")

            elif action == "update":
                medicine_id = input("Enter Medicine ID: ")

                # Ensure the medicine belongs to the doctor's patient
                cursor.execute("""
                    SELECT m.medicine_id
                    FROM Medicine m
                    JOIN Appointment a ON m.patient_id = a.patient_id
                    WHERE m.medicine_id=? AND a.doctor_id=?
                """, (medicine_id, doctor_id))

                if cursor.fetchone():
                    available_columns = ['name', 'cost']
                    columns_to_update = input("Enter the columns you want to update (comma-separated): ").split(',')

                    update_fields = []
                    update_values = []

                    for column in columns_to_update:
                        if column.strip() in available_columns:
                            new_value = input(f"Enter new value for {column.strip()}: ")
                            update_fields.append(f"{column.strip()}=?")
                            update_values.append(new_value)

                    if update_fields:
                        update_values.append(medicine_id)
                        query = f"UPDATE Medicine SET {', '.join(update_fields)} WHERE medicine_id=?"
                        cursor.execute(query, tuple(update_values))
                        conn.commit()
                        print("Medicine record updated successfully.")
                    else:
                        print("No valid columns selected for update.")
                else:
                    print("You do not have permission to update this medicine record.")

        elif choice == "5":
            # Exit the portal
            break

        else:
            print("Invalid choice. Please try again.")
