import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import streamlit as st
import json

from backend.resume_parser import parse_resume
from backend.jd_parser import parse_jd
from backend.skills_comparator import compare_skills
from backend.cover_letter import generate_cover_letter
from backend.database import save_application
from backend.auth import get_user_by_token
from utils import SESSION_COOKIE_NAME
from frontend.components.footer import render_footer
from frontend.components.header import render_header

st.set_page_config(
    page_title="Resume & JD Analysis - AI Job Application Agent",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# --------------------------
# Header
# --------------------------
render_header()

# --------------------------
# Custom CSS for theme
# --------------------------
def load_custom_css():
 st.markdown("""
 <style>
    .stApp {
         background: linear-gradient(135deg, #e3f2fd, #ede7f6);
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    /* Animated background effect - same as main page */
        .email-header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: shimmer 6s ease-in-out infinite;
        }

    .email-header {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(102,126,234,0.3);

    }

    .email-header h1 {
            font-size: clamp(1.5rem, 4vw, 2.2rem);
            font-weight: 700;
            margin-bottom: 0.5rem;
            position: relative;
            z-index: 2;
            text-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }
        .email-header .icon {
            font-size: clamp(2rem, 6vw, 3.5rem);
            margin-bottom: 0rem;
            display: inline-block;
            animation: float 2s ease-in-out infinite;
        }



    .email-header p {
            font-size: clamp(0.9rem, 2vw, 1.1rem);
            font-weight: 300;
            opacity: 0.95;
            line-height: 1.4;
            max-width: 600px;
            margin: 0 auto;
        }

    .feature-badges {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-top: 1.5rem;
        flex-wrap: wrap;
        position: relative;
            z-index: 2;
    }

    .badge {
        background: rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.3);
        padding: 0.7rem 1.5rem;
        border-radius: 50px;
        font-size: 0.9rem;
        font-weight: 500;
        transition: all 0.3s ease;
        cursor: pointer;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        text-shadow: 0 1px 3px rgba(0,0,0,0.3);
        position: relative;
        overflow: hidden;
    }
    .badge::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }

    .badge:hover {
            background: rgba(255,255,255,0.3);
            border: 2px solid rgba(255,255,255,0.6);
            transform: translateY(-3px);
            box-shadow: 0 12px 25px rgba(0,0,0,0.25);
        }
        .badge:hover::before {
            left: 100%;
        }
        .card h3 {
    font-size: clamp(1rem, 2.5vw, 1.5rem);
    margin-bottom: 0.5rem;
    color: #1a237e;
 }

 .card p, .card div, .card span, .card li {
    font-size: clamp(0.9rem, 2vw, 1.1rem);
 }

 .card code {
    font-size: clamp(0.8rem, 1.8vw, 1rem);
    white-space: pre-wrap;
    word-break: break-word;
 }

    

    div[data-testid="stButton"] > button {
        background: #e3f2fd;
        border: 1px solid #90caf9;
        padding: 0.7rem 1.2rem;
        border-radius: 50px;
        font-size: 0.95rem;
        font-weight: 600;
        color: #1a237e;
        transition: all 0.3s ease;
        cursor: pointer;
        min-width: 120px;
        width: 100%;
    }

    div[data-testid="stButton"] > button:hover {
        background: #ede7f6;
        border: 1px solid #b39ddb;
        color: #311b92;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }

    @keyframes float {
        0%,100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }

    @media (max-width:768px){
        .email-header { padding:1.5rem; }
        .email-header h1 { font-size:1.8rem; }
        .email-header .icon { font-size:2.5rem; }
    }

     /* Mobile */
        @media (max-width: 480px) {
            .email-header {
                padding: 1.3rem;
                border-radius: 18px;
                margin-bottom: 1.5rem;
            }

            .email-header h1 {
                font-size: 1.8rem;
            }

            .email-header p {
                font-size: 1rem;
                line-height: 1.5;
                margin-bottom: 1rem;
            }
            
            .feature-badges {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 0.5rem;
                margin-top: 1rem;
                max-width: 100%;
            }
            
            .badge {
                padding: 0.8rem 0.6rem;
                font-size: 0.8rem;
                border-radius: 10px;
                text-align: center;
                min-height: 50px;
                display: flex;
                align-items: center;
                justify-content: center;
                line-height: 1.2;
            }
            .card {
        padding: 1rem;
        border-radius: 12px;
    }
    .card h3 {
        font-size: 1rem;
    }
    .card p, .card div, .card span, .card li {
        font-size: 1rem;
    }
    .card code {
        font-size: 0.95rem;
    }
 }
 </style>
 """, unsafe_allow_html=True)

# --------------------------
# Page Header
# --------------------------
def render_analysis_header():
 st.markdown("""
 <div class="email-header">
     <div class="icon">🤖</div>
     <h1>Resume & Job Description Analysis</h1>
     <p>Compare your resume against job descriptions to highlight matching skills</p>
     <div class="feature-badges">
         <div class="badge">🚀 Skills Match Analysis</div>
         <div class="badge">📝 JSON Detailed View</div>
         <div class="badge">⚡ Skills Match Scores</div>
         <div class="badge">✉️ Generated Cover Letter</div>
     </div>
 </div>
 """, unsafe_allow_html=True)

# --------------------------
# Authentication check
# --------------------------
def check_authentication():
 if "user" not in st.session_state or not st.session_state.user:
        st.markdown("""
        <div class="card" style="text-align: center;">
            <h3>🔒 Access Denied</h3>
            <p>Please log in to access the Resume & Job Description Analysis feature.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🛡️ Go to Login", use_container_width=True):
                st.switch_page("pages/0_👤_Auth.py")
        with col2:
            if st.button("🏠 Home", use_container_width=True):
                st.switch_page("1_🏠_Home.py")
        st.stop()
        
 return st.session_state.user["id"], st.session_state.user["name"]


# --------------------------
# Main Application
# --------------------------
def main():
    load_custom_css()
    render_analysis_header()
    
    user_id, user_name = check_authentication()

    st.markdown(f"""
   <div style="
    background: linear-gradient(135deg, #e3f2fd, #ede7f6);
    color: #1a237e;
    padding: 0.8rem 1.2rem;
    border-radius: 12px;
    font-size: 1rem;
    font-weight: 600;
    text-align: center;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    border: 1px solid #90caf9;
    ">
   👋 Welcome back, {user_name}! Ready to analyze your resume?
   </div>
    """, unsafe_allow_html=True)


# --------------------------
# Resume & JD Upload Card
# --------------------------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    resume_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf","docx"])
    jd_text = st.text_area("Paste Job Description")
    if st.button("🚀 Analyze", use_container_width=True):
      if resume_file and jd_text:
          try:
            with st.spinner("🔄 Processing your resume and job description..."):

              temp_path = f"temp_{resume_file.name}"
              with open(temp_path,"wb") as f: f.write(resume_file.getbuffer())
              resume_text = parse_resume(temp_path)
              jd_clean = parse_jd(jd_text)

              # Skills analysis
              skills_result = compare_skills(resume_text, jd_clean)
              skills_json = json.loads(skills_result)

            # --------------------------
            # Skills Match Card
            # --------------------------
              st.markdown('<div class="card">', unsafe_allow_html=True)
              if 'match_percentage' in skills_json:
                  st.markdown(f"<h3>🎯 Skills Match: {skills_json['match_percentage']}</h3>", unsafe_allow_html=True)
              if 'matching_skills' in skills_json:
                  st.markdown("✅ **Matching Skills:**")
                  for s in skills_json['matching_skills']: st.markdown(f"• {s}")
              if 'missing_skills' in skills_json:
                  st.markdown("⚠️ **Skills to Improve:**")
                  for s in skills_json['missing_skills']: st.markdown(f"• {s}")
              with st.expander("📋 Detailed JSON View"): st.json(skills_json)
              st.markdown('</div>', unsafe_allow_html=True)

            # --------------------------
            # Cover Letter Card
            # --------------------------
              st.markdown('<div class="card">', unsafe_allow_html=True)
              st.markdown("✉️ **Generated Cover Letter:**")
              cover_letter = generate_cover_letter(resume_text, jd_clean)
              st.code(cover_letter, language="text")
              st.markdown('</div>', unsafe_allow_html=True)
              # Download button for cover letter
              st.download_button(
                    label="📥 Download Cover Letter",
                    data=cover_letter,
                    file_name=f"cover_letter_{user_name.replace(' ', '_')}.txt",
                    mime="text/plain"
                )
              st.markdown('</div>', unsafe_allow_html=True)

            # Save analysis to DB
              try:
                  app_id = save_application(resume_text, jd_clean, skills_result, cover_letter, user_id)
                  st.success(f"✅ Analysis saved to your profile (ID: {app_id})")
              except:
                  st.info("⚠️ Analysis completed but not saved to DB")

              # Clean up temporary file
              if os.path.exists(temp_path):
                    os.remove(temp_path)
                    
          except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")
                if 'temp_path' in locals() and os.path.exists(temp_path):
                    os.remove(temp_path)
      else:
            st.warning("⚠️ Please upload a resume and paste a job description to proceed with the analysis.")
    
    if not resume_file or not jd_text.strip():
        st.markdown('</div>', unsafe_allow_html=True)

# --------------------------
# Footer
# --------------------------
render_footer()

if __name__ == "__main__":
    main()
