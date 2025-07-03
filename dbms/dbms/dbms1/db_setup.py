import sqlite3

# Connect to SQLite (or create the database if it doesn't exist)
conn = sqlite3.connect('hospital_management_system.db')
cursor = conn.cursor()

# Create the Patient table
cursor.execute('''CREATE TABLE IF NOT EXISTS Patient (
                    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    gender TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    phonenumber TEXT NOT NULL,
                    DOB DATE NOT NULL
                )''')
print("Patient table created.")

# Create the Doctor table
cursor.execute('''CREATE TABLE IF NOT EXISTS Doctor (
                    doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    d_name TEXT NOT NULL,
                    specialty TEXT NOT NULL,
                    ph_no TEXT NOT NULL
                )''')
print("Doctor table created.")

# Create the Nurse table
cursor.execute('''CREATE TABLE IF NOT EXISTS Nurse (
                    nurse_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone_no TEXT NOT NULL
                )''')
print("Nurse table created.")

# Create the Room table
cursor.execute('''CREATE TABLE IF NOT EXISTS Room (
                    room_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    room_number TEXT NOT NULL,
                    room_type TEXT NOT NULL CHECK (room_type IN ('ICU', 'general')),
                    availability TEXT NOT NULL CHECK (availability IN ('Available', 'Occupied')),
                    room_cost INTEGER NOT NULL,
                    nurse_id INTEGER,
                    FOREIGN KEY (nurse_id) REFERENCES Nurse(nurse_id)
                )''')
print("Room table created.")

# Create the Appointment table
cursor.execute('''CREATE TABLE IF NOT EXISTS Appointment (
                    appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id INTEGER,
                    doctor_id INTEGER,
                    appointment_date DATE NOT NULL,
                    appointment_time TIME NOT NULL,
                    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id),
                    FOREIGN KEY (doctor_id) REFERENCES Doctor(doctor_id)
                )''')
print("Appointment table created.")

# Create the Medicine table
cursor.execute('''CREATE TABLE IF NOT EXISTS Medicine (
                    medicine_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    cost INTEGER NOT NULL
                )''')
print("Medicine table created.")

# Create the Bill table
cursor.execute('''CREATE TABLE IF NOT EXISTS Bill (
                    bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id INTEGER,
                    room_id INTEGER,
                    appointment_id INTEGER,
                    prescription_id INTEGER,
                    total_cost INTEGER NOT NULL,
                    status TEXT NOT NULL CHECK (status IN ('Paid', 'Pending')),
                    insurance_applied BOOLEAN NOT NULL CHECK (insurance_applied IN (0, 1)),
                    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id),
                    FOREIGN KEY (room_id) REFERENCES Room(room_id),
                    FOREIGN KEY (appointment_id) REFERENCES Appointment(appointment_id),
                    FOREIGN KEY (prescription_id) REFERENCES Medicine(medicine_id)
                )''')
print("Bill table created.")

# Create the Insurance table
cursor.execute('''CREATE TABLE IF NOT EXISTS Insurance (
                    insurance_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    policy_number TEXT NOT NULL,
                    coverage_details TEXT NOT NULL,
                    patient_id INTEGER,
                    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id)
                )''')
print("Insurance table created.")

# Commit the changes to save the table creation
conn.commit()

# Close the connection
conn.close()

print("Database setup completed successfully.")