#!/usr/bin/env python3
"""
Unit tests for the Library Management System
Tests core functionality including books, videos, magazines, and user management
"""

import os
import sys
import unittest

# Add parent directory to path to import library_system
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from library_system import (
    Book,
    Librarian,
    LibraryItem,
    LibrarySystem,
    Magazine,
    Member,
    Video,
)


class TestLibraryItem(unittest.TestCase):
    """Test cases for the abstract LibraryItem class"""

    def test_library_item_initialization(self):
        """Test that LibraryItem cannot be instantiated directly (abstract class)"""
        with self.assertRaises(TypeError):
            LibraryItem("Test", 2023, "Test")


class TestBook(unittest.TestCase):
    """Test cases for the Book class"""

    def setUp(self):
        """Set up test fixtures"""
        self.book = Book("Test Book", 2023, "Fiction", "Test Author", "1234567890")

    def test_book_initialization(self):
        """Test book initialization with correct attributes"""
        self.assertEqual(self.book.title, "Test Book")
        self.assertEqual(self.book.year, 2023)
        self.assertEqual(self.book.genre, "Fiction")
        self.assertEqual(self.book.author, "Test Author")
        self.assertEqual(self.book.isbn, "1234567890")
        self.assertTrue(self.book.is_available)

    def test_book_checkout(self):
        """Test book checkout functionality"""
        # First checkout should succeed
        result = self.book.checkout_item()
        self.assertIn("✅", result)
        self.assertIn("Test Book", result)
        self.assertFalse(self.book.is_available)

        # Second checkout should fail
        result = self.book.checkout_item()
        self.assertIn("❌", result)
        self.assertIn("already been checked out", result)

    def test_book_return(self):
        """Test book return functionality"""
        # Return without checkout should fail
        result = self.book.return_item()
        self.assertIn("❌", result)
        self.assertIn("was not checked out", result)

        # Checkout then return should succeed
        self.book.checkout_item()
        result = self.book.return_item()
        self.assertIn("✅", result)
        self.assertIn("Test Book", result)
        self.assertTrue(self.book.is_available)

    def test_book_description(self):
        """Test book description generation"""
        description = self.book.get_description()
        self.assertIn("Test Book", description)
        self.assertIn("Test Author", description)
        self.assertIn("2023", description)
        self.assertIn("Fiction", description)
        self.assertIn("1234567890", description)


class TestVideo(unittest.TestCase):
    """Test cases for the Video class"""

    def setUp(self):
        """Set up test fixtures"""
        self.video = Video("Test Video", 2023, "Action", "DVD", 120)

    def test_video_initialization(self):
        """Test video initialization with correct attributes"""
        self.assertEqual(self.video.title, "Test Video")
        self.assertEqual(self.video.year, 2023)
        self.assertEqual(self.video.genre, "Action")
        self.assertEqual(self.video.video_format, "DVD")
        self.assertEqual(self.video.duration, 120)
        self.assertTrue(self.video.is_available)
        self.assertTrue(self.video.video_id.startswith("VID"))

    def test_video_id_increment(self):
        """Test that video IDs increment properly"""
        video1 = Video("Video 1", 2023, "Action", "DVD", 120)
        video2 = Video("Video 2", 2023, "Action", "DVD", 120)
        self.assertNotEqual(video1.video_id, video2.video_id)

    def test_video_checkout_return(self):
        """Test video checkout and return functionality"""
        # Test checkout
        result = self.video.checkout_item()
        self.assertIn("✅", result)
        self.assertFalse(self.video.is_available)

        # Test return
        result = self.video.return_item()
        self.assertIn("✅", result)
        self.assertTrue(self.video.is_available)


