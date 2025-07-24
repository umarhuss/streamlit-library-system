from abc import ABC, abstractmethod


# Abstract class for Library items
class LibraryItem(ABC):
    # Initialise class
    def __init__(self, title, year, genre):
        self.title = title
        self.year = year
        self.genre = genre
        self.is_available = True

    # Methods for child class to inherit
    @abstractmethod
    def checkout_item(self) -> str:
        """Mark item as checked out"""
        pass

    @abstractmethod
    def get_description(self) -> str:
        """Get a string description of the item"""
        pass

    @abstractmethod
    def return_item(self) -> str:
        """Mark item as returned"""
        pass


# Book class inherited from library class
class Book(LibraryItem):
    def __init__(self, title, year, genre, author, isbn):
        super().__init__(title, year, genre)
        self.author = author
        self.isbn = isbn

    # Check out book logic
    def checkout_item(self):
        # Check if book is available
        if not self.is_available:
            return f"❌ {self.title} has already been checked out"
        # If book is available to check out
        self.is_available = False
        return f" ✅ You have successfully checked out\n{self.title}\nISBN: {self.isbn}"

    # Get description of book logic
    def get_description(self):
        return (
            f"{self.title}\n{self.author}\n{self.year}\n{self.genre}\nISBN: {self.isbn}"
        )

    # Return book logic
    def return_item(self):
        if self.is_available:
            return f"❌ {self.title} was not checked out"
        self.is_available = True
        return f" ✅ You have successfully returned\n{self.title}\nISBN: {self.isbn}"


# Video class inherited from library item
class Video(LibraryItem):
    # Counter for video ID
    video_counter = 1

    def __init__(self, title, year, genre, video_format, duration):
        super().__init__(title, year, genre)
        self.video_format = video_format
        self.duration = duration
        self.video_id = f"VID{Video.video_counter:04d}"
        Video.video_counter += 1

    # Check out video logic
    def checkout_item(self):
        # Check if book is available
        if not self.is_available:
            return f"❌ {self.title} has already been checked out"
        # If book is available to check out
        self.is_available = False
        return (
            f"✅ You have successfully checked out\n{self.title}\nID: {self.video_id}"
        )

    # Get description of video logic
    def get_description(self):
        return (
            f"🎬 {self.title}\n"
            f"📅 {self.year} | 🎭 {self.genre}\n"
            f"💾 Format: {self.video_format} | ⏱️ Duration: {self.duration} mins\n"
            f"🆔 ID: {self.video_id}"
        )

    # Return video logic
    def return_item(self):
        if self.is_available:
            return f"❌ {self.title} was not checked out"
        self.is_available = True
        return f"✅ You have successfully returned\n{self.title}\nID: {self.video_id}"


# Magazine inherited from library item
class Magazine(LibraryItem):
    magazine_counter = 1

    def __init__(self, title, year, genre, publisher):
        super().__init__(title, year, genre)
        self.publisher = publisher
        self.magazine_id = f"MAG{Magazine.magazine_counter:04d}"
        Magazine.magazine_counter += 1

    # Check out Magazine logic
    def checkout_item(self):
        # Check if magazine is available
        if not self.is_available:
            return f"❌ {self.title} has already been checked out"
        # If magazine is available to check out
        self.is_available = False
        return f"✅ You have successfully checked out\n{self.title}\nID: {self.magazine_id}"

    # Get description of Magazine logic
    def get_description(self):
        return (
            f"📖 {self.title}\n"
            f"📅 {self.year} | 🎭 {self.genre}\n"
            f"📰 Publisher: {self.publisher}\n"
            f"🆔 ID: {self.magazine_id}"
        )

    # Return Magazine logic
    def return_item(self):
        if self.is_available:
            return f"❌ {self.title} was not checked out"
        self.is_available = True
        return (
            f"✅ You have successfully returned\n{self.title}\nID: {self.magazine_id}"
        )


# Person ABC class
class Person(ABC):
    def __init__(self, fname, lname, email_address):
        self.fname = fname
        self.lname = lname
        self.email_address = email_address

    @abstractmethod
    def get_role(self) -> str:
        """Return the role of the person (e.g., 'Member', 'Librarian')"""
        pass


