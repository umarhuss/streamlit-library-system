import streamlit as st


def show():
    system = st.session_state.library_system

    st.subheader("Magazines")

    # Check for registered members
    if not system.members:
        st.warning("Please register a member first to borrow magazines.")
        return
    member_id = st.selectbox(
        "Select a member", list(system.members.keys()), key="magazine_member"
    )

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
