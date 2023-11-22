import sqlite3

def delete_rejected_entries():
    # Connect to the SQLite database
    connection = sqlite3.connect('sample_library.db')
    cursor = connection.cursor()

    try:
        # Select entries that are reviewed but not approved
        cursor.execute("SELECT * FROM sample_library WHERE reviewed = 1 AND approved = 0")
        rejected_entries = cursor.fetchall()

        # If there are no rejected entries, exit
        if not rejected_entries:
            print("No rejected entries found.")
            return
        
        # Print out the rejected entries
        print("Rejected Entries:")
        for entry in rejected_entries:
            print(entry)
        
        # Ask for confirmation to delete
        confirmation = input("Do you want to delete these entries? (y/n): ").lower()

        if confirmation == 'y':
            # Delete the rejected entries
            cursor.execute("DELETE FROM sample_library WHERE reviewed = 1 AND approved = 0")
            
            print("Rejected entries deleted successfully.")

            # Commit the changes
            connection.commit()
        else:
            print("Deletion canceled.")

    finally:
        # Close the database connection
        connection.close()

if __name__ == "__main__":
    delete_rejected_entries()
