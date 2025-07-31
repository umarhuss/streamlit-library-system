import streamlit as st


def show():
    system = st.session_state.library_system

    st.subheader("Magazines")

    # Check if user is logged in
    if "logged_in_user" not in st.session_state:
        st.warning("Please log in to borrow magazines.")
        return

    if st.session_state.user_role != "Member":
        st.warning("Only members can borrow magazines.")
        return

    member = st.session_state.logged_in_user
    member_id = member.member_id

    # Check for magazines
    if not system.magazines:
        st.info("No magazines available.")
        return

    cols = st.columns(4)
    for i, mag in enumerate(system.magazines.values()):
        with cols[i % 4]:
            st.image(
                "https://img.icons8.com/?size=100&id=oo7qq9GfvBzP&format=png&color=000000",
                width=80,
            )
            st.markdown(f"### {mag.title}")
            st.caption(f"Published by {mag.publisher} ({mag.year})")
            st.write(f"Genre: {mag.genre}")
            st.write("✅ Available" if mag.is_available else "❌ Checked Out")
            if mag.is_available:
                if st.button("Borrow", key=f"borrow_mag_{mag.magazine_id}"):
                    result = system.checkout_magazine(mag.magazine_id, member_id)
                    st.success(result)
                    st.info("💡 Check your Member Portal to see your borrowed items!")
