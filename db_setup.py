import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('hospital.db')
cursor = conn.cursor()

# Create Staff Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Staff (
    staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
    s_name TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    salary REAL NOT NULL,
    role TEXT NOT NULL
)
''')

# Create Patient Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Patient (
    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    gender TEXT NOT NULL,
    dob DATE NOT NULL,
    phone_number TEXT NOT NULL,
    nurse_id INTEGER,
    FOREIGN KEY (nurse_id) REFERENCES Nurse (nurse_id)
)
''')

# Create Doctor Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Doctor (
    doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    d_name TEXT NOT NULL,
    specialty TEXT NOT NULL,
    phone_number TEXT NOT NULL
)
''')

# Create Nurse Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Nurse (
    nurse_id INTEGER PRIMARY KEY AUTOINCREMENT,
    n_name TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    room_id INTEGER,
    FOREIGN KEY (room_id) REFERENCES Room (room_id)
)
''')

# Create Receptionist Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Receptionist (
    receptionist_id INTEGER PRIMARY KEY AUTOINCREMENT,
    r_name TEXT NOT NULL,
    phone_number TEXT NOT NULL
)
''')

# Create Room Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Room (
    room_id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_type TEXT NOT NULL,
    availability BOOLEAN NOT NULL DEFAULT 1,
    room_cost REAL NOT NULL
)
''')

# Create Appointment Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Appointment (
    appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    doctor_id INTEGER,
    date DATE NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES Patient (patient_id),
    FOREIGN KEY (doctor_id) REFERENCES Doctor (doctor_id)
)
''')

# Create Medicine Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Medicine (
    medicine_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    cost REAL NOT NULL,
    patient_id INTEGER,
    doctor_id INTEGER,
    FOREIGN KEY (patient_id) REFERENCES Patient (patient_id),
    FOREIGN KEY (doctor_id) REFERENCES Doctor (doctor_id)
)
''')

# Create Bill Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Bill (
    bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    total_cost REAL NOT NULL,
    room_id INTEGER,
    prescription_id INTEGER,
    insurance_id INTEGER,
    status TEXT NOT NULL DEFAULT 'Pending',
    FOREIGN KEY (patient_id) REFERENCES Patient (patient_id),
    FOREIGN KEY (room_id) REFERENCES Room (room_id),
    FOREIGN KEY (insurance_id) REFERENCES Insurance (insurance_id)
)
''')

# Create Insurance Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Insurance (
    insurance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    policy_number TEXT NOT NULL,
    coverage_details REAL NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES Patient (patient_id)
)
''')

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database and tables created successfully.")
