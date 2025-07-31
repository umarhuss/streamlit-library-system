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
    if not hasattr(member, "borrowed_items"):
        st.error("❌ Invalid user session. Please log in again.")
        return

    st.title("📖 My Borrowed Items")

    # Add refresh button
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 Refresh", key="refresh_member_portal"):
            st.rerun()

    if not member.borrowed_items:
        st.info("You have not borrowed any items.")
    else:
        st.write(f"You have borrowed **{len(member.borrowed_items)}** item(s):")
        for item in member.borrowed_items:
            with st.expander(
                f"📘 {item.title} ({item.__class__.__name__})", expanded=True
            ):
                st.write(item.get_description())
                if st.button(
                    f"Return '{item.title}'", key=f"return_{item.title}_{id(item)}"
                ):
                    result = member.return_item(item)
                    st.success(result)
                    st.rerun()
