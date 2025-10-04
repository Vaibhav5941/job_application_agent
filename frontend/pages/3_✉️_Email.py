import streamlit as st
import sys, os
from datetime import datetime
import re
import cohere
from backend.resume_parser import parse_resume
from frontend.components.footer import render_footer
from frontend.components.header import render_header


# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))

try:
    from backend.email_sender import send_email
except ImportError as e:
    st.error(f"Import error: {e}")
    st.error("Please ensure your email_sender module is properly configured")
    st.stop()

# Hydrate session from cookie token if needed
from backend.auth import get_user_by_token
from utils import SESSION_COOKIE_NAME
if "user" not in st.session_state or not st.session_state.user:
    try:
        token = st.session_state.get("session_token") or st.experimental_get_cookie(SESSION_COOKIE_NAME)
        if token:
            user = get_user_by_token(token)
            if user:
                st.session_state.user = user
                st.session_state.session_token = token
    except Exception:
        pass

# Initialize Cohere client
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
if COHERE_API_KEY:
    co = cohere.Client(COHERE_API_KEY)
else:
    co = None

# Page configuration
st.set_page_config(
    page_title="Professional Email Sender - AI Job Application Agent",
    page_icon="✉️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

render_header()
# Custom CSS
st.markdown("""
    <style>
    section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f8f9fa 0%, #e3f2fd 100%);
    padding: 12px;
    border-right: 2px solid #d0d7de;
    }

    /* Sidebar title/logo area */
    section[data-testid="stSidebar"] div[data-testid="stSidebarNav"] h2 {
    color: #0d47a1;
    font-weight: 700;
    margin-bottom: 12px;
    text-align: center;
    }

    /* Sidebar list items */
    section[data-testid="stSidebar"] div[data-testid="stSidebarNav"] li {
    background: #ffffff;
    margin: 6px 0;
    padding: 10px 14px;
    border-radius: 10px;
    font-weight: 700;
    font-size: 18px;
 
    gap: 10px;
    cursor: pointer;
    transition: all 0.3s ease-in-out;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }

    /* Hover effect */
    section[data-testid="stSidebar"] div[data-testid="stSidebarNav"] li:hover {
    background: #667eea;
    color: #ffffff;
    transform: translateX(5px);
    }

    /* Active item highlight */
    section[data-testid="stSidebar"] div[data-testid="stSidebarNav"] li:has(svg) {
    background: #bbdefb;
    color: #0d47a1;
   }
        /* =================================
           BASE STYLES
           ================================= */
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        .stApp {
            background: url("https://cfcdn.apowersoft.info/astro/picwish/_astro/main-title-icon-1.wmRL6OHI.png");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }

        /* =================================
           HEADER SECTION
           ================================= */
        
        .email-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
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
            font-size: clamp(1.5rem, 4vw, 2.2rem);
            font-weight: 700;
            margin-bottom: 0.5rem;
            position: relative;
            z-index: 2;
            text-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }
        
        .email-header .icon {
            font-size: clamp(2rem, 6vw, 3.5rem);
            margin-bottom: 1rem;
            display: inline-block;
            animation: float 2s ease-in-out infinite;
        }
        
        .email-header p {
            font-size: clamp(0.9rem, 2vw, 1.1rem);
            font-weight: 300;
            opacity: 0.95;
            position: relative;
            z-index: 2;
            line-height: 1.4;
            max-width: 600px;
            margin: 0 auto;
        }

        /* =================================
           FEATURE BADGES
           ================================= */
        
        .feature-badges {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: clamp(0.5rem, 2vw, 1rem);
            margin-top: clamp(1rem, 2.5vw, 1.5rem);
            padding: 0 1rem;
            position: relative;
            z-index: 2;
            max-width: 1000px;
            margin-left: auto;
            margin-right: auto;
        }

        .badge {
            background: rgba(255,255,255,0.2);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.3);
            padding: clamp(0.5rem, 1.5vw, 0.7rem) clamp(0.8rem, 2vw, 1.5rem);
            border-radius: 50px;
            font-size: clamp(0.75rem, 1.5vw, 0.9rem);
            font-weight: 500;
            transition: all 0.3s ease;
            cursor: pointer;
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
            text-shadow: 0 1px 3px rgba(0,0,0,0.3);
            position: relative;
            overflow: hidden;
            text-align: center;
            white-space: nowrap;
            text-overflow: ellipsis;
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

        /* =================================
           CARD COMPONENTS
           ================================= */
        
        .card {
            background: rgba(255,255,255,0.95);
            padding: clamp(1rem, 3vw, 2rem);
            border-radius: clamp(12px, 2vw, 15px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin: 0 auto clamp(1rem, 3vw, 2rem) auto;
            text-align: left;
            border: 1px solid rgba(255,255,255,0.2);
            transition: all 0.3s ease;
            max-width: min(95%, 1200px);
            width: 100%;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.15);
            border: 1px solid rgba(102, 126, 234, 0.3);
        }

        .success-message {
            background: linear-gradient(135deg, #e3f2fd, #bbdefb);
            color: #1a237e;
            padding: clamp(0.8rem, 2vw, 1rem) clamp(1rem, 2.5vw, 1.5rem);
            border-radius: clamp(10px, 2vw, 12px);
            font-size: clamp(0.9rem, 1.8vw, 1rem);
            font-weight: 500;
            border: 1px solid #90caf9;
            margin-bottom: clamp(1rem, 3vw, 2rem);
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }

        .ai-modal {
            border: 2px solid #667eea;
            border-radius: 15px;
            padding: clamp(1rem, 2.5vw, 1.5rem);
            background: rgba(255,255,255,0.95);
            margin: 1rem 0;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
            transition: all 0.3s ease;
        }
        .ai-modal:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
        }
        .ai-modal h4 {
            color: #667eea;
            margin-bottom: 1rem;
            font-size: clamp(1.1rem, 2.5vw, 1.3rem);
            font-weight: 700;
        }
        .ai-modal p {
            color: #666;
            margin-bottom: 1.5rem;
            font-size: clamp(0.9rem, 1.8vw, 1rem);
        }

        /* =================================
           FORM INPUTS
           ================================= */
        
        .stTextInput > div > input, 
        .stTextArea > div > textarea, 
        {
            border-radius: 10px;
            border: 1px solid #90caf9;
            background: #fafafa;
            transition: all 0.3s ease;
            font-size: max(16px, 0.95rem);
            padding: 0.7rem 1rem;
        }
        
        .stTextInput > div > input:focus, 
        .stTextArea > div > textarea:focus,
        .stSelectbox > div > div:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
            outline: none;
        }

        .stFileUploader > div {
            border: 2px dashed #90caf9;
            border-radius: 10px;
            padding: clamp(0.8rem, 2vw, 1.2rem);
            background: rgba(227, 242, 253, 0.3);
            transition: all 0.3s ease;
        }
        
        .stFileUploader > div:hover {
            border-color: #667eea;
            background: rgba(227, 242, 253, 0.5);
        }

        /* Character counter */
        .char-counter {
            font-size: clamp(0.75rem, 1.5vw, 0.8rem);
            color: #6c757d;
            text-align: right;
            margin-top: 0.25rem;
            font-style: italic;
        }

        /* =================================
           BUTTON SYSTEM - RESPONSIVE GRID
           ================================= */
        
        /* Standard buttons */
        div[data-testid="stButton"] {
            display: flex;
            justify-content: center;
        }
        
        div[data-testid="stButton"] > button {
            width: 100%;
            background: #e3f2fd;
            border: 1px solid #90caf9;
            padding: clamp(0.6rem, 1.5vw, 0.7rem) clamp(1rem, 2vw, 1.2rem);
            border-radius: 50px;
            font-size: clamp(0.85rem, 1.8vw, 0.95rem);
            font-weight: 600;
            color: #1a237e;
            transition: all 0.3s ease;
            cursor: pointer;
            
            min-height: 44px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        
        div[data-testid="stButton"] > button:hover {
            background: #ede7f6;
            border: 1px solid #b39ddb;
            color: #311b92;
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }

        /* Form submit buttons */
        div[data-testid="stForm"] div[data-testid="stButton"] > button {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            font-weight: 700;
            text-shadow: 0 1px 3px rgba(0,0,0,0.3);
        }
        
        div[data-testid="stForm"] div[data-testid="stButton"] > button:hover {
            background: linear-gradient(135deg, #5a6fd8, #6a4190);
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
        }

        /* Navigation button grid */
        .nav-buttons-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(min(100%, 200px), 2fr));
            gap: clamp(0.5rem, 2vw, 1rem);
            margin: clamp(1rem, 2vw, 1.5rem) 0;
        }

        /* =================================
           EXPANDERS
           ================================= */
        
        .streamlit-expanderHeader {
            background: rgba(255,255,255,0.9);
            border-radius: 10px;
            border: 1px solid #e0e0e0;
            padding: clamp(0.6rem, 1.5vw, 0.8rem);
            transition: all 0.3s ease;
            font-size: clamp(0.9rem, 1.8vw, 1rem);
            min-height: 44px;
        }
        
        .streamlit-expanderHeader:hover {
            border-color: #667eea;
            background: rgba(227, 242, 253, 0.5);
        }

        /* =================================
           TYPOGRAPHY
           ================================= */
        
        h2, h3, h4 {
            color: #1a237e;
            font-weight: 700;
            margin-bottom: clamp(0.5rem, 2vw, 1rem);
            line-height: 1.3;
        }
        
        h2 {
            font-size: clamp(1.3rem, 3.5vw, 1.8rem);
        }
        
        h3 {
            font-size: clamp(1.1rem, 3vw, 1.6rem);
        }
        
        h4 {
            font-size: clamp(1rem, 2.5vw, 1.3rem);
        }

        /* =================================
           ALERTS & MESSAGES
           ================================= */
        
        .stSuccess, .stError, .stWarning, .stInfo {
            border-radius: 10px;
            border-left: 4px solid;
            padding: clamp(0.8rem, 2vw, 1rem);
            margin: clamp(0.5rem, 2vw, 1rem) 0;
            font-size: clamp(0.9rem, 1.8vw, 1rem);
        }

        /* =================================
           ANIMATIONS
           ================================= */
        
        @keyframes shimmer {
            0%, 100% { transform: translateX(-100%) translateY(-100%) rotate(0deg); }
            50% { transform: translateX(-50%) translateY(-50%) rotate(180deg); }
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }

        /* =================================
           RESPONSIVE BREAKPOINTS
           ================================= */

        /* Tablet Landscape (768px - 1023px) */
        @media (max-width: 1023px) and (min-width: 768px) {
            .feature-badges {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .nav-buttons-container {
                grid-template-columns: repeat(2, 1fr);
            }
        }

        /* Tablet Portrait (600px - 767px) */
        @media (max-width: 767px) and (min-width: 600px) {
            .email-header {
                padding: 1.2rem;
            }
            
            .feature-badges {
                grid-template-columns: repeat(2, 1fr);
                gap: 0.8rem;
            }
            
            .badge {
                white-space: normal;
                line-height: 1.3;
                min-height: 44px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .nav-buttons-container {
                grid-template-columns: repeat(2, 1fr);
            }
        }

        /* Mobile Landscape (480px - 599px) */
        @media (max-width: 599px) and (min-width: 480px) {
            .email-header {
                padding: 1rem;
                border-radius: 15px;
            }
            
            .feature-badges {
                grid-template-columns: repeat(2, 1fr);
                gap: 0.6rem;
            }
            
            .badge {
                padding: 0.6rem 0.8rem;
                white-space: normal;
                min-height: 50px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .card {
                padding: 1.2rem;
            }
            
            .nav-buttons-container {
                grid-template-columns: repeat(2, 1fr);
                gap: 0.8rem;
            }
        }

        /* Mobile Portrait (320px - 479px) */
        @media (max-width: 479px) {
            .email-header {
                padding: 2rem 1rem;
                border-radius: 18px;
                margin-bottom: 1.5rem;
            }

            .email-header h1 {
                font-size: 1.8rem;
                margin-bottom: 1rem;
            }
            
            
            .email-header .icon {
                font-size: 2rem;
            }
            
            .email-header p {
                font-size: 1rem;
                line-height: 1.5;
                margin-bottom: 1rem;
            }
            
            .feature-badges {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 1rem;
                margin-top: 2rem;
                padding: 0;
                max-width: 100%;
            }
            
            .badge {
                padding: 0.7rem 1rem;
                white-space: normal;
                min-height: 44px;
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
            }
            
            .card {
                padding: 1rem;
                border-radius: 12px;
            }
            
            .nav-buttons-container {
                grid-template-columns: 1fr;
                gap: 0.6rem;
            }
            
            /* Stack columns on mobile */
            div[data-testid="column"] {
                width: 100% !important;
                flex: 1 1 100% !important;
                min-width: 100% !important;
            }
            
            div[data-testid="stButton"] > button {
                font-size: 0.9rem;
                padding: 0.7rem 1rem;
            }
            
        }

 

        /* =================================
           ACCESSIBILITY IMPROVEMENTS
           ================================= */
        
        @media (pointer: coarse) {
            div[data-testid="stButton"] > button,
            .streamlit-expanderHeader,
            .badge {
                min-height: 44px;
                min-width: 44px;
            }
        }

        @media (prefers-reduced-motion: reduce) {
            *,
            *::before,
            *::after {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("""
<div class="email-header">
        <div class="icon">✉️</div>
        <h1>Professional Email Sender</h1>
        <p>Send personalized application emails directly through Gmail with confidence and professionalism</p>
        <div class="feature-badges">
            <div class="badge">🚀 Gmail Integration</div>
            <div class="badge">📝 Custom Templates</div>
            <div class="badge">⚡ Bulk Sending</div>
            <div class="badge">📊 Track Results</div>
        </div>
    </div>
    
""", unsafe_allow_html=True)

# Authentication check
if "user" not in st.session_state or not st.session_state.user:
    st.markdown("""
    <div class="card" style="text-align: center;">
            <h3>🔒 Access Denied</h3>
            <p>Please log in to access the Resume & Job Description Analysis feature.</p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🛡️ Go to Login", type="primary", use_container_width=True):
            st.switch_page("pages/0_👤_Auth.py")
    with col2:
        if st.button("🏠 Home", use_container_width=True):
            st.switch_page("app.py")
    st.stop()

# User info display
st.markdown(f"""
<div class="success-message">
    <strong>📧 Sending from:</strong> {st.session_state.user['email']}<br>
    <strong>👤 Sender name:</strong> {st.session_state.user['name']}
</div>
""", unsafe_allow_html=True)

# ============================================================================
# EMAIL TEMPLATES
# ============================================================================
st.subheader("📋 Email Templates")

# Predefined templates
email_templates = {
    "Job Application": {
        "subject": "Application for [Position Title] - [Your Name]",
        "body": """Dear Hiring Manager,

I am writing to express my strong interest in the [Position Title] position at [Company Name]. With my background in [Your Field/Experience], I am excited about the opportunity to contribute to your team.

Key highlights of my qualifications:
• [Relevant Experience/Skill 1]
• [Relevant Experience/Skill 2]
• [Relevant Experience/Skill 3]

I have attached my resume for your review and would welcome the opportunity to discuss how my skills and experience align with your needs. I am particularly drawn to [Company Name] because of [Specific reason - company mission, values, recent news, etc.].

Thank you for your time and consideration. I look forward to hearing from you.

Best regards,
[Your Name]
[Your Phone Number]
[Your Email]"""
    },
    
    "Follow-up Email": {
        "subject": "Following up on [Position Title] application - [Your Name]",
        "body": """Dear [Hiring Manager Name/Team],

I hope this email finds you well. I wanted to follow up on my application for the [Position Title] position that I submitted on [Date]. 

I remain very interested in this opportunity and believe my experience in [Relevant Area] would be valuable to your team. Since submitting my application, I have [any relevant updates - new certification, project completion, etc.].

I would be happy to provide any additional information you might need or to schedule a time to discuss my qualifications further.

Thank you for your consideration, and I look forward to hearing from you.

Best regards,
[Your Name]
[Your Phone Number]
[Your Email]"""
    },
    
    "Thank You After Interview": {
        "subject": "Thank you for the interview - [Position Title]",
        "body": """Dear [Interviewer Name],

Thank you for taking the time to interview me for the [Position Title] position at [Company Name]. I enjoyed our conversation about [specific topic discussed] and learning more about [specific aspect of the role/company].

Our discussion reinforced my enthusiasm for this opportunity, particularly [mention something specific from the interview]. I believe my experience with [relevant experience/skill mentioned in interview] would allow me to make meaningful contributions to your team.

If you need any additional information from me, please don't hesitate to reach out. I look forward to the next steps in the process.

Best regards,
[Your Name]
[Your Phone Number]
[Your Email]"""
    },
    
    "Networking Email": {
        "subject": "Introduction and Career Advice - [Your Name]",
        "body": """Dear [Contact Name],

I hope this message finds you well. I'm [Your Name], a [your current role/background] with a strong interest in [relevant field/industry]. I came across your profile through [how you found them - LinkedIn, company website, referral, etc.] and was impressed by your experience at [Company Name].

I'm currently exploring opportunities in [specific area/role] and would greatly value any insights you might have about the industry or your experience at [Company Name]. If you have 15-20 minutes for a brief informational interview, I would be grateful for the opportunity to learn from your expertise.

I understand you're busy, so please don't feel obligated to respond. However, if you're available for a quick chat over coffee or phone, I would appreciate it greatly.

Thank you for your time and consideration.

Best regards,
[Your Name]
[Your Phone Number]
[Your Email]"""
    },
    
    "Custom Email": {
        "subject": "",
        "body": ""
    }
}

    # Template selection
selected_template = st.selectbox(
        "📝 Choose a template to get started:",
        list(email_templates.keys()),
        help="Select a pre-written template or choose 'Custom Email' to start from scratch"
    )
# Create two columns for template selection and AI generation
col1, col2 = st.columns([1, 1])

with col1:
    # Display template preview
    if selected_template != "Custom Email":
     with st.expander(f"👁️ Preview: {selected_template} Template"):
        template = email_templates[selected_template]
        st.markdown(f"**Subject:** {template['subject']}")
        st.markdown("**Body:**")
        st.text(template['body'])

# AI Generation Section
with col2:
    # Initialize session state for modal
    if "show_ai_modal" not in st.session_state:
        st.session_state.show_ai_modal = False
    
    # AI Button - Always visible
    if st.button("🤖 AI Email Generator", type="primary", use_container_width=True):
        st.session_state.show_ai_modal = True
    
    # Modal/Popup for AI Generation
    if st.session_state.show_ai_modal:
            st.markdown("""
            <div class="ai-modal">
                <h4>🤖 AI Email Generator</h4>
                <p>Generate personalized emails using AI based on your resume and job description</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Job Description Input
            job_description = st.text_area(
                "📋 Paste Job Description",
                height=100,
                placeholder="Paste the job description here to generate a personalized email...",
                help="Paste the full job description and AI will generate a customized application email",
                key="modal_job_desc"
            )
            
            # Resume uploader
            resume_file = st.file_uploader(
                "📂 Upload Resume (PDF/DOCX)", 
                type=["pdf", "docx"],
                key="modal_resume"
            )
            
            # Action buttons with better spacing
            st.markdown("<br>", unsafe_allow_html=True)
            
            button_col1, button_col2, button_col3 = st.columns([2, 1, 2])
            
            with button_col1:
                if st.button("🚀 Generate Email", type="primary", use_container_width=True, 
                            help="Generate AI-powered email"):
                    if job_description.strip() and resume_file:
                        with st.spinner("🤖 AI is crafting your email..."):
                            try:
                                # Save uploaded resume temporarily
                                with open(resume_file.name, "wb") as f:
                                    f.write(resume_file.getbuffer())
                                
                                # Parse resume text
                                resume_text = parse_resume(resume_file.name)
                                
                                # ✅ Agentic AI Prompt: combine resume + JD
                                message = f"""
                                You are an expert career assistant. Write a concise, professional job application email.
                                
                                📄 Candidate Resume: {resume_text[:2000]}  # limit length if resume is huge
                                📌 Job Description: {job_description}
                                
                                The email should:
                                - Have a compelling subject line
                                - Be professionally written and concise
                                - Highlight relevant skills that match the job requirements
                                - Show enthusiasm for the role
                                - Include placeholders for personalization like [Your Name], [Company Name], etc.
                                - Be around 150-200 words
                                - End with a professional closing
                                
                                Format the response as:
                                SUBJECT: [subject line]
                                BODY: [email body]
                                """
                                
                                response = co.chat(
                                    model="command-a-03-2025",
                                    message=message,
                                    max_tokens=500,
                                    temperature=0.6,
                                    stop_sequences=["--END--"]
                                )
                                
                                ai_email = response.text.strip()
                                
                                # Store generated email in session state
                                st.session_state["email_body"] = ai_email
                                
                                # Close modal and show success
                                st.session_state.show_ai_modal = False
                                st.success("✅ AI Email Generated Successfully!")
                                st.rerun()
                                
                            except Exception as e:
                                st.error(f"❌ AI generation failed: {str(e)}")
                    else:
                        st.warning("⚠️ Please upload a resume and paste the job description")
            
            with button_col3:
                if st.button("❌ Cancel", use_container_width=True, 
                            help="Close AI generator"):
                    st.session_state.show_ai_modal = False
                    st.rerun()
    
    # Show generated email preview if available
    if "email_body" in st.session_state and st.session_state["email_body"]:
        st.markdown("### 📧 Generated Email Preview:")
        with st.expander("View Generated Email", expanded=False):
            st.write(st.session_state["email_body"])


# ============================================================================
# EMAIL COMPOSITION FORM
# ============================================================================
# Email Composition Form
st.markdown("---")
st.subheader("✉ Compose Your Email")

# Add button to use AI generated email if available
if "email_body" in st.session_state and st.session_state["email_body"]:
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("🤖 Use AI Email", type="secondary"):
            # Parse AI email content
            ai_content = st.session_state["email_body"]
            if "SUBJECT:" in ai_content and "BODY:" in ai_content:
                parts = ai_content.split("BODY:", 1)
                subject_part = parts[0].replace("SUBJECT:", "").strip()
                body_part = parts[1].strip()
                st.session_state["selected_subject"] = subject_part
                st.session_state["selected_body"] = body_part
            st.rerun()
    with col2:
        if st.button("📝 Use Template", type="secondary"):
            if "selected_subject" in st.session_state:
                del st.session_state["selected_subject"]
            if "selected_body" in st.session_state:
                del st.session_state["selected_body"]
            st.rerun()

with st.form("email_form"):
    # Email fields
    col1, col2 = st.columns(2)
    
    with col1:
        recipient = st.text_input(
            "► Recipient Email *",
            placeholder="hr@company.com, hiring.manager@example.com",
            help="Enter the recipient's email address"
        )
        
        # Validate email format
        if recipient:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            if not re.match(email_pattern, recipient):
                st.error("⚠️ Please enter a valid email address")
    
    with col2:
        cc_recipients = st.text_input(
            "► CC (Optional)",
            placeholder="additional@email.com",
            help="Carbon copy recipients (separate multiple emails with commas)"
        )
    
    # Resume attachment
    st.markdown("**Resume Attachment**")
    resume_attachment = st.file_uploader(
        "Attach Resume (PDF/DOCX) - Optional",
        type=["pdf", "docx"],
        help="Your resume will be attached to the email"
    )
    
    # Subject line - use selected content if available
    subject_value = st.session_state.get("selected_subject", email_templates[selected_template]["subject"])
    
    subject = st.text_input(
        "► Email Subject *",
        value=subject_value,
        placeholder="Clear, professional subject line",
        help="Make it clear and specific - mention the position and your name"
    )
    
    # Character counter for subject
    if subject:
        st.markdown(f'<div class="char-counter">Subject length: {len(subject)} characters (recommended: 30-50)</div>', unsafe_allow_html=True)
    
    # Email body - use selected content if available
    body_value = st.session_state.get("selected_body", email_templates[selected_template]["body"])
    
    body = st.text_area(
        "► Email Body *",
        value=body_value,
        height=400,
        placeholder="Write your professional email message here...",
        help="Personalize the template with specific details about the company and position"
    )
    
    # Character/word counter for body
    if body:
        word_count = len(body.split())
        char_count = len(body)
        st.markdown(f'<div class="char-counter">Body: {word_count} words, {char_count} characters</div>', unsafe_allow_html=True)
    
    # Pre-send suggestions (non-mandatory)
    st.markdown("---")
    st.markdown("### Pre-send Suggestions")
    st.markdown("*These are helpful reminders, not requirements:*")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("• Replace [placeholders] with actual details")
        st.markdown("• Proofread for spelling and grammar")
        st.markdown("• Mention specific company details")
    
    with col2:
        st.markdown("• Prepare attachments (resume, portfolio)")
        st.markdown("• Include contact information")
        st.markdown("• Maintain professional tone")
    
    # Send button
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        send_email_button = st.form_submit_button(
            "📤 Send Email",
            type="primary",
            use_container_width=True
        )
    
    with col2:
        preview_button = st.form_submit_button(
            "👁️ Preview",
            use_container_width=True
        )

# Email sending logic (outside the form)
if send_email_button:
    if not recipient or not subject or not body:
        st.error("⚠️ Please fill in all required fields (Recipient, Subject, Body)")
    elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', recipient):
        st.error("⚠️ Please enter a valid recipient email address")
    elif "[" in body or "]" in body or "[" in subject or "]" in subject:
        # Check for placeholders and stop if found
        st.warning("⚠️ Warning: Your email contains placeholders [like this]. Please replace them before sending.")
        st.info("💡 Tip: Replace placeholders like [Your Name], [Company Name], [Position Title] with actual information.")    
    else:
        # Show warnings for placeholders
        with st.spinner("Sending email..."):
            try:
                # Prepare attachments
                attachments = []
                if resume_attachment:
                    attachments.append({
                        'filename': resume_attachment.name,
                        'content': resume_attachment.getbuffer()
                    })
                
                # Send email with attachments
                status = send_email(
                    recipient, 
                    subject, 
                    body, 
                    st.session_state.user["email"],
                    cc_recipients if cc_recipients else None,
                    attachments if attachments else None
                )
                
                if "sent successfully" in status.lower() or "success" in status.lower():
                    st.success(f"📤 Email sent successfully!")
                    st.balloons()
                    
                    # Email stats update
                    if 'emails_sent' not in st.session_state:
                        st.session_state.emails_sent = 0
                    st.session_state.emails_sent += 1
                    
                    # Show next steps
                    st.info("""
                    **Next Steps:**
                    • Email sent successfully
                    • Track this application in your dashboard
                    • Set a follow-up reminder for 1 week
                    """)
                    
                else:
                    st.error(f"Failed to send email: {status}")
                    
            except Exception as e:
                st.error(f"Unexpected error: {str(e)}")

# Preview logic (outside the form)
if preview_button and recipient and subject and body:
    st.markdown("---")
    st.subheader("Email Preview")
    
    preview_content = f"""
    **From:** {st.session_state.user['name']} <{st.session_state.user['email']}>
    **To:** {recipient}
    """
    
    if cc_recipients:
        preview_content += f"**CC:** {cc_recipients}\n"
    
    if resume_attachment:
        preview_content += f"**Attachment:** {resume_attachment.name}\n"
    
    preview_content += f"""**Subject:** {subject}
    
    ---
    
    {body}
    """
    
    st.markdown(preview_content)

# Initialize session state variables
if 'send_requested' not in st.session_state:
    st.session_state.send_requested = False

# ============================================================================
# EMAIL BEST PRACTICES
# ============================================================================
st.markdown("---")

with st.expander("💡 Email Best Practices & Tips"):
    st.markdown("""
    ### ✉️ **Subject Line Best Practices:**
    - **Be specific**: Include position title and your name
    - **Keep it concise**: 30-50 characters is ideal
    - **Avoid spam words**: "URGENT", excessive caps, multiple exclamation marks
    - **Examples**: 
        - ✅ "Application for Software Engineer - John Smith"
        - ✅ "Following up on Marketing Manager interview"
        - ❌ "URGENT!!! Please read this!!!"
    
    ### 📝 **Email Body Tips:**
    - **Start with a clear purpose**: State why you're writing in the first sentence
    - **Keep it concise**: 150-200 words is usually sufficient
    - **Use bullet points**: Make key qualifications easy to scan
    - **Personalize**: Mention something specific about the company
    - **Include a clear call-to-action**: What do you want them to do next?
    
    ### 🎯 **Personalization Strategies:**
    - **Research the company**: Mention recent news, values, or projects
    - **Address by name**: Use "Dear [Name]" instead of "To Whom It May Concern"
    - **Connect your experience**: Explain how your skills solve their specific needs
    - **Show enthusiasm**: Explain why you're excited about THIS particular role
    
    ### 🤖 **AI Generation Tips:**
    - **Provide detailed job descriptions**: More details = better personalized emails
    - **Always review and edit**: AI provides a great starting point, but add your personal touch
    - **Replace placeholders**: Make sure to customize company names, your details, etc.
    - **Adjust tone as needed**: Fine-tune the AI output to match your communication style
    
    ### ⏰ **Timing Best Practices:**
    - **Best days**: Tuesday through Thursday
    - **Best times**: 9-11 AM or 2-4 PM in recipient's timezone
    - **Avoid**: Monday mornings, Friday afternoons, weekends, holidays
    - **Follow-up timing**: Wait 1 week before following up
    
    ### 📎 **Professional Etiquette:**
    - **Use professional email address**: firstname.lastname@gmail.com
    - **Include signature**: Name, phone number, LinkedIn profile
    - **Proofread carefully**: Use spell check and read aloud
    - **Mobile-friendly**: Keep paragraphs short for mobile reading
    
    ### 🚫 **Common Mistakes to Avoid:**
    - Generic mass emails without personalization
    - Too long (over 300 words) or too short (under 50 words)
    - Focusing only on what you want, not what you offer
    - Forgetting to attach resume or mentioned documents
    - Using informal language or emojis (except in very casual industries)
    """)

# ============================================================================
# QUICK ACTIONS & NAVIGATION
# ============================================================================
st.markdown("---")
st.subheader("⚡ Quick Actions")
# Using HTML/CSS grid for better responsive control
st.markdown('<div class="nav-buttons-container">', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📊 Skills Analysis", use_container_width=True):
        st.switch_page("pages/2_📊_Analysis.py")

with col2:    
    if st.button("📧 Email", use_container_width=True):
        st.switch_page("pages/3_✉️_Email.py")

with col3:
    if st.button("📈 Dashboard", use_container_width=True):
        st.switch_page("pages/5_📊_Dashboard.py")

with col4:
    if st.button("📂 History", use_container_width=True):
        st.switch_page("pages/4_📂_History.py")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>💡 <strong>Pro Tip:</strong> Always customize your emails for each application. Generic emails have lower response rates!</p>
    <p>🤖 <strong>Agentic AI Tip:</strong> Upload your resume along with job descriptions for highly personalized emails that match your actual experience to job requirements!</p>
    <p>📧 Need help with Gmail setup? Check the Authentication page for detailed instructions.</p>
</div>
""", unsafe_allow_html=True)
render_footer()