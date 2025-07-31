#!/usr/bin/env python3
"""
Integration tests for the Library Management System
Tests complete workflows and user scenarios
"""

import os
import sys
import unittest

# Add parent directory to path to import library_system
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from library_system import Book, Librarian, LibrarySystem, Magazine, Member, Video


class TestLibraryWorkflows(unittest.TestCase):
    """Integration tests for complete library workflows"""

    def setUp(self):
        """Set up test fixtures"""
        self.system = LibrarySystem()

        # Create sample data
        self.book1 = Book(
            "Python Programming",
            2023,
            "Computer Science",
            "John Smith",
            "9780123456789",
        )
        self.book2 = Book(
            "Data Science", 2023, "Computer Science", "Jane Doe", "9780987654321"
        )
        self.video1 = Video("Python Tutorial", 2023, "Educational", "Digital", 60)
        self.magazine1 = Magazine("Tech Weekly", 2023, "Technology", "Tech Publishers")

        self.member1 = Member("Alice", "Johnson", "alice@test.com")
        self.member2 = Member("Bob", "Brown", "bob@test.com")
        self.librarian1 = Librarian("Carol", "Wilson", "carol@library.com")

        # Add items to system
        self.system.add_book(self.book1)
        self.system.add_book(self.book2)
        self.system.add_video(self.video1)
        self.system.add_magazine(self.magazine1)

        # Register users
        self.system.register_member(self.member1)
        self.system.register_member(self.member2)
        self.system.register_librarian(self.librarian1)

    def test_complete_member_workflow(self):
        """Test complete workflow for a member borrowing and returning items"""
        # Member borrows multiple items
        result1 = self.system.checkout_book(self.book1.isbn, self.member1.member_id)
        self.assertIn("✅", result1)

        result2 = self.system.checkout_video(
            self.video1.video_id, self.member1.member_id
        )
        self.assertIn("✅", result2)

        result3 = self.system.checkout_magazine(
            self.magazine1.magazine_id, self.member1.member_id
        )
        self.assertIn("✅", result3)

        # Check that items are in member's borrowed list
        self.assertIn(self.book1, self.member1.borrowed_items)
        self.assertIn(self.video1, self.member1.borrowed_items)
        self.assertIn(self.magazine1, self.member1.borrowed_items)

        # Check that items are marked as unavailable
        self.assertFalse(self.book1.is_available)
        self.assertFalse(self.video1.is_available)
        self.assertFalse(self.magazine1.is_available)

        # Member returns items
        result4 = self.system.return_book(self.book1.isbn, self.member1.member_id)
        self.assertIn("✅", result4)

        result5 = self.system.return_video(self.video1.video_id, self.member1.member_id)
        self.assertIn("✅", result5)

        result6 = self.system.return_magazine(
            self.magazine1.magazine_id, self.member1.member_id
        )
        self.assertIn("✅", result6)

        # Check that items are removed from borrowed list
        self.assertNotIn(self.book1, self.member1.borrowed_items)
        self.assertNotIn(self.video1, self.member1.borrowed_items)
        self.assertNotIn(self.magazine1, self.member1.borrowed_items)

        # Check that items are available again
        self.assertTrue(self.book1.is_available)
        self.assertTrue(self.video1.is_available)
        self.assertTrue(self.magazine1.is_available)

    def test_multiple_members_workflow(self):
        """Test workflow with multiple members borrowing different items"""
        # Member 1 borrows book 1
        result1 = self.system.checkout_book(self.book1.isbn, self.member1.member_id)
        self.assertIn("✅", result1)

        # Member 2 tries to borrow the same book (should fail)
        result2 = self.system.checkout_book(self.book1.isbn, self.member2.member_id)
        self.assertIn("❌", result2)
        self.assertIn("not available", result2)

        # Member 2 borrows book 2 (should succeed)
        result3 = self.system.checkout_book(self.book2.isbn, self.member2.member_id)
        self.assertIn("✅", result3)

        # Check that each member has their own borrowed items
        self.assertIn(self.book1, self.member1.borrowed_items)
        self.assertNotIn(self.book1, self.member2.borrowed_items)
        self.assertIn(self.book2, self.member2.borrowed_items)
        self.assertNotIn(self.book2, self.member1.borrowed_items)

    def test_error_handling_workflow(self):
        """Test error handling in various scenarios"""
        # Try to checkout non-existent item
        result1 = self.system.checkout_book("invalid_isbn", self.member1.member_id)
        self.assertIn("❌", result1)
        self.assertIn("not found", result1)

        # Try to checkout with non-existent member
        result2 = self.system.checkout_book(self.book1.isbn, "invalid_member_id")
        self.assertIn("❌", result2)
        self.assertIn("not found", result2)

        # Try to return item that wasn't borrowed
        result3 = self.system.return_book(self.book1.isbn, self.member1.member_id)
        self.assertIn("❌", result3)
        self.assertIn("not in your borrowed list", result3)

        # Try to return item borrowed by different member
        self.system.checkout_book(self.book1.isbn, self.member1.member_id)
        result4 = self.system.return_book(self.book1.isbn, self.member2.member_id)
        self.assertIn("❌", result4)
        self.assertIn("not in your borrowed list", result4)

    def test_library_inventory_management(self):
        """Test library inventory management functionality"""
        # Check initial inventory
        self.assertEqual(len(self.system.books), 2)
        self.assertEqual(len(self.system.videos), 1)
        self.assertEqual(len(self.system.magazines), 1)
        self.assertEqual(len(self.system.members), 2)
        self.assertEqual(len(self.system.librarians), 1)

        # Add new items
        new_book = Book("New Book", 2024, "Fiction", "New Author", "9781111111111")
        new_video = Video("New Video", 2024, "Action", "Blu-Ray", 90)
        new_magazine = Magazine("New Magazine", 2024, "Science", "New Publisher")

        self.system.add_book(new_book)
        self.system.add_video(new_video)
        self.system.add_magazine(new_magazine)

        # Check updated inventory
        self.assertEqual(len(self.system.books), 3)
        self.assertEqual(len(self.system.videos), 2)
        self.assertEqual(len(self.system.magazines), 2)

        # Register new users
        new_member = Member("David", "Lee", "david@test.com")
        new_librarian = Librarian("Eve", "Davis", "eve@library.com")

        self.system.register_member(new_member)
        self.system.register_librarian(new_librarian)

        # Check updated user counts
        self.assertEqual(len(self.system.members), 3)
        self.assertEqual(len(self.system.librarians), 2)

    def test_id_generation_workflow(self):
        """Test that IDs are generated correctly and uniquely"""
        # Create multiple items and users
        items = []
        for i in range(5):
            book = Book(f"Book {i}", 2023, "Test", f"Author {i}", f"978{i:010d}")
            video = Video(f"Video {i}", 2023, "Test", "DVD", 120)
            magazine = Magazine(f"Magazine {i}", 2023, "Test", f"Publisher {i}")
            member = Member(f"Member{i}", f"Last{i}", f"member{i}@test.com")
            librarian = Librarian(f"Librarian{i}", f"Last{i}", f"librarian{i}@test.com")

            items.extend([book, video, magazine, member, librarian])

        # Check that all IDs are unique
        ids = []
        for item in items:
            if hasattr(item, "isbn"):
                ids.append(item.isbn)
            elif hasattr(item, "video_id"):
                ids.append(item.video_id)
            elif hasattr(item, "magazine_id"):
                ids.append(item.magazine_id)
            elif hasattr(item, "member_id"):
                ids.append(item.member_id)
            elif hasattr(item, "librarian_id"):
                ids.append(item.librarian_id)

        # Check for uniqueness
        self.assertEqual(len(ids), len(set(ids)), "All IDs should be unique")

        # Check ID formats
        for item in items:
            if hasattr(item, "video_id"):
                self.assertTrue(item.video_id.startswith("VID"))
            elif hasattr(item, "magazine_id"):
                self.assertTrue(item.magazine_id.startswith("MAG"))
            elif hasattr(item, "member_id"):
                self.assertTrue(item.member_id.startswith("MBR"))
            elif hasattr(item, "librarian_id"):
                self.assertTrue(item.librarian_id.startswith("LBR"))


