import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import streamlit as st
import json
from backend.resume_parser import parse_resume
from backend.jd_parser import parse_jd
from backend.skills_comparator import compare_skills
from backend.cover_letter import generate_cover_letter
from backend.database import save_application

st.title("📊 Resume & Job Description Analysis")

resume_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
jd_text = st.text_area("Paste Job Description")

if st.button("Analyze"):
    if resume_file and jd_text:
        try:
            # Save uploaded file
            with open(resume_file.name, "wb") as f:
                f.write(resume_file.getbuffer())
            
            # Parse resume and JD
            resume_text = parse_resume(resume_file.name)
            jd_clean = parse_jd(jd_text)
            
            st.subheader("📊 Skills Match Analysis")
            skills_result = compare_skills(resume_text, jd_clean)
            
            # Try to display as JSON, fallback to text
            try:
                skills_json = json.loads(skills_result)
                st.json(skills_json)
            except json.JSONDecodeError:
                st.text("Skills Analysis:")
                st.text(skills_result)
            
            st.subheader("✉️ Generated Cover Letter")
            cover_letter = generate_cover_letter(resume_text, jd_clean)
            st.write(cover_letter)
            
            # Save to DB with error handling
            try:
                save_application(resume_text, jd_clean, skills_result, cover_letter)
                st.success("✅ Analysis saved to database")
            except Exception as db_error:
                st.error(f"❌ Database error: {str(db_error)}")
                st.info("Analysis completed but not saved to database")
                
        except Exception as e:
            st.error(f"❌ Analysis failed: {str(e)}")
            
    else:
        st.warning("⚠️ Please upload a resume and paste job description")