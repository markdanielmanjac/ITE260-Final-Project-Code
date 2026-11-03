# ==================================================
# ITE 260 - Computer Programming 1
# Library Management System - Librarian Managed
# Institution: PHINMA Cagayan de Oro College
# ==================================================

import json
import msvcrt
from pathlib import Path

LIBRARIAN_PASSWORD = "123456789"
STUDENTS_FILE = Path(__file__).with_name("students.json")
BOOKS_FILE = Path(__file__).with_name("books.json")

# ==================================================
# DATA STORAGE
# ==================================================

students = []

books = [
    [101, "Introduction to Physics", "John Smith", 3],
    [102, "College Algebra", "Maria Santos", 0],
    [103, "Computer Programming", "James Lee", 5],
    [104, "History of the Philippines", "Jose Reyes", 2]
]

# Borrowed books record
# Format:
# [Student ID, Book ID, Quantity]
borrowed_books = []


def load_students():
    try:
        saved_students = json.loads(STUDENTS_FILE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return []

    if not isinstance(saved_students, list) or any(
        not isinstance(student, list)
        or len(student) != 2
        or not isinstance(student[0], str)
        or not isinstance(student[1], str)
        for student in saved_students
    ):
        raise ValueError("Saved student data has an invalid format.")

    return saved_students


def save_students(student_list):
    STUDENTS_FILE.write_text(
        json.dumps(student_list, indent=2),
        encoding="utf-8"
    )


def load_books():
    try:
        saved_books = json.loads(BOOKS_FILE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return books

    if not isinstance(saved_books, list) or any(
        not isinstance(book, list)
        or len(book) != 4
        or type(book[0]) is not int
        or not isinstance(book[1], str)
        or not isinstance(book[2], str)
        or type(book[3]) is not int
        or book[3] < 0
        for book in saved_books
    ):
        raise ValueError("Saved book data has an invalid format.")

    return saved_books


def save_books(book_list):
    BOOKS_FILE.write_text(
        json.dumps(book_list, indent=2),
        encoding="utf-8"
    )


def input_integer(prompt, error_message, minimum=None):
    while True:
        value = input(prompt).strip()

        try:
            number = int(value)
        except ValueError:
            print(error_message)
            continue

        if minimum is not None and number < minimum:
            print(error_message)
            continue

        return number


# ==================================================
# LIBRARIAN AUTHENTICATION
# ==================================================

def librarian_login():
    print("\n" + "=" * 60)
    print("             LIBRARIAN LOGIN")
    print("=" * 60)

    password = get_hidden_password("Enter Librarian Password: ")

    if password == LIBRARIAN_PASSWORD:
        print("\n✅ Access Granted!")
        print("Welcome, Librarian.")
        return True
    else:
        print("\n❌ Access Denied!")
        print("Incorrect password.")
        return False


# ==================================================
# STUDENT MANAGEMENT
# ==================================================

def add_student():
    print("\n" + "-" * 60)
    print("                 ADD NEW STUDENT")
    print("-" * 60)

    while True:
        student_id = input("Enter Student ID: ").strip()

        if not student_id.isdigit():
            print("Invalid ❌ Student ID must be a number.")
            continue

        if any(student[0] == student_id for student in students):
            print("❌ Student ID already exists!")
            continue

        break

    while True:
        name = input("Enter Student Name: ").strip()

        if not name:
            print("❌ Student Name cannot be empty.")
        elif not all(character.isalpha() or character.isspace() for character in name):
            print("Invalid ❌ Student Name: letters only (spaces are allowed).")
        else:
            break

    new_student = [student_id, name]
    try:
        save_students(students + [new_student])
    except OSError as error:
        print(f"❌ Could not save the student: {error}")
        return

    students.append(new_student)

    print("\n✅ Student added successfully!")
    print(f"Student ID   : {student_id}")
    print(f"Student Name : {name}")


def view_all_students():
    print("\n" + "=" * 60)
    print("                  REGISTERED STUDENTS")
    print("=" * 60)

    if not students:
        print("No students registered yet.")
        return

    print(f"{'STUDENT ID':<20} {'STUDENT NAME'}")
    print("-" * 60)

    for student in students:
        print(f"{student[0]:<20} {student[1]}")

    print("-" * 60)


# ==================================================
# DISPLAY BOOKS
# ==================================================

def view_all_books():
    print("\n" + "=" * 85)
    print("                         ALL BOOKS")
    print("=" * 85)

    if not books:
        print("No books available in the library.")
        return

    print(
        f"{'BOOK ID':<15}"
        f"{'BOOK NAME':<30}"
        f"{'BOOK AUTHOR':<25}"
        f"{'BOOK AVAILABLE':<15}"
    )

    print("-" * 85)

    for book in books:
        print(
            f"{book[0]:<15}"
            f"{book[1]:<30}"
            f"{book[2]:<25}"
            f"{book[3]:<15}"
        )

    print("=" * 85)


# ==================================================
# ADD BOOK
# ==================================================

def add_book():
    print("\n" + "-" * 60)
    print("                    ADD NEW BOOK")
    print("-" * 60)

    while True:
        book_id = input_integer(
            "Enter BOOK ID: ",
            "❌ Invalid input! Book ID must be a number."
        )

        if find_book(book_id) is not None:
            print("\n❌ Book ID already exists!")
        else:
            break

    while True:
        book_name = input("Enter BOOK NAME: ").strip()
        if book_name:
            break
        print("❌ Book name cannot be empty.")

    while True:
        book_author = input("Enter BOOK AUTHOR: ").strip()
        if book_author:
            break
        print("❌ Book author cannot be empty.")

    quantity = input_integer(
        "Enter QUANTITY: ",
        "❌ Quantity must be a number greater than or equal to 0.",
        minimum=0
    )

    books.append([book_id, book_name, book_author, quantity])

    print("\n" + "=" * 60)
    print("✅ BOOK ADDED SUCCESSFULLY!")
    print("=" * 60)

    print(f"BOOK ID        : {book_id}")
    print(f"BOOK NAME      : {book_name}")
    print(f"BOOK AUTHOR    : {book_author}")
    print(f"BOOK AVAILABLE : {quantity}")


# ==================================================
# UPDATE BOOK
# ==================================================

def update_book():
    print("\n" + "-" * 60)
    print("                     UPDATE BOOK")
    print("-" * 60)

    if not books:
        print("No books available to update.")
        return

    # Show books first
    view_all_books()

    while True:
        book_id = input_integer(
            "\nEnter BOOK ID to update: ",
            "❌ Invalid Book ID. Please enter a number."
        )
        book_found = find_book(book_id)
        if book_found is not None:
            break
        print("\n❌ Book ID not found. Please try again.")

    print("\nCurrent Book Information")
    print("-" * 40)
    print(f"Book ID        : {book_found[0]}")
    print(f"Book Name      : {book_found[1]}")
    print(f"Book Author    : {book_found[2]}")
    print(f"Book Available : {book_found[3]}")
    print("-" * 40)

    print("\nPress ENTER if you want to keep the current information.")

    new_name = input(
        f"Enter New Book Name [{book_found[1]}]: "
    ).strip()

    new_author = input(
        f"Enter New Book Author [{book_found[2]}]: "
    ).strip()

    while True:
        new_quantity = input(
            f"Enter New Quantity [{book_found[3]}]: "
        ).strip()
        if not new_quantity:
            break
        if new_quantity.isdigit():
            break
        print("❌ Invalid input. Quantity must be a number greater than or equal to 0.")

    if new_name:
        book_found[1] = new_name

    if new_author:
        book_found[2] = new_author

    if new_quantity:
        book_found[3] = int(new_quantity)

    print("\n✅ Book updated successfully!")

    print("\nUpdated Book Information")
    print("-" * 40)
    print(f"Book ID        : {book_found[0]}")
    print(f"Book Name      : {book_found[1]}")
    print(f"Book Author    : {book_found[2]}")
    print(f"Book Available : {book_found[3]}")
    print("-" * 40)


# ==================================================
# REMOVE BOOK
# ==================================================

def remove_book():
    print("\n" + "-" * 60)
    print("                     REMOVE BOOK")
    print("-" * 60)

    if not books:
        print("No books available to remove.")
        return

    view_all_books()

    while True:
        book_id = input_integer(
            "\nEnter BOOK ID to remove: ",
            "❌ Invalid Book ID. Please enter a number."
        )
        book_index = next(
            (index for index, book in enumerate(books) if book[0] == book_id),
            None
        )
        if book_index is not None:
            break
        print("\n❌ Book ID not found. Please try again.")

    book = books[book_index]
    print("\nBook Found")
    print("-" * 40)
    print(f"Book ID        : {book[0]}")
    print(f"Book Name      : {book[1]}")
    print(f"Book Author    : {book[2]}")
    print(f"Book Available : {book[3]}")
    print("-" * 40)

    while True:
        confirm = input(
            "\nAre you sure you want to delete this book? (y/n): "
        ).strip().lower()
        if confirm in ("y", "n"):
            break
        print("❌ Please enter y or n.")

    if confirm == "y":
        books.pop(book_index)
        print("\n✅ Book removed successfully!")
    else:
        print("\nDeletion cancelled.")


# ==================================================
# FIND STUDENT
# ==================================================

def find_student(student_id):
    for student in students:
        if student[0] == student_id:
            return student

    return None


# ==================================================
# FIND BOOK
# ==================================================

def find_book(book_id):
    for book in books:
        if book[0] == book_id:
            return book

    return None


# ==================================================
# BORROW BOOK
# ==================================================

def borrow_book():
    print("\n" + "=" * 60)
    print("                     BORROW BOOK")
    print("=" * 60)

    # Check if students exist
    if not students:
        print("\n⚠️ No students registered yet.")
        print("Please add a student first.")
        return

    # Check if books exist
    if not books:
        print("\n⚠️ No books registered in the library.")
        return

    # Show all books before borrowing
    print("\nAVAILABLE BOOK INFORMATION")
    print("-" * 85)

    print(
        f"{'BOOK ID':<15}"
        f"{'BOOK NAME':<30}"
        f"{'BOOK AUTHOR':<25}"
        f"{'BOOK AVAILABLE':<15}"
    )

    print("-" * 85)

    for book in books:

        if book[3] > 0:
            print(
                f"{book[0]:<15}"
                f"{book[1]:<30}"
                f"{book[2]:<25}"
                f"{book[3]:<15}"
            )
        else:
            print(
                f"{book[0]:<15}"
                f"{book[1]:<30}"
                f"{book[2]:<25}"
                f"{'NOT AVAILABLE':<15}"
            )

    print("-" * 85)

    while True:
        student_id = input("\nEnter STUDENT ID: ").strip()
        student = find_student(student_id)
        if student is not None:
            break
        print("\n❌ Student not found! Please enter a registered student ID.")

    print(f"\nStudent Found: {student[1]}")

    while True:
        book_id = input_integer(
            "Enter BOOK ID to borrow: ",
            "❌ Invalid Book ID. Please enter a number."
        )
        book = find_book(book_id)
        if book is None:
            print("\n❌ Book ID not found. Please try again.")
        elif book[3] <= 0:
            print("\n❌ No copies available to borrow. Please choose another book.")
        else:
            break

    print("\nSelected Book")
    print("-" * 40)
    print(f"Book ID        : {book[0]}")
    print(f"Book Name      : {book[1]}")
    print(f"Book Author    : {book[2]}")
    print(f"Book Available : {book[3]}")
    print("-" * 40)

    while True:
        quantity = input_integer(
            "\nEnter QUANTITY to borrow: ",
            f"❌ Enter a quantity from 1 to {book[3]}.",
            minimum=1
        )
        if quantity > book[3]:
            print(f"\n❌ Only {book[3]} copy/copies are available.")
            continue
        break

    book[3] -= quantity

    existing_record = None
    for record in borrowed_books:
        if record[0] == student_id and record[1] == book_id:
            existing_record = record
            break

    if existing_record:
        existing_record[2] += quantity
    else:
        borrowed_books.append([student_id, book_id, quantity])

    print("\n" + "=" * 60)
    print("              BORROWING SUCCESSFUL")
    print("=" * 60)

    print(f"Student ID     : {student_id}")
    print(f"Student Name   : {student[1]}")
    print(f"Book ID        : {book[0]}")
    print(f"Book Name      : {book[1]}")
    print(f"Book Author    : {book[2]}")
    print(f"Quantity       : {quantity}")
    print(f"Remaining      : {book[3]}")

    print("=" * 60)


# ==================================================
# RETURN BOOK
# ==================================================

def return_book():
    print("\n" + "=" * 60)
    print("                     RETURN BOOK")
    print("=" * 60)

    if not borrowed_books:
        print("\n⚠️ There are currently no borrowed books.")
        return

    print("\nBORROWED BOOK RECORDS")
    print("-" * 85)

    print(
        f"{'STUDENT ID':<15}"
        f"{'BOOK ID':<15}"
        f"{'BOOK NAME':<30}"
        f"{'BORROWED':<15}"
    )

    print("-" * 85)

    for record in borrowed_books:

        student_id = record[0]
        book_id = record[1]
        quantity = record[2]

        book = find_book(book_id)

        if book:
            print(
                f"{student_id:<15}"
                f"{book_id:<15}"
                f"{book[1]:<30}"
                f"{quantity:<15}"
            )

    print("-" * 85)

    while True:
        student_id = input("\nEnter STUDENT ID: ").strip()
        student = find_student(student_id)
        if student is not None and any(
            record[0] == student_id for record in borrowed_books
        ):
            break
        print("\n❌ No borrowed books found for that student. Please try again.")

    while True:
        book_id = input_integer(
            "Enter BOOK ID to return: ",
            "❌ Invalid Book ID. Please enter a number."
        )
        book = find_book(book_id)
        borrowed_record = next(
            (
                record for record in borrowed_books
                if record[0] == student_id and record[1] == book_id
            ),
            None
        )
        if book is not None and borrowed_record is not None:
            break
        print("\n❌ This student has not borrowed that book. Please try again.")

    borrowed_quantity = borrowed_record[2]

    print("\nReturn Information")
    print("-" * 45)
    print(f"Student ID       : {student_id}")
    print(f"Student Name     : {student[1]}")
    print(f"Book ID          : {book[0]}")
    print(f"Book Name        : {book[1]}")
    print(f"Book Author      : {book[2]}")
    print(f"Borrowed Copies  : {borrowed_quantity}")
    print("-" * 45)

    while True:
        quantity = input_integer(
            "Enter QUANTITY to return: ",
            f"❌ Enter a quantity from 1 to {borrowed_quantity}.",
            minimum=1
        )
        if quantity <= borrowed_quantity:
            break
        print(f"❌ The student only borrowed {borrowed_quantity} copy/copies.")

    book[3] += quantity
    borrowed_record[2] -= quantity

    if borrowed_record[2] == 0:
        borrowed_books.remove(borrowed_record)

    print("\n" + "=" * 60)
    print("               RETURN SUCCESSFUL")
    print("=" * 60)

    print(f"Student ID       : {student_id}")
    print(f"Student Name     : {student[1]}")
    print(f"Book ID          : {book[0]}")
    print(f"Book Name        : {book[1]}")
    print(f"Book Author      : {book[2]}")
    print(f"Returned Copies  : {quantity}")
    print(f"Remaining Borrowed: {borrowed_quantity - quantity}")
    print(f"Book Available   : {book[3]}")

    print("=" * 60)


# ==================================================
# MAIN MENU
# ==================================================

def main_menu():

    while True:

        print("\n" + "=" * 60)
        print("           PHINMA COC LIBRARY MANAGEMENT")
        print("=" * 60)

        print("1.  Add Book")
        print("2.  Update Book")
        print("3.  Remove Book")
        print("4.  View All Books")
        print("5.  Borrow Book")
        print("6.  Return Book")
        print("7.  Add Student")
        print("8.  View All Students")
        print("9.  Exit")

        print("=" * 60)

        choice = input("Please Choice (1-9): ").strip()

        if choice == "1":
            add_book()

        elif choice == "2":
            update_book()

        elif choice == "3":
            remove_book()

        elif choice == "4":
            view_all_books()

        elif choice == "5":
            borrow_book()

        elif choice == "6":
            return_book()

        elif choice == "7":
            add_student()

        elif choice == "8":
            view_all_students()

        elif choice == "9":
            try:
                save_books(books)
            except OSError as error:
                print(f"\n❌ Could not save books: {error}")
                continue

            print("\n" + "=" * 60)
            print("Thank you for using the PHINMA COC")
            print("Library Management System!")
            print("=" * 60)
            break

        else:
            print("\n❌ Invalid choice!")
            print("Please enter a number from 1 to 9.")
            

def get_hidden_password(prompt):
    print(prompt, end="", flush=True)
    password = []

    while True:
        char = msvcrt.getwch()

        if char in ("\r", "\n"):
            print()
            return "".join(password)
        elif char == "\b":
            if password:
                password.pop()
                print("\b \b", end="", flush=True)
        elif char in ("\x00", "\xe0"):
            msvcrt.getwch()  # Ignore special keys
        else:
            password.append(char)
            print("*", end="", flush=True)

# ==================================================
# MAIN PROGRAM
# ==================================================

def main():

    print("\n" + "=" * 60)
    print("     WELCOME TO PHINMA COC LIBRARY MANAGEMENT")
    print("=" * 60)

    while not librarian_login():
        print("\nPlease try again.")

    try:
        students.extend(load_students())
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"\n❌ Could not load saved students: {error}")
        return

    try:
        books[:] = load_books()
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"\n❌ Could not load saved books: {error}")
        return

    main_menu()


# ==================================================
# RUN PROGRAM
# ==================================================

if __name__ == "__main__":
    main()
