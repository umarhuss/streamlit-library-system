import streamlit as st


def show():
    # Check if the user is logged in and has librarian role
    if (
        "logged_in_user" not in st.session_state
        or st.session_state.user_role != "Librarian"
    ):
        st.error("❌ Access denied. Librarian login required.")
        return

    st.title("📚 Librarian Portal")
    system = st.session_state.library_system

    # Check if members exist
    if not system.members:
        st.warning("No registered members. Please register a member first.")
        return

    st.subheader("🔎 Select a Member")

    # Dropdown to choose a member
    selected_member_id = st.selectbox(
        "Choose a member to view their borrowed items",
        options=list(system.members.keys()),
        format_func=lambda mid: f"{system.members[mid].fname} {system.members[mid].lname} ({mid})",
    )

    selected_member = system.members[selected_member_id]

    st.subheader("📦 Items Borrowed by Member")

    if selected_member.borrowed_items:
        for item in selected_member.borrowed_items:
            with st.expander(
                f"{item.title} ({item.__class__.__name__})", expanded=True
            ):
                st.caption(item.get_description())
                if st.button(f"Return '{item.title}'", key=f"return_{item.title}"):
                    result = selected_member.return_item(item)
                    st.success(result)
    else:
        st.info("This member has no borrowed items.")
