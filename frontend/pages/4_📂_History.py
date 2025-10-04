import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
import json
from datetime import datetime
from backend.database import fetch_applications, delete_application
from backend.auth import get_user_by_token
from utils import SESSION_COOKIE_NAME
from frontend.components.footer import render_footer
from frontend.components.header import render_header

# --------------------------
# Page Configuration - FIXED FOR FULL WIDTH
# --------------------------
st.set_page_config(
    page_title="Application History - AI Job Application Agent",
    page_icon="📂",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------
# Header
# --------------------------
render_header()

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

# --------------------------
# Load Custom CSS (EXACT MATCH with Auth page)
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

        /* Header - Exact match with Auth page */
        .email-header {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 1.2rem;
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
            position: relative;
            z-index: 2;
        }

        /* Feature badges */
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

        
        /* Welcome card styling */
        .welcome-card {
            background: linear-gradient(135deg, #e3f2fd, #ede7f6);
            color: #1a237e;
            padding: 0.8rem 1.2rem;
            border-radius: 12px;
            font-size: 1.1rem;
            font-weight: 600;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            border: 1px solid #90caf9;
            margin-bottom: 2rem;
            transition: all 0.3s ease;
        }
        .welcome-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.12);
        }

        /* Info card styling */
        .info-card {
            background: linear-gradient(135deg, #e3f2fd, #bbdefb);
            color: #1565c0;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            font-size: 1rem;
            font-weight: 600;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            border: 1px solid #90caf9;
            margin-bottom: 2rem;
        }

        /* Metrics container */
        .metrics-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }

        .metric-card {
            background: rgba(255,255,255,0.95);
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            transition: all 0.3s ease;
            text-align: center;
        }
        .metric-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 25px rgba(0,0,0,0.15);
            border: 1px solid rgba(102, 126, 234, 0.3);
        }

        .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: #667eea;
            margin-bottom: 0.5rem;
        }
        .metric-label {
            font-size: 0.9rem;
            color: #666;
            font-weight: 500;
        }

        /* Input styling - match Auth page */
        .stTextInput > div > input, .stTextArea > div > textarea, .stSelectbox > div > div {
            border-radius: 10px;
            border: 1px solid #90caf9;
            background: #fafafa;
            transition: all 0.3s ease;
        }
        .stTextInput > div > input:focus, .stTextArea > div > textarea:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
        }

        /* Button styling - EXACT MATCH with Auth page */
        div[data-testid="stButton"] {
            display: flex;
            justify-content: center;
        }
        div[data-testid="stButton"] > button {
            width: 100%;
            background: #e3f2fd;
            border: 1px solid #90caf9;
            padding: 0.7rem 1.2rem;
            border-radius: 50px;
            font-size: 0.95rem;
            font-weight: 600;
            color: #1a237e;
            transition: all 0.3s ease;
            cursor: pointer;
            margin-top: 1rem;
        }
        div[data-testid="stButton"] > button:hover {
            background: #ede7f6;
            border: 1px solid #b39ddb;
            color: #311b92;
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }

        /* Expander styling */
        .streamlit-expanderHeader {
            background: rgba(255,255,255,0.9);
            border-radius: 10px;
            border: 1px solid #e0e0e0;
            padding: 0.8rem;
            transition: all 0.3s ease;
        }
        .streamlit-expanderHeader:hover {
            border-color: #667eea;
            background: rgba(227, 242, 253, 0.5);
        }

        /* Content styling */
        .card h3, .card h4 {
            color: #1a237e;
            font-weight: 700;
            margin-bottom: 1rem;
        }
        .card h3 {
            font-size: clamp(1.2rem, 3vw, 1.6rem);
        }
        .card h4 {
            font-size: clamp(1rem, 2.5vw, 1.3rem);
        }

        /* Checkbox styling */
        .stCheckbox {
            padding: 0.5rem 0;
        }

        /* Success/Error message styling */
        .stSuccess, .stError, .stWarning, .stInfo {
            border-radius: 10px;
            border-left: 4px solid;
            padding: 1rem;
            margin: 1rem 0;
        }

        /* Animations - EXACT MATCH with Auth page */
        @keyframes shimmer {
            0%, 100% { transform: translateX(-100%) translateY(-100%) rotate(0deg); }
            50% { transform: translateX(-50%) translateY(-50%) rotate(180deg); }
        }
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }

        /* Responsive design - EXACT MATCH with Auth page */
        @media (max-width: 768px) {
            .email-header { padding: 1.5rem; }
            .card { margin-bottom: 1.5rem; padding: 1.5rem; }
            .email-header h1 { font-size: 1.8rem; }
            .email-header .icon { font-size: 2.5rem; }
            .feature-badges {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 0.8rem;
                margin-top: 1rem;
            }
            .badge {
                padding: 0.6rem 1rem;
                font-size: 0.85rem;
                text-align: center;
            }
            .metrics-container {
                grid-template-columns: 1fr;
            }
        }
        @media (max-width: 480px) {
            .email-header { padding: 1rem; border-radius: 12px; }
            .email-header h1 { font-size: 1.5rem; }
            .email-header .icon { font-size: 2.2rem; }
            .card { border-radius: 12px; padding: 1rem; }
            .badge {
                padding: 0.5rem 0.8rem;
                font-size: 0.8rem;
                border-radius: 8px;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# --------------------------
# Page Header
# --------------------------
def render_history_header():
    st.markdown("""
    <div class="email-header">
        <div class="icon">📂</div>
        <h1>Past Applications</h1>
        <p>Easily access and review all your previous job applications to stay organized and track progress</p>
        <div class="feature-badges">
            <div class="badge">🚀 Delete with Confirmation</div>
            <div class="badge">📝 Filter Options</div>
            <div class="badge">⚡ Application Details</div>
            <div class="badge">📊 Sort Applications</div>
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
            <p>Please log in to access your Application History.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🛡️ Go to Login", use_container_width=True):
                st.switch_page("pages/0_👤_Auth.py")
        with col2:
            if st.button("🏠 Home", use_container_width=True):
                st.switch_page("app.py")
        st.stop()
        
    return st.session_state.user["id"], st.session_state.user["name"]

# --------------------------
# Main Application
# --------------------------
def main():
    load_custom_css()
    render_history_header()
    
    user_id, user_name = check_authentication()

    # Welcome message
    st.markdown(f"""
    <div class="welcome-card">
        👋 Welcome back, {user_name}!
    </div>
    """, unsafe_allow_html=True)

    # Fetch user's applications only
    apps = fetch_applications(user_id)

    if apps:
        st.markdown(f"""
        <div class="info-card">
            Found {len(apps)} applications in your history
        </div>
        """, unsafe_allow_html=True)
        
        # Search and filter options
        st.markdown('<div class="card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            search_term = st.text_input("🔍 Search applications", placeholder="Search by company, skills, etc.")
        
        with col2:
            sort_order = st.selectbox("📅 Sort by", ["Newest First", "Oldest First"])
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Filter applications based on search
        filtered_apps = apps
        if search_term:
            filtered_apps = []
            for app in apps:
                # Search in skills_match and cover_letter
                skills_text = str(app[1]).lower() if app[1] else ""
                cover_letter_text = str(app[2]).lower() if app[2] else ""
                
                if (search_term.lower() in skills_text or 
                    search_term.lower() in cover_letter_text):
                    filtered_apps.append(app)
        
        # Sort applications
        apps_to_display = filtered_apps.copy()
        if sort_order == "Oldest First":
            apps_to_display.reverse()
        
        if apps_to_display:
            # Create user-specific numbering based on creation order
            all_user_apps = sorted(apps, key=lambda x: x[3])  # Sort by created_at
            app_id_to_user_number = {}
            
            for idx, app in enumerate(all_user_apps, 1):
                app_id_to_user_number[app[0]] = idx
            
            for i, app in enumerate(apps_to_display):
                app_id = app[0]
                skills_match = app[1]
                cover_letter = app[2]
                created_at = app[3]
                
                # Get user-specific application number
                user_app_number = app_id_to_user_number[app_id]
                
                with st.expander(f"📋 Application #{user_app_number} - {created_at.strftime('%B %d, %Y')}"):
                    
                    # Application details in columns
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**📌 Application Number:** {user_app_number}")
                        st.write(f"**🕒 Created:** {created_at.strftime('%B %d, %Y at %I:%M %p')}")
                    
                    with col2:
                        # Delete button with confirmation
                        if st.button(f"🗑️ Delete", key=f"delete_{app_id}", type="secondary"):
                            st.session_state[f"confirm_delete_{app_id}"] = True
                            
                    # Delete confirmation dialog
                    if st.session_state.get(f"confirm_delete_{app_id}", False):
                        st.error("⚠️ **Delete Confirmation**")
                        st.write("Are you sure you want to delete this application? This action cannot be undone.")
                        
                        confirm_col1, confirm_col2 = st.columns(2)
                        
                        with confirm_col1:
                            if st.button(f"✅ Yes, Delete", key=f"confirm_yes_{app_id}", type="primary"):
                                try:
                                    delete_application(app_id, user_id)
                                    st.success(f"✅ Application #{user_app_number} deleted successfully!")
                                    st.session_state[f"confirm_delete_{app_id}"] = False
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"❌ Delete failed: {str(e)}")
                                    st.session_state[f"confirm_delete_{app_id}"] = False
                        
                        with confirm_col2:
                            if st.button(f"❌ Cancel", key=f"confirm_no_{app_id}"):
                                st.session_state[f"confirm_delete_{app_id}"] = False
                                st.rerun()
                    
                    st.markdown("---")        
                    
                    # Skills Analysis Section
                    st.subheader("📊 Skills Analysis")
                    if skills_match:
                        try:
                            # Try to parse as JSON for better display
                            skills_data = json.loads(skills_match)
                            
                            # Display key metrics
                            if 'match_percentage' in skills_data:
                                st.metric("🎯 Match Percentage", skills_data['match_percentage'])
                            
                            skill_col1, skill_col2 = st.columns(2)
                            
                            with skill_col1:
                                if 'matching_skills' in skills_data and skills_data['matching_skills']:
                                    st.success("✅ **Matching Skills:**")
                                    for skill in skills_data['matching_skills']:
                                        st.write(f"• {skill}")
                            
                            with skill_col2:
                                if 'missing_skills' in skills_data and skills_data['missing_skills']:
                                    st.warning("⚠️ **Missing Skills:**")
                                    for skill in skills_data['missing_skills']:
                                        st.write(f"• {skill}")
                            
                            # Detailed JSON view with toggle
                            if st.checkbox(f"🔍 Show Detailed Skills Data", key=f"details_{app_id}"):
                                st.json(skills_data)
                                
                        except json.JSONDecodeError:
                            # Fallback for non-JSON data
                            st.text_area("Skills Analysis:", skills_match, height=100, key=f"skills_{app_id}")
                    else:
                        st.info("No skills analysis data available")
                    
                    # Cover Letter Section
                    st.subheader("📄 Cover Letter")
                    if cover_letter:
                        st.write(cover_letter)
                        
                        # Copy button for cover letter
                        if st.checkbox(f"📄 Show Cover Letter Text", key=f"show_cover_{app_id}"):
                            st.text_area("Copy Cover Letter:", cover_letter, height=200, key=f"cover_{app_id}")
                    else:
                        st.info("No cover letter generated")
                    
                    
        
        else:
            st.warning("No applications found matching your search criteria")
            
    else:
        st.markdown('<div class="card" style="text-align: center;">', unsafe_allow_html=True)
        st.info("📝 No applications found in your history")
        st.markdown("### Get Started")
        st.write("Upload your first resume and job description to start tracking your applications!")
        
        if st.button("📊 Go to Analysis Page", type="primary"):
            st.switch_page("pages/2_📊_Analysis.py")
        st.markdown('</div>', unsafe_allow_html=True)

    # Summary statistics
    if apps:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📈 Your Application History")
        
        total_apps = len(apps)
        recent_apps = len([app for app in apps if (datetime.now() - app[3]).days <= 30])
        
        st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{total_apps}</div>
                <div class="metric-label">Total Applications</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{recent_apps}</div>
                <div class="metric-label">This Month</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            avg_per_month = round(total_apps / max(1, (datetime.now() - min(app[3] for app in apps)).days / 30), 1)
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{avg_per_month}</div>
                <div class="metric-label">Avg per Month</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Quick actions
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### ⚡ Quick Actions")

    action_col1, action_col2 = st.columns(2)

    with action_col1:
        if st.button("📊 New Analysis", type="primary", use_container_width=True):
            st.switch_page("pages/2_📊_Analysis.py")

    with action_col2:
        if st.button("📈 View Dashboard", use_container_width=True):
            st.switch_page("pages/5_📊_Dashboard.py")
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    render_footer()

if __name__ == "__main__":
    main()