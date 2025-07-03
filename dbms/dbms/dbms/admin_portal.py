import sqlite3

def admin_portal(conn, cursor):
    print("Welcome to the Admin Portal!")
    while True:
        print("\n1. View all tables\n2. Insert Data\n3. Update Data\n4. Delete Data\n5. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            # View all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print("Available tables:", [table[0] for table in tables])
            table = input("Enter table name to view: ")

            if table:
                try:
                    cursor.execute(f"SELECT * FROM {table}")
                    records = cursor.fetchall()
                    for record in records:
                        print(record)
                except sqlite3.OperationalError as e:
                    print(f"Error: {e}")

        elif choice == "2":
            # Insert Data for all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [table[0] for table in cursor.fetchall()]
            print("Available tables:", tables)
            table = input("Enter table name to insert data: ")

            if table in tables:
                # Fetch column names for the chosen table
                cursor.execute(f"PRAGMA table_info({table})")
                columns = cursor.fetchall()
                column_names = [column[1] for column in columns if column[5] == 0]  # Skip the auto-increment columns

                # Prompt user to enter values for each column
                values = []
                for column in column_names:
                    value = input(f"Enter value for {column}: ")
                    values.append(value)

                # Dynamically build the INSERT statement
                placeholders = ', '.join('?' for _ in values)
                column_list = ', '.join(column_names)
                cursor.execute(f"INSERT INTO {table} ({column_list}) VALUES ({placeholders})", values)
                conn.commit()
                print(f"Data inserted into {table} successfully.")
            else:
                print("Table not found.")

        elif choice == "3":
            # Update Data for any table
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [table[0] for table in cursor.fetchall()]
            print("Available tables:", tables)
            table = input("Enter table name to update data: ")

            if table in tables:
                # Fetch column names for the chosen table
                cursor.execute(f"PRAGMA table_info({table})")
                columns = cursor.fetchall()
                column_names = [column[1] for column in columns]  # Include all columns

                # Display the primary key column name (assuming it's the first column)
                primary_key_column = columns[0][1]
                print(f"Primary key for {table}: {primary_key_column}")

                # Ask user for the primary key value to identify the record to update
                primary_key_value = input(f"Enter the {primary_key_column} value of the record to update: ")

                # Display available columns for the user to update
                print(f"Columns available for update: {column_names[1:]}")

                # Allow multiple column updates
                columns_to_update = input("Enter the columns you want to update (comma-separated): ").split(',')
                columns_to_update = [col.strip() for col in columns_to_update if col.strip() in column_names]

                if columns_to_update:
                    values = []
                    for column in columns_to_update:
                        new_value = input(f"Enter new value for {column}: ")
                        values.append(new_value)

                    # Build the dynamic update query for multiple columns
                    update_clause = ', '.join(f"{col} = ?" for col in columns_to_update)
                    query = f"UPDATE {table} SET {update_clause} WHERE {primary_key_column} = ?"
                    values.append(primary_key_value)  # Append the primary key value to the parameter list

                    # Execute the update
                    cursor.execute(query, values)
                    conn.commit()
                    print(f"Data in {table} updated successfully.")
                else:
                    print("No valid columns were selected for update.")
            else:
                print("Table not found.")

        elif choice == "4":
            # Delete Data for any table
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [table[0] for table in cursor.fetchall()]
            print("Available tables:", tables)
            table = input("Enter table name to delete data: ")

            if table in tables:
                # Fetch column names for the chosen table
                cursor.execute(f"PRAGMA table_info({table})")
                columns = cursor.fetchall()

                # Display the primary key column name (assuming it's the first column)
                primary_key_column = columns[0][1]
                print(f"Primary key for {table}: {primary_key_column}")

                # Ask user for the primary key value to identify the record to delete
                primary_key_value = input(f"Enter the {primary_key_column} value of the record to delete: ")

                # Confirm deletion
                confirmation = input(f"Are you sure you want to delete the record with {primary_key_column} = {primary_key_value}? (yes/no): ")

                if confirmation.lower() == 'yes':
                    cursor.execute(f"DELETE FROM {table} WHERE {primary_key_column} = ?", (primary_key_value,))
                    conn.commit()
                    print(f"Record with {primary_key_column} = {primary_key_value} deleted from {table}.")
                else:
                    print("Deletion canceled.")
            else:
                print("Table not found.")

        elif choice == "5":
            # Exit the portal
            break

        else:
            print("Invalid choice. Please try again.")
