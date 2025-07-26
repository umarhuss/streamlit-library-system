import streamlit as st


def show():
    st.markdown("# 📚 Welcome to the Northeastern Library System")
    st.markdown("## A modern and simple system to manage your library experience")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔍 What you can do:")
        st.write(
            """
            - Browse books, videos, and magazines
            - Search for resources by title or genre
            - Register as a member to borrow items
            - Use the librarian portal to manage inventory
            """
        )

    with col2:
        st.markdown("### 🛠️ Built With:")
        st.write(
            """
            - **Python**
            - **Streamlit**
            - **Object-Oriented Programming**
            - Optional: **Docker**, **GitHub**, **UML Diagrams**
            """
        )

    st.markdown("---")
    st.markdown("Use the **sidebar** to navigate between features.")
