#!/usr/bin/env python3
"""
Main test runner for the Library Management System
Runs all unit tests and integration tests with comprehensive reporting
"""

import os
import sys
import time
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def run_all_tests():
    """Run all tests and provide comprehensive reporting"""
    print("🧪 LIBRARY MANAGEMENT SYSTEM - COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    print(f"Test Run Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    start_time = time.time()
    total_tests = 0
    total_failures = 0
    total_errors = 0

    # Import test modules
    try:
        from tests.test_integration import run_integration_tests
        from tests.test_library_system import run_tests as run_unit_tests
    except ImportError as e:
        print(f"❌ Error importing test modules: {e}")
        print("Make sure you're running this from the project root directory")
        return False

    # Run Unit Tests
    print("\n📋 UNIT TESTS")
    print("-" * 40)
    unit_success = run_unit_tests()

    # Run Integration Tests
    print("\n📋 INTEGRATION TESTS")
    print("-" * 40)
    integration_success = run_integration_tests()

    end_time = time.time()
    duration = end_time - start_time

    # Final Summary
    print("\n" + "=" * 70)
    print("📊 FINAL TEST SUMMARY")
    print("=" * 70)
    print(f"Test Duration: {duration:.2f} seconds")
    print(f"Unit Tests: {'✅ PASSED' if unit_success else '❌ FAILED'}")
    print(f"Integration Tests: {'✅ PASSED' if integration_success else '❌ FAILED'}")

    overall_success = unit_success and integration_success
    print(
        f"\nOverall Result: {'✅ ALL TESTS PASSED' if overall_success else '❌ SOME TESTS FAILED'}"
    )

    if overall_success:
        print(
            "\n🎉 Congratulations! Your Library Management System is working perfectly!"
        )
        print("   The system is ready for production use.")
    else:
        print(
            "\n⚠️  Some tests failed. Please review the errors above and fix any issues."
        )

    print("=" * 70)
    return overall_success


def run_quick_test():
    """Run a quick functionality test without detailed output"""
    print("🚀 Quick Functionality Test")
    print("-" * 30)

    try:
        from library_system import (
            Book,
            Librarian,
            LibrarySystem,
            Magazine,
            Member,
            Video,
        )

        # Create system and test basic functionality
        system = LibrarySystem()

        # Test adding items
        book = Book("Test Book", 2023, "Fiction", "Test Author", "1234567890")
        video = Video("Test Video", 2023, "Action", "DVD", 120)
        magazine = Magazine("Test Magazine", 2023, "Science", "Test Publisher")
        member = Member("John", "Doe", "john@test.com")

        system.add_book(book)
        system.add_video(video)
        system.add_magazine(magazine)
        system.register_member(member)

        # Test checkout and return
        result1 = system.checkout_book(book.isbn, member.member_id)
        result2 = system.return_book(book.isbn, member.member_id)

        if "✅" in result1 and "✅" in result2:
            print("✅ Basic functionality test passed!")
            return True
        else:
            print("❌ Basic functionality test failed!")
            return False

    except Exception as e:
        print(f"❌ Error during quick test: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        success = run_quick_test()
    else:
        success = run_all_tests()

    # Exit with appropriate code
    sys.exit(0 if success else 1)
