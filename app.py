import streamlit as st
import os
import tempfile
from src.extractors import (
    extract_from_pdf,
    extract_from_docx,
    extract_from_ppt,
    extract_from_txt,
    extract_from_image,
    extract_from_audio_video
)
from src.summarizer import generate_summary

# Page Configuration
st.set_page_config(page_title="Summarizerly", page_icon="📝", layout="centered")

def main():
    st.title("📝 Summarizerly")
    st.subheader("Summarize Documents, Images, Audio & Video Offline")
    
    st.markdown("---")
    
    # file uploader
    uploaded_file = st.file_uploader(
        "Upload a file", 
        type=["pdf", "docx", "pptx", "txt", "jpg", "png", "mp3", "wav", "mp4", "mkv", "avi"]
    )
    
    if uploaded_file is not None:
        # Save uploaded file to a temporary file
        # We need a real path for some libraries (like ffmpeg/tesseract/pypdf sometimes prefers paths)
        file_ext = uploaded_file.name.split('.')[-1].lower()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_ext}") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name
            
        st.info(f"File uploaded: {uploaded_file.name}")
        
        # Extraction Step
        text_content = ""
        st.text("Processing file... Please wait.")
        
        try:
            if file_ext == "pdf":
                text_content = extract_from_pdf(tmp_path)
            elif file_ext == "docx":
                text_content = extract_from_docx(tmp_path)
            elif file_ext == "pptx":
                text_content = extract_from_ppt(tmp_path)
            elif file_ext == "txt":
                text_content = extract_from_txt(tmp_path)
            elif file_ext in ["jpg", "png", "jpeg"]:
                text_content = extract_from_image(tmp_path)
            elif file_ext in ["mp3", "wav", "mp4", "mkv", "avi"]:
                st.warning("Audio/Video processing might take some time on CPU.")
                text_content = extract_from_audio_video(tmp_path)
            else:
                st.error("Unsupported file format.")
            
            # Clean up temp file
            os.remove(tmp_path)

            if not text_content:
                st.error("Could not extract any text from the file. It might be empty or scanned without OCR text.")
                return

            # Show extracted text (optional, expandable)
            with st.expander("View Extracted Text"):
                st.write(text_content[:2000] + ("..." if len(text_content) > 2000 else ""))

            # Summarization Step
            if st.button("Summarize"):
                with st.spinner("Generating Summary using T5-small..."):
                    summary = generate_summary(text_content)
                    st.success("Summary Generated!")
                    st.markdown("### Final Summary")
                    st.write(summary)
                    
        except Exception as e:
            st.error(f"An error occurred: {e}")

    st.markdown("---")
    st.markdown("*Built with ❤️ using Python, Streamlit, and Open Source Models*")

if __name__ == "__main__":
    main()
