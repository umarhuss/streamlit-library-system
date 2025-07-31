import streamlit as st


def show():
    system = st.session_state.library_system
    st.subheader("Videos")

    # Check if user is logged in
    if "logged_in_user" not in st.session_state:
        st.warning("Please log in to borrow videos.")
        return

    if st.session_state.user_role != "Member":
        st.warning("Only members can borrow videos.")
        return

    member = st.session_state.logged_in_user
    member_id = member.member_id

    # Check if there are any videos
    if not system.videos:
        st.info("No videos available.")
        return

    # Create 4 columns for layout consistency
    cols = st.columns(4)
    for i, video in enumerate(system.videos.values()):
        with cols[i % 4]:
            st.image(
                "https://img.icons8.com/?size=100&id=44827&format=png&color=000000",
                width=80,
            )
            st.markdown(f"### {video.title}")
            st.caption(f"{video.year} • {video.genre}")
            st.write(f"💾 Format: {video.video_format}")
            st.write(f"⏱️ Duration: {video.duration} mins")
            st.write("✅ Available" if video.is_available else "❌ Checked Out")
            if video.is_available:
                if st.button("Borrow", key=f"borrow_video_{video.video_id}"):
                    result = system.checkout_video(video.video_id, member_id)
                    st.success(result)
                    st.info("💡 Check your Member Portal to see your borrowed items!")
