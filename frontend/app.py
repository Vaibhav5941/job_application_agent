import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from backend.resume_parser import parse_resume
from backend.auth import get_user_by_token, create_sessions_table
from utils import SESSION_COOKIE_NAME
from frontend.components.footer import render_footer
from frontend.components.header import render_header


create_sessions_table()

def load_custom_css():
   
    """Load custom CSS for responsive design"""
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f8f9fa 0%, #e3f2fd 100%);
    padding: 15px;
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
    padding: 10px 35px;
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
   
         
        /* Reset and base styles */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        /* App background */
        .stApp {
            background-image: url("https://cfcdn.apowersoft.info/astro/picwish/_astro/main-title-icon-1.wmRL6OHI.png");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }

        /* Main header styling */
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


        /* Animated background effect */
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

        /* Header content */
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

        /* Streamlit navigation buttons container */
        div[data-testid="stHorizontalBlock"] {
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-top: 2rem;
            flex-wrap: wrap;
            padding: 0 1rem;
        }

        /* Individual button containers */
        div[data-testid="stButton"] {
            display: flex;
            justify-content: center;
            flex: 1;
            min-width: 0;
        }

        /* Navigation buttons styling (inside header) */
        .email-header + div div[data-testid="stButton"] > button {
            background: rgba(255,255,255,0.2);
            backdrop-filter: blur(15px);
            border: 2px solid rgba(255,255,255,0.4);
            padding: 1rem 1.5rem;
            border-radius: 15px;
            font-size: 1rem;
            font-weight: 600;
            color: white;
            transition: all 0.3s ease;
            cursor: pointer;
            width: 100%;
            min-width: 140px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
            text-shadow: 0 1px 3px rgba(0,0,0,0.3);
            position: relative;
            overflow: hidden;
        }

        .email-header + div div[data-testid="stButton"] > button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }

        .email-header + div div[data-testid="stButton"] > button:hover {
            background: rgba(255,255,255,0.3);
            border: 2px solid rgba(255,255,255,0.6);
            transform: translateY(-3px);
            box-shadow: 0 12px 25px rgba(0,0,0,0.25);
        }

        .email-header + div div[data-testid="stButton"] > button:hover::before {
            left: 100%;
        }

        .email-header + div div[data-testid="stButton"] > button:active {
            transform: translateY(-1px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }

        /* Regular buttons styling (outside header) */
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
            box-shadow: 0 3px 6px rgba(0,0,0,0.12);
        }

        div[data-testid="stButton"] > button:hover {
            background: #ede7f6;
            border: 1px solid #b39ddb;
            color: #311b92;
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }

        /* Content area styling */
        .content-section {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 0rem;
            border-radius: 15px;
            margin: 2rem 0;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }

        /* File uploader styling */
        div[data-testid="stFileUploader"] {
            background: rgba(255, 255, 255, 0.8);
            padding: 1rem;
            border-radius: 10px;
            border: 2px dashed #667eea;
            margin: 1rem 0;
        }

        /* Animations */
        @keyframes shimmer {
            0%, 100% { 
                transform: translateX(-100%) translateY(-100%) rotate(0deg); 
            }
            50% { 
                transform: translateX(-50%) translateY(-50%) rotate(180deg); 
            }
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }

        /* Responsive breakpoints */
        
        /* Tablet - Better spacing and sizing */
        @media (max-width: 768px) {
            .email-header {
                padding: 2rem 1.5rem;
                border-radius: 20px;
                margin-bottom: 2rem;
            }

            div[data-testid="stHorizontalBlock"] {
                gap: 1rem;
                margin-top: 2.5rem;
                padding: 0 0.5rem;
            }

            .email-header + div div[data-testid="stButton"] > button,
            div[data-testid="stButton"] > button {
                padding: 0.9rem 1.2rem;
                min-width: 130px;
                font-size: 0.95rem;
                border-radius: 12px;
            }

            .content-section {
                padding: 1.8rem;
                margin: 2rem 0;
            }
        }

        /* Mobile - Optimized Grid Layout */
        @media (max-width: 480px) {
            .email-header {
                padding: 2rem 1rem;
                border-radius: 18px;
                margin-bottom: 1.5rem;
            }

            .email-header h1 {
                font-size: 1.8rem;
                margin-bottom: 1rem;
            }

            .email-header p {
                font-size: 1rem;
                line-height: 1.5;
                margin-bottom: 1rem;
            }

            /* Perfect 2x2 Grid for mobile */
            div[data-testid="stHorizontalBlock"] {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 1rem;
                margin-top: 2rem;
                padding: 0;
                max-width: 100%;
            }

            div[data-testid="stButton"] {
                width: 100%;
                display: flex;
                justify-content: stretch;
            }

            .email-header + div div[data-testid="stButton"] > button {
                padding: 1.2rem 0.8rem;
                font-size: 0.9rem;
                font-weight: 700;
                min-width: unset;
                width: 100%;
                border-radius: 12px;
                min-height: 60px;
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                line-height: 1.2;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }

            .content-section {
                padding: 0rem;
                margin: 1.5rem 0;
                border-radius: 12px;
            }
        }

        /* Small Mobile - Refined grid */
        @media (max-width: 380px) {
            .email-header {
                padding: 1.5rem 0.8rem;
                margin-bottom: 1rem;
            }

            .email-header h1 {
                font-size: 1.5rem;
            }

            .email-header p {
                font-size: 0.9rem;
            }

            div[data-testid="stHorizontalBlock"] {
                gap: 0.8rem;
                margin-top: 1.5rem;
            }

            .email-header + div div[data-testid="stButton"] > button {
                padding: 1rem 0.5rem;
                font-size: 0.85rem;
                min-height: 55px;
                border-radius: 10px;
            }
        }

        /* Very small screens - Stack vertically if needed */
        @media (max-width: 320px) {
            div[data-testid="stHorizontalBlock"] {
                grid-template-columns: 1fr;
                gap: 0.8rem;
                max-width: 250px;
                margin-left: auto;
                margin-right: auto;
            }

            .email-header + div div[data-testid="stButton"] > button {
                padding: 1rem;
                font-size: 0.9rem;
                min-height: 50px;
            }
        }
    </style>
    """, unsafe_allow_html=True)

def render_main_header():
    """Render the main application header"""
    st.markdown("""
    <div class="email-header">
        <div class="icon">🤖</div>
        <h1>AI-powered Job Application Agent</h1>
        <p>Simplify your job application process with tools designed to make you stand out — 
            from resume analysis to cover letter generation and application tracking.</p>
    </div>
    """, unsafe_allow_html=True)

def render_navigation_buttons():
    """Render navigation buttons"""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("Skills Analysis", use_container_width=True):
            st.switch_page("pages/2_📊_Analysis.py")

    with col2:    
        if st.button("Email", use_container_width=True):
            st.switch_page("pages/3_✉️_Email.py")

    with col3:
        if st.button("Dashboard", use_container_width=True):
            st.switch_page("pages/5_📊_Dashboard.py")

    with col4:
        if st.button("History", use_container_width=True):
            st.switch_page("pages/4_📂_History.py")

def handle_authentication():
    """Handle user authentication and session management"""
    # Hydrate session from cookie token if needed
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
    
    # Check authentication
    if "user" not in st.session_state or not st.session_state.user:
        st.error("🔒 Access Denied: Please log in to access the application")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🛡️ Go to Login", type="primary", use_container_width=True):
                st.switch_page("pages/0_👤_Auth.py")
        with col2:
            if st.button("🏠 Home", use_container_width=True):
                st.switch_page("pages/1_🏠_Home.py")
        st.stop()

    return st.session_state.user

def render_resume_section():
    """Render resume upload and processing section"""
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    
    st.subheader("📄 Resume Analysis")
    st.write("Upload your resume to get started with AI-powered analysis and job application assistance.")
    
    resume_file = st.file_uploader(
        "Choose your resume file", 
        type=["pdf", "docx"],
        help="Supported formats: PDF, DOCX"
    )

    if resume_file:
        try:
            # Save uploaded file temporarily
            with open(resume_file.name, "wb") as f:
                f.write(resume_file.getbuffer())
            
            # Parse resume
            with st.spinner("Analyzing your resume..."):
                text = parse_resume(resume_file.name)
            
            # Display results
            st.markdown("""
