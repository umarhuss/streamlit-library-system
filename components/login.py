import streamlit as st
from library_system import Member, Librarian


def show():
    st.title("Login")

    role = st.radio("Login as", ["Member", "Librarian"])
    fname = st.text_input("First Name", key="fname_input")
    lname = st.text_input("Last Name", key="lname_input")
    email = st.text_input("Email Address", key="email_input")

    if st.button("Login"):
        # Strip whitespace
        fname = fname.strip()
        lname = lname.strip()
        email = email.strip()

        if not fname.strip() or not lname.strip() or not email.strip():
            st.error("❌ Please fill in all fields.")
            return

        system = st.session_state.library_system

        if role == "Member":
            member = next(
                (
                    m
                    for m in system.members.values()
                    if m.fname == fname
                    and m.lname == lname
                    and m.email_address == email
                ),
                None,
            )
            if not member:
                member = system.register_member(Member(fname, lname, email))
                st.success("✅ New member registered.")
            else:
                st.success("✅ Logged in as existing member.")

            st.session_state.logged_in_user = member
            st.session_state.user_role = "Member"
            st.session_state.redirect_target = "Member Portal"
            # st.rerun()

        else:  # Librarian
            librarian = next(
                (
                    l
                    for l in system.librarians.values()
                    if l.fname == fname
                    and l.lname == lname
                    and l.email_address == email
                ),
                None,
            )
            if not librarian:
                librarian = system.register_librarian(Librarian(fname, lname, email))
                st.success("✅ New librarian registered.")
            else:
                st.success("✅ Logged in as existing librarian.")

            st.session_state.logged_in_user = librarian
            st.session_state.user_role = "Librarian"
            st.session_state.redirect_target = "Librarian Portal"
            st.rerun()
