import streamlit as st
from library_system import LibrarySystem


# Initialize session state with the LibrarySystem
if "library_system" not in st.session_state:
    st.session_state.library_system = LibrarySystem()
    # Preload books magazines and videos for demonstration
    st.session_state.library_system.preload_sample_books()
    st.session_state.library_system.preload_sample_magazines()
    st.session_state.library_system.preload_sample_videos()

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

# Redirect handling: do this only once before widgets render
if "redirect_target" in st.session_state and "nav_selection" not in st.session_state:
    st.session_state.nav_selection = st.session_state.redirect_target
    del st.session_state.redirect_target
    st.rerun()  # clean rerun with updated nav

# # Set sidebar title
# with st.sidebar:
#     if "logged_in_user" in st.session_state:
#         user = st.session_state.logged_in_user
#         role = st.session_state.user_role

#         if hasattr(user, "fname"):
#             st.markdown(f"👋 Logged in as **{user.fname} ({role})**")
#             if st.button("🚪 Logout"):
#                 del st.session_state.logged_in_user
#                 del st.session_state.user_role
#                 st.rerun()
#         else:
#             st.warning("⚠️ Invalid login state — resetting.")
#             del st.session_state.logged_in_user
#             del st.session_state.user_role
#             st.rerun()

#     # Build role-aware navigation menu
#     nav_items = ["Home", "Browse Books", "Magazines", "Videos", "Login"]
#     if "user_role" in st.session_state:
#         if st.session_state.user_role == "Member":
#             nav_items.append("Member Portal")
#         elif st.session_state.user_role == "Librarian":
#             nav_items.append("Member Portal")
#             nav_items.append("Librarian Portal")

#     icon_map = {
#         "Home": "house",
#         "Browse Books": "book",
#         "Magazines": "newspaper",
#         "Videos": "film",
#         "Login": "person",
#         "Member Portal": "person",
#         "Librarian Portal": "shield",
#     }

with st.sidebar:
    if "logged_in_user" in st.session_state:
        user = st.session_state.logged_in_user
        role = st.session_state.user_role

        if hasattr(user, "fname"):
            st.markdown(f"👋 Logged in as **{user.fname} ({role})**")
            if st.button("🚪 Logout"):
                del st.session_state.logged_in_user
                del st.session_state.user_role
                del st.session_state.nav_selection  # Reset nav
                st.rerun()
        else:
            st.warning("⚠️ Invalid login state — resetting.")
            del st.session_state.logged_in_user
            del st.session_state.user_role
            st.rerun()

    # Menu options should reflect login status
    nav_items = ["Home", "Browse Books", "Magazines", "Videos", "Login"]
    if "user_role" in st.session_state:
        if st.session_state.user_role == "Member":
            nav_items.append("Member Portal")
        elif st.session_state.user_role == "Librarian":
            nav_items.append("Member Portal")
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

    # Finally render the menu after all session state is stable
    selected = option_menu(
        "Navigation",
        nav_items,
        icons=[icon_map[item] for item in nav_items],
        menu_icon="cast",
        default_index=0,
        key="nav_selection",
    )

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