class TestSampleDataWorkflow(unittest.TestCase):
    """Test workflows using preloaded sample data"""

    def setUp(self):
        """Set up test fixtures with sample data"""
        self.system = LibrarySystem()
        self.system.preload_sample_books()
        self.system.preload_sample_magazines()
        self.system.preload_sample_videos()
        self.system.preload_sample_members()

        # Get first member for testing
        self.member = list(self.system.members.values())[0]

    def test_sample_data_availability(self):
        """Test that sample data is properly loaded"""
        self.assertGreater(len(self.system.books), 0, "Sample books should be loaded")
        self.assertGreater(
            len(self.system.magazines), 0, "Sample magazines should be loaded"
        )
        self.assertGreater(len(self.system.videos), 0, "Sample videos should be loaded")
        self.assertGreater(
            len(self.system.members), 0, "Sample members should be loaded"
        )

    def test_sample_data_workflow(self):
        """Test complete workflow with sample data"""
        # Get first available items
        first_book = list(self.system.books.values())[0]
        first_video = list(self.system.videos.values())[0]
        first_magazine = list(self.system.magazines.values())[0]

        # Borrow items
        result1 = self.system.checkout_book(first_book.isbn, self.member.member_id)
        self.assertIn("✅", result1)

        result2 = self.system.checkout_video(
            first_video.video_id, self.member.member_id
        )
        self.assertIn("✅", result2)

        result3 = self.system.checkout_magazine(
            first_magazine.magazine_id, self.member.member_id
        )
        self.assertIn("✅", result3)

        # Check borrowed items list
        borrowed_list = self.member.list_borrowed_items()
        self.assertIn("Borrowed Items", borrowed_list)
        self.assertIn(first_book.title, borrowed_list)
        self.assertIn(first_video.title, borrowed_list)
        self.assertIn(first_magazine.title, borrowed_list)

        # Return items
        result4 = self.system.return_book(first_book.isbn, self.member.member_id)
        self.assertIn("✅", result4)

        result5 = self.system.return_video(first_video.video_id, self.member.member_id)
        self.assertIn("✅", result5)

        result6 = self.system.return_magazine(
            first_magazine.magazine_id, self.member.member_id
        )
        self.assertIn("✅", result6)


def run_integration_tests():
    """Run all integration tests and display results"""
    print("🔗 Running Library Management System Integration Tests...")
    print("=" * 60)

    # Create test suite
    test_suite = unittest.TestSuite()

    # Add test classes
    test_classes = [TestLibraryWorkflows, TestSampleDataWorkflow]

    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Print summary
    print("=" * 60)
    print(f"Integration Tests run: {result.testsRun}")
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
        print("\n✅ All integration tests passed successfully!")

    return result.wasSuccessful()


if __name__ == "__main__":
    run_integration_tests()