class TestMagazine(unittest.TestCase):
    """Test cases for the Magazine class"""

    def setUp(self):
        """Set up test fixtures"""
        self.magazine = Magazine("Test Magazine", 2023, "Science", "Test Publisher")

    def test_magazine_initialization(self):
        """Test magazine initialization with correct attributes"""
        self.assertEqual(self.magazine.title, "Test Magazine")
        self.assertEqual(self.magazine.year, 2023)
        self.assertEqual(self.magazine.genre, "Science")
        self.assertEqual(self.magazine.publisher, "Test Publisher")
        self.assertTrue(self.magazine.is_available)
        self.assertTrue(self.magazine.magazine_id.startswith("MAG"))

    def test_magazine_id_increment(self):
        """Test that magazine IDs increment properly"""
        mag1 = Magazine("Mag 1", 2023, "Science", "Publisher")
        mag2 = Magazine("Mag 2", 2023, "Science", "Publisher")
        self.assertNotEqual(mag1.magazine_id, mag2.magazine_id)


class TestMember(unittest.TestCase):
    """Test cases for the Member class"""

    def setUp(self):
        """Set up test fixtures"""
        self.member = Member("John", "Doe", "john@test.com")
        self.book = Book("Test Book", 2023, "Fiction", "Test Author", "1234567890")

    def test_member_initialization(self):
        """Test member initialization with correct attributes"""
        self.assertEqual(self.member.fname, "John")
        self.assertEqual(self.member.lname, "Doe")
        self.assertEqual(self.member.email_address, "john@test.com")
        self.assertEqual(self.member.get_role(), "Member")
        self.assertTrue(self.member.member_id.startswith("MBR"))
        self.assertEqual(len(self.member.borrowed_items), 0)

    def test_member_borrow(self):
        """Test member borrowing functionality"""
        # Borrow available item
        result = self.member.borrow(self.book)
        self.assertIn("✅", result)
        self.assertIn(self.book, self.member.borrowed_items)

        # Try to borrow unavailable item
        result = self.member.borrow(self.book)
        self.assertIn("❌", result)
        self.assertIn("not available", result)

    def test_member_return(self):
        """Test member return functionality"""
        # Return item not in borrowed list
        result = self.member.return_item(self.book)
        self.assertIn("❌", result)
        self.assertIn("not in your borrowed list", result)

        # Borrow then return
        self.member.borrow(self.book)
        result = self.member.return_item(self.book)
        self.assertIn("✅", result)
        self.assertNotIn(self.book, self.member.borrowed_items)

    def test_list_borrowed_items(self):
        """Test listing borrowed items"""
        # Empty list
        result = self.member.list_borrowed_items()
        self.assertIn("No items currently borrowed", result)

        # With items
        self.member.borrow(self.book)
        result = self.member.list_borrowed_items()
        self.assertIn("Borrowed Items", result)
        self.assertIn("Test Book", result)


class TestLibrarian(unittest.TestCase):
    """Test cases for the Librarian class"""

    def setUp(self):
        """Set up test fixtures"""
        self.librarian = Librarian("Jane", "Smith", "jane@test.com")

    def test_librarian_initialization(self):
        """Test librarian initialization with correct attributes"""
        self.assertEqual(self.librarian.fname, "Jane")
        self.assertEqual(self.librarian.lname, "Smith")
        self.assertEqual(self.librarian.email_address, "jane@test.com")
        self.assertEqual(self.librarian.get_role(), "Librarian")
        self.assertTrue(self.librarian.librarian_id.startswith("LBR"))


