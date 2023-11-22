import sqlite3

def review_entries(cursor):
    cursor.execute("SELECT * FROM sample_library WHERE reviewed = 0")
    unreviewed_entries = cursor.fetchall()
    for entry in unreviewed_entries:
        print("ID:", entry[0])
        print("Book Name:", entry[1])
        print("Author:", entry[2])
        print("Webpage:", entry[3])
        print("Tags:", entry[4])
        print("Excerpt:", entry[5])
        print("Male Pronouns:", entry[6])
        print("Female Pronouns:", entry[7])
        print("Name Matches:", entry[8])
        print()

        approval = input("Approve (y) or Reject (n): ")
        if approval.lower() == 'y':
            update_review_status(cursor, entry[0], True)
        elif approval.lower() == 'n':
            update_review_status(cursor, entry[0], False)
        else:
            print("Invalid input. Entry will remain unreviewed.\n")

def update_review_status(cursor, entry_id, approval):
    cursor.execute("UPDATE sample_library SET reviewed = 1, approved = ? WHERE id = ?", (approval, entry_id))
    cursor.connection.commit()

def main():
    # Connect to the SQLite database
    connection = sqlite3.connect('sample_library.db')
    cursor = connection.cursor()

    try:
        print("Unreviewed Entries:")
        print("-------------------")
        review_entries(cursor)
        
    finally:
        # Close the database connection
        connection.close()

if __name__ == "__main__":
    main()
