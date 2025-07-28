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
    # if not isinstance(member, Member):
    #     st.error("❌ Invalid user session. Please log in again.")
    #     return
    if not hasattr(member, "borrowed_items"):
        st.error("❌ Invalid user session. Please log in again.")
        st.write("DEBUG: logged_in_user =", member)
        st.write("DEBUG: type =", type(member))
        return

    st.title("📖 My Borrowed Items")

    if not member.borrowed_items:
        st.info("You have not borrowed any items.")
    else:
        for item in member.borrowed_items:
            st.markdown(f"📘 **{item.title}** – {item.__class__.__name__}")
