import sqlite3

# Connect to the existing SQLite database
conn = sqlite3.connect('hospital_management_system.db')
cursor = conn.cursor()

# Function to insert predefined medicines
def insert_predefined_medicines():
    medicines = [
        ('Paracetamol', 5),
        ('Ibuprofen', 8),
        ('Amoxicillin', 15),
        ('Aspirin', 4),
        ('Cetirizine', 10),
        ('Metformin', 12),
        ('Atorvastatin', 20),
        ('Omeprazole', 18),
        ('Insulin', 30),
        ('Lisinopril', 25)
    ]
    
    cursor.executemany("INSERT INTO Medicine (name, cost) VALUES (?, ?)", medicines)
    conn.commit()
    print("Predefined medicines added successfully.")

# Function to insert predefined doctors (with phone numbers)
def insert_predefined_doctors():
    doctors = [
        ('Dr. John Smith', 'Cardiology', '123-456-7890'),
        ('Dr. Emily Davis', 'Dermatology', '234-567-8901'),
        ('Dr. Sarah Johnson', 'Neurology', '345-678-9012'),
        ('Dr. Michael Brown', 'Pediatrics', '456-789-0123'),
        ('Dr. Laura Wilson', 'Orthopedics', '567-890-1234'),
        ('Dr. David Moore', 'General Surgery', '678-901-2345'),
        ('Dr. Amanda Taylor', 'Gastroenterology', '789-012-3456'),
        ('Dr. James Anderson', 'ENT', '890-123-4567'),
        ('Dr. Susan Martin', 'Ophthalmology', '901-234-5678'),
        ('Dr. Chris Thompson', 'Psychiatry', '012-345-6789')
    ]
    
    cursor.executemany("INSERT INTO Doctor (d_name, specialty, ph_no) VALUES (?, ?, ?)", doctors)
    conn.commit()
    print("Predefined doctors added successfully.")

# Close the connection
def close_connection():
    conn.close()
    print("Database connection closed.")

# Example: Calling the functions to insert predefined data
if __name__ == "__main__":
    insert_predefined_medicines()
    insert_predefined_doctors()
    close_connection()