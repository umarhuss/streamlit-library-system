import streamlit as st
from library_system import Member


def show():
    if "logged_in_user" not in st.session_state:
        st.error("❌ Access denied. Login required.")
        return

    if st.session_state.user_role not in ["Member", "Librarian"]:
        st.error("❌ Access denied. Insufficient permissions.")
        return

    member = st.session_state.logged_in_user
    st.title("📖 My Borrowed Items")

    if not member.borrowed_items:
        st.info("You have not borrowed any items.")
    else:
        for item in member.borrowed_items:
            st.markdown(f"📘 **{item.title}** – {item.__class__.__name__}")
