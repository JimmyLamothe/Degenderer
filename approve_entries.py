"""
This script is used to review and approve samples submitted by users.

It goes through all the unreviewed samples in sample_library.db and lets
the user approve, reject or pass on each. Approved samples can be displayed
in the samples page. Rejected samples can be deleted with delete_rejected.py

Possible improvements:

Add a rating to each entry. This could be used to prioritize samples for display.
Add the date added to each entry. This could also be used to prioritize newer samples.
"""
import sqlite3

def review_entries(cursor):
    """ Ask user to approve a single submission """
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
    """ Change review status for a submission """
    cursor.execute("UPDATE sample_library SET reviewed = 1, approved = ? WHERE id = ?",
                   (approval, entry_id))
    cursor.connection.commit()

def main():
    """ Connect to database and ask user to approve all unreviewed submissions """
    connection = sqlite3.connect('sample_library.db')
    cursor = connection.cursor()

    try:
        print("Unreviewed Entries:")
        print("-------------------")
        review_entries(cursor)

    finally:
        connection.close()

if __name__ == "__main__":
    main()
