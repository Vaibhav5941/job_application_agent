import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import base64
import streamlit as st
from frontend.components.footer import render_footer
from frontend.components.header import render_header
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return f"data:image/png;base64,{base64.b64encode(data).decode()}"

resume_img = get_base64_image("frontend/assets/resume.png")
cover_img = get_base64_image("frontend/assets/coverletter.png")
email_img = get_base64_image("frontend/assets/email.png")
dashboard_img = get_base64_image("frontend/assets/dashboard.png")
history_img = get_base64_image("frontend/assets/history.png")
auth_img = get_base64_image("frontend/assets/auth.png")

# --------------------------
# Load custom CSS
# --------------------------
def load_custom_css():
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
            box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
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
        /* Feature badges styling */
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
            backdrop-filter: blur(15px);
            border: 2px solid rgba(255,255,255,0.4);
            padding: 0.7rem 1.5rem;
            border-radius: 15px;
            font-size: 0.9rem;
            font-weight: 500;
            color: white;
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


        /* Card Styles - enhanced to match main page */
        .card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
            text-align: center;
            transition: all 0.3s ease;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            height: 100%;
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.15);
            border: 1px solid rgba(102, 126, 234, 0.3);
        }
        
        .card img {
            width: 100%;
            max-width: 250px;
            height: auto;
            border-radius: 10px;
            margin-bottom: 15px;
            align-self: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .card h4 {
            margin: 1rem 0;
            font-size: 1.3rem;
            color: #667eea;
            font-weight: 600;
        }
        
        .card ul {
            text-align: left;
            padding-left: 0;
            list-style: none;
            margin: 1rem 0;
        }
        
        .card li {
            font-size: 0.95rem;
            color: #555;
            line-height: 1.6;
            margin-bottom: 0.5rem;
            padding-left: 1.5rem;
            position: relative;
        }
        
        .card li::before {
            content: '✓';
            position: absolute;
            left: 0;
            color: #667eea;
            font-weight: bold;
            font-size: 1rem;
        }

        /* Button styling - same as main page */
        div[data-testid="stButton"] > button {
            background: #e3f2fd;
            border: 1px solid #90caf9;
            padding: 0.7rem 1.2rem;
            border-radius: 50px;
            font-size: 0.1rem;
            font-weight: 600;
            color: #1a237e;
            transition: all 0.3s ease;
            cursor: pointer;
            min-width: 120px;
            box-shadow: 0 3px 6px rgba(0,0,0,0.12);
            width: 40%;
            display:flex;
            
            
        }

        div[data-testid="stButton"] > button:hover {
            background: #ede7f6;
            border: 1px solid #b39ddb;
            color: #311b92;
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }

        /* Animations - same as main page */
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

        /* Responsive Design - matching main page approach */
        
        /* Tablet */
        @media (max-width: 768px) {
            .email-header {
                padding: 2rem 1.5rem;
                border-radius: 20px;
                margin-bottom: 2rem;
            }
            
            .feature-badges {
                gap: 0.8rem;
                margin-top: 1.5rem;
            }
            
            .badge {
                padding: 0.6rem 1.2rem;
                font-size: 0.85rem;
                border-radius: 12px;
            }
            
            .card {
                padding: 1.5rem;
                margin-bottom: 1.5rem;
            }
            
            .card h4 {
                font-size: 1.2rem;
            }
            
            .card li {
                font-size: 0.9rem;
            }
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
                padding: 1.2rem;
                margin-bottom: 1.2rem;
                border-radius: 12px;
            }
            
            .card img {
                max-width: 200px;
            }
            
            .card h4 {
                font-size: 1.1rem;
                margin: 0.8rem 0;
            }
            
            .card li {
                font-size: 0.85rem;
                margin-bottom: 0.4rem;
            }
            
            /* Make columns stack on mobile */
            .stColumns {
                flex-direction: column;
            }
        }

    </style>
    """, unsafe_allow_html=True)

# --------------------------
# Header
# --------------------------
def render_main_header():
    st.markdown("""
    <div class="email-header">
        <div class="icon">🤖</div>
        <h1>AI-powered Job Application Agent</h1>
        <p>Simplify your job application process with tools designed to make you stand out —
           from resume analysis to cover letter generation, application tracking and authentication.</p>
       <div class="feature-badges">
        <div class="badge">🚀 Skills Match Analysis</div>
        <div class="badge">📝 JSON detailed view</div>
        <div class="badge">📊 Application Tracking</div>
        <div class="badge">🛡️ User Authentication</div>
    </div>

    </div>
    """, unsafe_allow_html=True)

# --------------------------
# Cards Section
# --------------------------
def render_cards_section():
    # Features grid
 col1, col2 = st.columns(2)

 with col1:
    st.markdown(f"""
        <div class="card">
            <img src="{resume_img}" alt="Resume Analysis">
            <h4>Upload & Analyze Resume</h4>
           <ul>
            <li>Upload and scan resumes instantly.</li>
            <li>AI highlights key skills and gaps.</li>
            <li>Provides job-specific match percentage.</li>
            <li>Suggestions for improvement.</li>
            <li>Optimize resumes before applying.</li>
        </ul>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="card">
            <img src="{cover_img}" alt="Cover Letter">
            <h4>Generate Tailored Cover Letters</h4>
           <ul>
            <li>Create personalized letters in seconds.</li>
            <li>Adapts tone and format automatically.</li>
            <li>Tailors content to job descriptions.</li>
            <li>Ensures professionalism and impact.</li>
            <li>Save time with AI-driven writing.</li>
        </ul>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="card">
            <img src="{history_img}" alt="History">
            <h4>User Application History</h4>
              <ul>
            <li>Chronological log of all submissions.</li>
            <li>Store resumes & letters safely.</li>
            <li>Revisit past documents easily.</li>
            <li>Track patterns & progress history.</li>
            <li>Eliminate duplicate applications.</li>
        </ul>
        </div>
    """, unsafe_allow_html=True)

 with col2:
    st.markdown(f"""
        <div class="card">
            <img src="{email_img}" alt="Email Recruiters">
            <h4>Email Recruiters Directly</h4>
            <ul>
            <li>AI-generated professional email drafts.</li>
            <li>Formal tone for HR & recruiters.</li>
            <li>Custom templates for job outreach.</li>
            <li>Save and reuse email formats.</li>
            <li>Boost response chances with clarity.</li>
        </ul>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="card">
            <img src="{dashboard_img}" alt="Dashboard">
            <h4>Track Your Applications</h4>
           <ul>
            <li>Central hub for all applications.</li>
            <li>Track applied, shortlisted, interview.</li>
            <li>Visual progress charts & analytics.</li>
            <li>Stay organized with reminders.</li>
            <li>Monitor success across roles.</li>
        </ul>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="card">
            <img src="{auth_img}" alt="Authentication">
            <h4>User Authentication</h4>
             <ul>
            <li>Secure login system for users.</li>
            <li>Encrypted password protection.</li>
            <li>Session-based authentication.</li>
            <li>Supports multiple login options.</li>
            <li>Ensures safe access to all tools.</li>
        </ul>
        </div>

        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# --------------------------
# Main
# --------------------------
def main():
    st.set_page_config(
        page_title="AI Job Application Agent - Features",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    render_header()
    load_custom_css()
    render_main_header()
    render_cards_section()

    if st.button("🛡️ Go to Login", type="primary", use_container_width=True):
        st.switch_page("pages/0_👤_Auth.py")

    render_footer()

if __name__ == "__main__":
    main()
