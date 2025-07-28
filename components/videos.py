import streamlit as st


def show():
    system = st.session_state.library_system
    st.subheader("Videos")

    # Check for registered members
    if not system.members:
        st.warning("Please register a member first to borrow videos.")
        return

    member_id = st.selectbox(
        "Select a member", list(system.members.keys()), key="video_member"
    )

    # Check if there are any videos
    if not system.videos:
        st.info("No videos available.")
        return

    # Create 4 columns for layout consistency
    cols = st.columns(4)
    for i, video in enumerate(system.videos.values()):
        with cols[i % 4]:
            st.image(
                "https://img.icons8.com/?size=100&id=44827&format=png&color=000000",  # replace with a better thumbnail if desired
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