class TestLibrarySystem(unittest.TestCase):
    """Test cases for the LibrarySystem class"""

    def setUp(self):
        """Set up test fixtures"""
        self.system = LibrarySystem()
        self.book = Book("Test Book", 2023, "Fiction", "Test Author", "1234567890")
        self.video = Video("Test Video", 2023, "Action", "DVD", 120)
        self.magazine = Magazine("Test Magazine", 2023, "Science", "Test Publisher")
        self.member = Member("John", "Doe", "john@test.com")
        self.librarian = Librarian("Jane", "Smith", "jane@test.com")

    def test_add_book(self):
        """Test adding books to the system"""
        result = self.system.add_book(self.book)
        self.assertIn("📚", result)
        self.assertIn("Test Book", result)
        self.assertIn(self.book.isbn, self.system.books)

    def test_add_video(self):
        """Test adding videos to the system"""
        result = self.system.add_video(self.video)
        self.assertIn("🎞️", result)
        self.assertIn("Test Video", result)
        self.assertIn(self.video.video_id, self.system.videos)

    def test_add_magazine(self):
        """Test adding magazines to the system"""
        result = self.system.add_magazine(self.magazine)
        self.assertIn("📰", result)
        self.assertIn("Test Magazine", result)
        self.assertIn(self.magazine.magazine_id, self.system.magazines)

    def test_register_member(self):
        """Test member registration"""
        result = self.system.register_member(self.member)
        self.assertEqual(result, self.member)
        self.assertIn(self.member.member_id, self.system.members)

    def test_register_librarian(self):
        """Test librarian registration"""
        result = self.system.register_librarian(self.librarian)
        self.assertEqual(result, self.librarian)
        self.assertIn(self.librarian.librarian_id, self.system.librarians)

    def test_checkout_book(self):
        """Test book checkout through the system"""
        self.system.add_book(self.book)
        self.system.register_member(self.member)

        result = self.system.checkout_book(self.book.isbn, self.member.member_id)
        self.assertIn("✅", result)
        self.assertFalse(self.book.is_available)

        # Test checkout with non-existent book
        result = self.system.checkout_book("invalid_isbn", self.member.member_id)
        self.assertIn("❌", result)
        self.assertIn("not found", result)

    def test_return_book(self):
        """Test book return through the system"""
        self.system.add_book(self.book)
        self.system.register_member(self.member)

        # Checkout first
        self.system.checkout_book(self.book.isbn, self.member.member_id)

        # Then return
        result = self.system.return_book(self.book.isbn, self.member.member_id)
        self.assertIn("✅", result)
        self.assertTrue(self.book.is_available)

    def test_find_functions(self):
        """Test find functions for all item types"""
        self.system.add_book(self.book)
        self.system.add_video(self.video)
        self.system.add_magazine(self.magazine)
        self.system.register_member(self.member)
        self.system.register_librarian(self.librarian)

        # Test find functions
        found_book = self.system.find_book_by_isbn(self.book.isbn)
        self.assertEqual(found_book, self.book)

        found_video = self.system.find_video_by_id(self.video.video_id)
        self.assertEqual(found_video, self.video)

        found_magazine = self.system.find_magazine_by_id(self.magazine.magazine_id)
        self.assertEqual(found_magazine, self.magazine)

        found_member = self.system.find_member(self.member.member_id)
        self.assertEqual(found_member, self.member)

        found_librarian = self.system.find_librarian(self.librarian.librarian_id)
        self.assertEqual(found_librarian, self.librarian)

    def test_preload_functions(self):
        """Test preload functions create sample data"""
        self.system.preload_sample_books()
        self.system.preload_sample_magazines()
        self.system.preload_sample_videos()
        self.system.preload_sample_members()

        # Check that sample data was created
        self.assertGreater(len(self.system.books), 0)
        self.assertGreater(len(self.system.magazines), 0)
        self.assertGreater(len(self.system.videos), 0)
        self.assertGreater(len(self.system.members), 0)


def run_tests():
    """Run all tests and display results"""
    print("🧪 Running Library Management System Tests...")
    print("=" * 50)

    # Create test suite
    test_suite = unittest.TestSuite()

    # Add test classes
    test_classes = [
        TestLibraryItem,
        TestBook,
        TestVideo,
        TestMagazine,
        TestMember,
        TestLibrarian,
        TestLibrarySystem,
    ]

    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Print summary
    print("=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.failures:
        print("\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")

    if result.errors:
        print("\n❌ Errors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")

    if not result.failures and not result.errors:
        print("\n✅ All tests passed successfully!")

    return result.wasSuccessful()


if __name__ == "__main__":
    run_tests()
