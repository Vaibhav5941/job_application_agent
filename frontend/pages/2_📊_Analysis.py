import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import streamlit as st
import json
from backend.resume_parser import parse_resume
from backend.jd_parser import parse_jd
from backend.skills_comparator import compare_skills
from backend.cover_letter import generate_cover_letter
from backend.database import save_application


# Custom CSS
st.markdown("""
<style>
            * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        
        .email-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.2rem 2rem;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
            position: relative;
            overflow: hidden;
        }
        
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
        
        .email-header h1 {
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 0;
            position: relative;
            z-index: 2;
            text-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }
        
        .email-header .icon {
            font-size: 3.5rem;
            margin-bottom: 0rem;
            display: inline-block;
            animation: float 2s ease-in-out infinite;
        }
        
        .email-header p {
            font-size: 1 rem;
            font-weight: 300;
            opacity: 0.95;
            position: relative;
            z-index: 2;
            line-height: 1.2;
        }
        
        .feature-badges {
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-top: 2rem;
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
        }
        
        .badge:hover {
            background: rgba(255,255,255,0.3);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        

        
        .demo-text {
            text-align: center;
            color: #666;
            font-size: 1.1rem;
            line-height: 1.6;
        }
        
        @keyframes shimmer {
            0%, 100% { transform: translateX(-100%) translateY(-100%) rotate(0deg); }
            50% { transform: translateX(-50%) translateY(-50%) rotate(180deg); }
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
 @media (max-width: 1024px) {
            .email-header {
                padding: 2.5rem 2rem;
            }
            
            .email-header h1 {
                font-size: 2.4rem;
            }
            
            .email-header .icon {
                font-size: 3rem;
            }
        }
        
        /* Mobile landscape */
        @media (max-width: 768px) {
           
            
            .email-header {
                padding: 2rem 1.5rem;
                margin-bottom: 1.5rem;
                border-radius: 15px;
            }
            
            .email-header h1 {
                font-size: 2rem;
                margin-bottom: 0.8rem;
            }
            
            .email-header .icon {
                font-size: 2.5rem;
                margin-bottom: 0.8rem;
            }
            
            .email-header p {
                font-size: 1.1rem;
                line-height: 1.5;
            }
            
            .feature-badges {
                margin-top: 1.5rem;
                gap: 0.8rem;
            }
            
            .badge {
                padding: 0.6rem 1.2rem;
                font-size: 0.85rem;
            }
            
            .content-area {
                padding: 1.5rem;
                border-radius: 12px;
            }
        }
        
        /* Mobile portrait */
        @media (max-width: 480px) {

            
            .email-header {
                padding: 1rem 1rem;
                margin-bottom: 1rem;
                border-radius: 12px;
            }
            
            .email-header h1 {
                font-size: 1.2rem;
                margin-bottom: 0rem;
            }
            
            .email-header .icon {
                font-size: 2.2rem;
                margin-bottom: 0rem;
            }
            
            .email-header p {
                font-size: 0.8rem;
                line-height: 1;
            }
            
            .feature-badges {
                flex-direction: row;
                align-items: center;
                gap: 0.5rem;
                margin-top: 1.2rem;
            }
            
            .badge {
                width: fit-content;
                padding: 0.5rem 1rem;
                font-size: 0.8rem;
            }
            
            .content-area {
                padding: 1.2rem;
                border-radius: 10px;
            }
            
            .demo-text h3 {
                font-size: 1.1rem;
            }
            
            .demo-text p {
                font-size: 0.95rem;
            }
        }


</style>
""", unsafe_allow_html=True)
# Header
st.markdown("""
<div class="email-header">
        <div class="icon">✉️</div>
        <h1>Resume & Job Description Analysis</h1>
        <p>Compare your resume against job descriptions to highlight matching skills</p>
        <div class="feature-badges">
            <div class="badge">🚀 Skills Match Analysis</div>
            <div class="badge">📝 JSON detailed view</div>
            <div class="badge">⚡ Skills match scores</div>
            <div class="badge">📊 Generated Cover Letter</div>
        </div>
    </div>
    
""", unsafe_allow_html=True)

# Check authentication
if "user" not in st.session_state or not st.session_state.user:
    st.error("🔒 Access Denied: Please log in to send emails")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔑 Go to Login", type="primary", use_container_width=True):
            st.switch_page("pages/0_👤_Auth.py")
    with col2:
        if st.button("🏠 Home", use_container_width=True):
            st.switch_page("app.py")
    st.stop()

user_id = st.session_state.user["id"]
user_name = st.session_state.user["name"]

st.success(f"Welcome, {user_name}! 👋")

resume_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
jd_text = st.text_area("Paste Job Description")

if st.button("Analyze",type="primary"):
    if resume_file and jd_text:
        try:
            # Save uploaded file
                temp_file_path = f"temp_{resume_file.name}"
                with open(temp_file_path, "wb") as f:
                    f.write(resume_file.getbuffer())
                        
                # Parse resume and JD
                resume_text = parse_resume(temp_file_path)
                jd_clean = parse_jd(jd_text)
                        
                st.subheader("📊 Skills Match Analysis")
                skills_result = compare_skills(resume_text, jd_clean)
                        
                # Try to display as JSON, fallback to text
                try:
                    skills_json = json.loads(skills_result)
                    
                    # Display match percentage prominently
                    if 'match_percentage' in skills_json:
                        match_pct = skills_json['match_percentage']
                        st.metric("🎯 Skills Match", match_pct)
                    
                    # Show matching skills
                    if 'matching_skills' in skills_json and skills_json['matching_skills']:
                        st.success("✅ **Matching Skills:**")
                        for skill in skills_json['matching_skills']:
                            st.write(f"• {skill}")
                    
                    # Show missing skills
                    if 'missing_skills' in skills_json and skills_json['missing_skills']:
                        st.warning("⚠️ **Skills to Improve:**")
                        for skill in skills_json['missing_skills']:
                            st.write(f"• {skill}")
                    
                    # Show full JSON for detailed view
                    with st.expander("📋 Detailed Analysis"):
                        st.json(skills_json)
                        
                except json.JSONDecodeError:
                    st.text("Skills Analysis:")
                    st.text(skills_result)
                        
                st.subheader("✉️ Generated Cover Letter")
                with st.spinner("✍️ Generating personalized cover letter..."):
                    cover_letter = generate_cover_letter(resume_text, jd_clean)
                    st.write(cover_letter)
                
                # Copy button for cover letter
                st.code(cover_letter, language="text")
                        
                # Save to DB with user_id for isolation
                try:
                    app_id = save_application(resume_text, jd_clean, skills_result, cover_letter, user_id)
                    st.success(f"✅ Analysis saved to your profile (ID: {app_id})")
                except Exception as db_error:
                    st.error(f"❌ Database error: {str(db_error)}")
                    st.info("Analysis completed but not saved to database")
                
                # Clean up temp file
                try:
                    os.remove(temp_file_path)
                except:
                    pass
                
        except Exception as e:
            st.error(f"❌ Analysis failed: {str(e)}")
            
    else:
        st.warning("⚠️ Please upload a resume and paste job description")