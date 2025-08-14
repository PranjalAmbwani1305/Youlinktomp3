# Save this code in a file, for example: app.py

import streamlit as st
from pytube import YouTube
import io

def sanitize_filename(title):
    """Removes characters that are invalid for filenames."""
    return "".join([c for c in title if c.isalpha() or c.isdigit() or c.isspace()]).rstrip()

# --- Streamlit App Interface ---

st.set_page_config(page_title="YouTube to MP3", page_icon="🎧")

st.title("YouTube to MP3 Downloader 🎧")
st.markdown("Enter the URL of the YouTube video you want to download as an MP3 file. The highest available audio quality will be downloaded.")

# Input field for the YouTube URL
url = st.text_input("Enter YouTube URL:", placeholder="e.g., https://www.youtube.com/watch?v=dQw4w9WgXcQ")

if st.button("Convert Video"):
    if url:
        try:
            # Show a spinner while processing
            with st.spinner('Fetching video and converting to audio... Please wait.'):
                yt = YouTube(url)

                # Filter for audio-only streams and select the best one
                audio_stream = yt.streams.filter(only_audio=True).order_by('abr', ascending=False).first()

                if audio_stream:
                    # Download audio stream into an in-memory buffer
                    buffer = io.BytesIO()
                    audio_stream.stream_to_buffer(buffer)
                    buffer.seek(0)  # Reset buffer position to the beginning

                    # Sanitize the video title to create a valid filename
                    safe_title = sanitize_filename(yt.title)
                    file_name = f"{safe_title}.mp3"

                    st.success(f"✅ **{yt.title}** is ready for download!")

                    # Provide the download button
                    st.download_button(
                        label="📥 Download MP3",
                        data=buffer,
                        file_name=file_name,
                        mime="audio/mpeg"
                    )
                else:
                    st.error("❌ No audio-only stream found for this video.")

        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.info("Please check the URL and try again. The video might be private, age-restricted, or unavailable.")
    else:
        st.warning("⚠️ Please enter a YouTube URL to proceed.")

st.markdown("---")
st.markdown("Created with ❤️ using **Streamlit** & **Pytube**.")