# Member class inherited from Person
class Member(Person):
    # Class variable for incrementing IDs
    id_counter = 1

    def __init__(self, fname, lname, email_address):
        super().__init__(fname, lname, email_address)
        self.member_id = f"MBR{Member.id_counter:04d}"
        Member.id_counter += 1
        self.borrowed_items = []

    def get_role(self):
        return "Member"

    def borrow(self, item: LibraryItem):
        if not item.is_available:
            return f"❌ {item.title} is not available for borrowing"
        self.borrowed_items.append(item)
        return item.checkout_item()

    def return_item(self, item: LibraryItem):
        if item not in self.borrowed_items:
            return f"❌ {item.title} is not in your borrowed list"
        self.borrowed_items.remove(item)
        return item.return_item()

    def list_borrowed_items(self):
        if not self.borrowed_items:
            return "📭 No items currently borrowed."
        return "📚 Borrowed Items:\n" + "\n".join(
            [
                f"- {item.title} ({item.__class__.__name__})"
                for item in self.borrowed_items
            ]
        )


class Librarian(Person):
    def __init__(self, fname, lname, email_address):
        super().__init__(fname, lname, email_address)
        self.librarian_id = f"LBR{Member.id_counter:04d}"
        Member.id_counter += 1
        self.registered_items = []

    def get_role(self):
        return "Librarian"

    def list_registered_items(self):
        if not self.registered_items:
            return "🗂️ No items registered yet."
        return "📋 Items Registered:\n" + "\n".join(
            [
                f"- {item.title} ({item.__class__.__name__})"
                for item in self.registered_items
            ]
        )


class LibrarySystem:
    def __init__(self):
        self.books = {}  # Key: ISBN, Value: Book object
        self.videos = {}  # Key: Video ID, Value: Video object
        self.magazines = {}  # Key: Magazine ID, Value: Magazine object
        self.members = {}  # Key: Member ID, Value: Member object
        self.librarians = {}  # Key: Librarian ID, Value: Librarian object

    # Book Operations

    def add_book(self, book: Book):
        self.books[book.isbn] = book
        return f"📚 Book '{book.title}' added successfully."

    def find_book_by_isbn(self, isbn):
        return self.books.get(isbn)

    def checkout_book(self, isbn, member_id):
        book = self.find_book_by_isbn(isbn)
        member = self.members.get(member_id)

        if not book:
            return "❌ Book not found."
        if not member:
            return "❌ Member not found."

        return member.borrow(book)

    def return_book(self, isbn, member_id):
        book = self.find_book_by_isbn(isbn)
        member = self.members.get(member_id)

        if not book or not member:
            return "❌ Book or member not found."
        return member.return_item(book)

    # Video Operations

    def add_video(self, video):
        self.videos[video.video_id] = video
        return f"🎞️ Video '{video.title}' added successfully."

    def find_video_by_id(self, video_id):
        return self.videos.get(video_id)

    def checkout_video(self, video_id, member_id):
        video = self.find_video_by_id(video_id)
        member = self.members.get(member_id)

        if not video:
            return "❌ Video not found."
        if not member:
            return "❌ Member not found."

        return member.borrow(video)

    def return_video(self, video_id, member_id):
        video = self.find_video_by_id(video_id)
        member = self.members.get(member_id)

        if not video or not member:
            return "❌ Video or member not found."
        return member.return_item(video)

    # Magazine Operations

    def add_magazine(self, magazine):
        self.magazines[magazine.magazine_id] = magazine
        return f"📰 Magazine '{magazine.title}' added successfully."

    def find_magazine_by_id(self, magazine_id):
        return self.magazines.get(magazine_id)

    def checkout_magazine(self, magazine_id, member_id):
        magazine = self.find_magazine_by_id(magazine_id)
        member = self.members.get(member_id)

        if not magazine:
            return "❌ Magazine not found."
        if not member:
            return "❌ Member not found."

        return member.borrow(magazine)

    def return_magazine(self, magazine_id, member_id):
        magazine = self.find_magazine_by_id(magazine_id)
        member = self.members.get(member_id)

        if not magazine or not member:
            return "❌ Magazine or member not found."
        return member.return_item(magazine)

    # Member Management

    def register_member(self, member):
        self.members[member.member_id] = member
        return f"👤 Member '{member.fname} {member.lname}' registered successfully."

    def find_member(self, member_id):
        return self.members.get(member_id)

    # Librarian Management

    def register_librarian(self, librarian):
        self.librarians[librarian.librarian_id] = librarian
        return f"🧑‍🏫 Librarian '{librarian.fname} {librarian.lname}' registered successfully."

    def find_librarian(self, librarian_id):
        return self.librarians.get(librarian_id)