<div style="
    background: linear-gradient(135deg, #e3f2fd, #ede7f6);
    color: #1a237e;
    padding: 0.8rem 1.2rem;
    border-radius: 10px;
    font-size: 1rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 8px;
    border: 1px solid #90caf9;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
">
✅ Resume analyzed successfully!
</div>
""", unsafe_allow_html=True)

            
            with st.expander("📖 View Extracted Text Preview", expanded=False):
             st.markdown(f"""
              <div style="
        background: linear-gradient(135deg, #e3f2fd, #ede7f6);
        color:#1a237e;
        padding:1rem;
        border-radius:10px;
        border:1px solid #ddd;
        font-size:0.95rem;
        line-height:1.6;
        max-height:300px;
        overflow-y:auto;
        white-space:pre-wrap;
        font-family: 'Segoe UI', Tahoma, sans-serif;
    ">
           {text[:1000] + "..." if len(text) > 1000 else text}
         </div>
        """, unsafe_allow_html=True)

            
           
            
            # Clean up temporary file
            try:
                os.remove(resume_file.name)
            except:
                pass
                
        except Exception as e:
            st.error(f"❌ Error processing resume: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    # Set page config
    st.set_page_config(
        page_title="AI Job Application Agent",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Load components and styles
    render_header()
    
    load_custom_css()
    
    # Render main content
    render_main_header()
    render_navigation_buttons()
    
    
    # Handle authentication
    user = handle_authentication()
    
    
    
    # Welcome message
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
👋 Welcome back, {user['name']}
</div>
""", unsafe_allow_html=True)
    
    # Main content sections
    render_resume_section()
    render_footer()
    

if __name__ == "__main__":
    main()