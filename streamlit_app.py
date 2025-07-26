import streamlit as st
from streamlit_option_menu import option_menu
import components.homepage as homepage
import components.books as books
import components.member_page as member_page
import components.librarian_portal as librarian_portal
import components.magazines as magazines
import components.videos as videos


# Set page layout
st.set_page_config(page_title="Northeastern Library System", layout="wide")

# Set sidebar title
with st.sidebar:
    selected = option_menu(
        "Navigation",
        [
            "Home",
            "Browse Books",
            "Magazines",
            "Videos",
            "Member Login",
            "Librarian Portal",
        ],
        icons=["house", "book", "newspaper", "film", "person", "shield"],
        menu_icon="cast",
        default_index=0,
    )
    selected

if selected == "Home":
    homepage.show()
elif selected == "Browse Books":
    books.render()
elif selected == "Magazines":
    magazines.render()
elif selected == "Videos":
    videos.render()
elif selected == "Member Login":
    member_page.render()
elif selected == "Librarian Portal":
    librarian_portal.render()
