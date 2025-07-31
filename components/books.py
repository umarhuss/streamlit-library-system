import streamlit as st


def show():
    # Initialise the library session state
    system = st.session_state.library_system

    st.subheader("Browse Books")

    # Check if user is logged in
    if "logged_in_user" not in st.session_state:
        st.warning("Please log in to borrow books.")
        return

    if st.session_state.user_role != "Member":
        st.warning("Only members can borrow books.")
        return

    member = st.session_state.logged_in_user
    member_id = member.member_id

    # Check if there are any books in the library yet
    if not system.books:
        st.write("📚 No books available in the library yet.")
        return
    # Display books in rows of 4
    books = list(system.books.values())
    for row_start in range(0, len(books), 4):
        cols = st.columns(4)
        for i in range(4):
            if row_start + i < len(books):
                book = books[row_start + i]
                with cols[i]:
                    st.image(
                        "https://img.icons8.com/?size=100&id=32Akt39C5Dah&format=png&color=000000",
                        width=80,
                    )
                    st.markdown(f"### {book.title}")
                    st.caption(f"Published in {book.year}")
                    st.write(f"Author: {book.author}")
                    st.write(f"Genre: {book.genre}")
                    st.write(f"ISBN: {book.isbn}")
                    st.write("✅ Available" if book.is_available else "❌ Checked Out")
                    if book.is_available:
                        if st.button("Borrow", key=f"borrow_{book.isbn}"):
                            result = system.checkout_book(book.isbn, member_id)
                            st.success(result)
                            st.info(
                                "💡 Check your Member Portal to see your borrowed items!"
                            )
                    else:
                        st.write("❌ Not Available")
