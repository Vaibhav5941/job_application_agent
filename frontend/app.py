import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from backend.resume_parser import parse_resume

st.title("🤖 Job Application Agent")

resume_file = st.file_uploader("Upload Resume", type=["pdf","docx"])

if resume_file:
    with open(resume_file.name, "wb") as f:
        f.write(resume_file.getbuffer())
    text = parse_resume(resume_file.name)
    st.subheader("📄 Extracted Resume Text")
    st.write(text[:1000])  # preview
