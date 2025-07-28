import streamlit as st
from library_system import LibrarySystem


# Initialize session state with the LibrarySystem
if "library_system" not in st.session_state:
    st.session_state.library_system = LibrarySystem()
    # Preload books magazines users and videos for demonstration
    st.session_state.library_system.preload_sample_books()
    st.session_state.library_system.preload_sample_magazines()
    st.session_state.library_system.preload_sample_videos()
    st.session_state.library_system.preload_sample_members()

from streamlit_option_menu import option_menu
import components.homepage as homepage
import components.books as books
import components.member_page as member_page
import components.librarian_portal as librarian_portal
import components.magazines as magazines
import components.videos as videos
import components.login as login


# Set page layout
st.set_page_config(page_title="Northeastern Library System", layout="wide")
user = st.session_state.get("logged_in_user", None)

# Handle redirect logic
if "redirect_target" in st.session_state and "nav_selection" not in st.session_state:
    st.session_state.nav_selection = st.session_state.redirect_target
    del st.session_state.redirect_target
    st.rerun()

# Sidebar
with st.sidebar:

    if "logged_in_user" in st.session_state and hasattr(
        st.session_state.logged_in_user, "fname"
    ):
        user = st.session_state.logged_in_user
        role = st.session_state.user_role
        st.markdown(f"👋 Logged in as **{user.fname} ({role})**")
        if st.button("🚪 Logout"):
            for key in ["logged_in_user", "user_role", "nav_selection"]:
                st.session_state.pop(key, None)
            st.session_state["nav_selection"] = "Home"
            st.rerun()
    else:
        st.markdown("🔒 Not logged in")

    # Navigation Menu
    nav_items = ["Home", "Browse Books", "Magazines", "Videos"]
    if "logged_in_user" not in st.session_state:
        nav_items.append("Login")
    else:
        if st.session_state.user_role == "Member":
            nav_items.append("Member Portal")
        elif st.session_state.user_role == "Librarian":
            nav_items.append("Librarian Portal")

    icon_map = {
        "Home": "house",
        "Browse Books": "book",
        "Magazines": "newspaper",
        "Videos": "film",
        "Login": "person",
        "Member Portal": "person",
        "Librarian Portal": "shield",
    }

    selected = option_menu(
        "Navigation",
        nav_items,
        icons=[icon_map[item] for item in nav_items],
        menu_icon="cast",
        default_index=0,
        key="nav_selection",
    )

# Page Routing
if selected == "Home":
    homepage.show()
elif selected == "Browse Books":
    books.show()
elif selected == "Magazines":
    magazines.show()
elif selected == "Videos":
    videos.show()
elif selected == "Login":
    login.show()
elif selected == "Member Portal":
    member_page.show()
elif selected == "Librarian Portal":
    librarian_portal.show()
