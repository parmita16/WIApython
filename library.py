import csv #to store csv file
import os 

from book import Book
from member import Student, Faculty
from exceptions import (
    BookNotFoundError,
    MemberNotFoundError,
    NoCopiesAvailableError,
    BorrowLimitReachedError,
    BookNotBorrowedError,
)


class Library:
    """
    This is the class that ties everything together.
    While the program is running, it keeps all books and members in
    memory as two dictionaries so lookups are fast. Every time
    something changes (a book is added, someone borrows a book and
    so on) it writes that change straight back into the csv files
    inside the data folder, so nothing is lost when the program is
    closed and everything comes back the next time it is opened.
    """

    def __init__(self, data_folder="data"):
        self.data_folder = data_folder
        self.books_file = os.path.join(data_folder, "books.csv")
        self.members_file = os.path.join(data_folder, "members.csv")
        self.borrowed_file = os.path.join(data_folder, "borrowed.csv")

        self.books = {}    # isbn maps to a Book object
        self.members = {}  # member_id maps to a Student or Faculty object

        os.makedirs(self.data_folder, exist_ok=True)
        self.load_data()

    # loading everything back from the csv files at startup

    def load_data(self):
        self.load_books()
        self.load_members()
        self.load_borrowed()

    def load_books(self):
        if not os.path.exists(self.books_file):
            return
        with open(self.books_file, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                book = Book(
                    row["isbn"],
                    row["title"],
                    row["author"],
                    row["total_copies"],
                    row["available_copies"],
                )
                self.books[book.isbn] = book

    def load_members(self):
        if not os.path.exists(self.members_file):
            return
        with open(self.members_file, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["member_type"] == "Faculty":
                    member = Faculty(row["member_id"], row["name"])
                else:
                    member = Student(row["member_id"], row["name"])
                self.members[member.member_id] = member

    def load_borrowed(self):
        if not os.path.exists(self.borrowed_file):
            return
        with open(self.borrowed_file, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                member = self.members.get(row["member_id"])
                if member:
                    member.borrowed_books.append(row["isbn"])

    # saving everything back into the csv files

    def save_books(self):
        with open(self.books_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["isbn", "title", "author", "total_copies", "available_copies"])
            for book in self.books.values():
                writer.writerow(book.to_row())

    def save_members(self):
        with open(self.members_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["member_id", "name", "member_type"])
            for member in self.members.values():
                writer.writerow(member.to_row())

    def save_borrowed(self):
        with open(self.borrowed_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["member_id", "isbn"])
            for member in self.members.values():
                for isbn in member.borrowed_books:
                    writer.writerow([member.member_id, isbn])

    def save_all(self):
        # called after almost every change so the csv files always match what is in memory
        self.save_books()
        self.save_members()
        self.save_borrowed()

    # book related operations

    def add_book(self, isbn, title, author, total_copies):
        if isbn in self.books:
            # the book already exists, so just add more copies to it
            # instead of creating a second entry with the same isbn
            book = self.books[isbn]
            book.total_copies += int(total_copies)
            book.available_copies += int(total_copies)
        else:
            self.books[isbn] = Book(isbn, title, author, total_copies)
        self.save_all()

    def find_book(self, isbn):
        book = self.books.get(isbn)
        if not book:
            raise BookNotFoundError(f"No book found with isbn {isbn}")
        return book

    def search_book(self, keyword):
        keyword = keyword.lower()
        results = []
        for book in self.books.values():
            if keyword in book.title.lower() or keyword in book.author.lower():
                results.append(book)
        return results

    def view_all_books(self):
        return list(self.books.values())

    # member related operations

    def register_member(self, member_id, name, member_type):
        if member_type.strip().lower() == "faculty":
            member = Faculty(member_id, name)
        else:
            member = Student(member_id, name)
        self.members[member_id] = member
        self.save_all()

    def find_member(self, member_id):
        member = self.members.get(member_id)
        if not member:
            raise MemberNotFoundError(f"No member found with id {member_id}")
        return member

    # issuing and returning books

    def issue_book(self, isbn, member_id):
        book = self.find_book(isbn)
        member = self.find_member(member_id)

        if book.available_copies <= 0:
            raise NoCopiesAvailableError(f"{book.title} has no copies available right now")

        if not member.can_borrow():
            raise BorrowLimitReachedError(f"{member.name} has already reached their borrowing limit")

        book.available_copies -= 1
        member.borrowed_books.append(isbn)
        self.save_all()

    def return_book(self, isbn, member_id):
        book = self.find_book(isbn)
        member = self.find_member(member_id)

        if isbn not in member.borrowed_books:
            raise BookNotBorrowedError(f"{member.name} did not borrow this book, so it cannot be returned")

        member.borrowed_books.remove(isbn)
        book.available_copies += 1
        self.save_all()
