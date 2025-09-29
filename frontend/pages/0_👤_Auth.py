import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from frontend.components.footer import render_footer
from frontend.components.header import render_header

from backend.auth import (
    create_users_table,
    signup_user,
    login_user,
    create_sessions_table,
    create_session,
    get_user_by_token,
    delete_session,
)
from utils import SESSION_COOKIE_NAME, SESSION_TTL_HOURS

st.set_page_config(
    page_title="AI Job Application Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# --------------------------
# Ensure users and sessions tables exist
# --------------------------
create_users_table()
create_sessions_table()

# --------------------------
# Render Header
# --------------------------
render_header()

# --------------------------
# Load Custom CSS (matching first page theme)
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

    /* Header */
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

    /* Card for forms */
    .card {
       
        padding: 0rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 0 auto 2rem auto;
        text-align: left;
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
        max-width: 600px;
        width: 90%;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
        border: 1px solid rgba(102, 126, 234, 0.3);
    }

    /* Input and button */
    .stTextInput > div > input {
        width: 100%;
        padding: 0.8rem 1rem;
        border-radius: 10px;
    }
    div[data-testid="stButton"] {
    display: flex;
    justify-content: center;
}
div[data-testid="stButton"] > button {
    width: 40%;  /* keep your size */
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

    /* Tabs styling */
    button[role="tab"] {
        background-color: #e3f2fd;
        border: 1px solid #90caf9;
        border-radius: 50px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        color: #1a237e;
        margin: 0 0.3rem;
        transition: all 0.3s ease;
    }
    button[role="tab"][aria-selected="true"] {
        background-color: #667eea;
        color: white;
        border: 1px solid #764ba2;
    }
    button[role="tab"]:hover {
        background-color: #ede7f6;
        border-color: #b39ddb;
        color: #311b92;
        transform: translateY(-1px);
    }

    /* Animations */
    @keyframes shimmer {
        0%, 100% { transform: translateX(-100%) translateY(-100%) rotate(0deg); }
        50% { transform: translateX(-50%) translateY(-50%) rotate(180deg); }
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }

    /* Responsive */
    @media (max-width: 768px) {
        .email-header { padding: 1.5rem; }
        .card { margin-bottom: 1.5rem; }
        .email-header h1 { font-size: 1.8rem; }
        .email-header .icon { font-size: 2.5rem; }
    }
    @media (max-width: 480px) {
        .email-header { padding: 1rem; border-radius: 12px; }
        .email-header h1 { font-size: 1.5rem; }
        .email-header .icon { font-size: 2.2rem; }
        .card { border-radius: 12px; }
    }
 </style>
 """, unsafe_allow_html=True)

# --------------------------
# Header
# --------------------------
def render_main_header():
 st.markdown("""
 <div class="email-header">
    <div class="icon">🛡️</div>
    <h1>User Authentication</h1>
    <p>Securely login or create an account to track your applications and resumes.</p>
 </div>
 """, unsafe_allow_html=True)

# --------------------------
# Session Initialization
# --------------------------
def handle_authentication():
 if "user" not in st.session_state: st.session_state.user = None
 if "session_token" not in st.session_state: st.session_state.session_token = None

# Try hydrating user from cookie
 if not st.session_state.user:
    try:
        token = st.session_state.session_token or st.experimental_get_cookie(SESSION_COOKIE_NAME)
        if token:
            user = get_user_by_token(token)
            if user:
                st.session_state.user = user
                st.session_state.session_token = token
    except Exception:
        pass

# --------------------------
# Logged-in view
# --------------------------
def render_logged_in_view():
 
    st.markdown(f"""
    <div class="card" style="text-align:center;">
        <h2>Welcome, {st.session_state.user['name']} 👋</h2>
        <p>📧 Logged in as: {st.session_state.user['email']}</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("✖️ Logout", type="primary"):
        try:
            if st.session_state.session_token:
                delete_session(st.session_state.session_token)
        except Exception:
            pass
        st.session_state.user = None
        st.session_state.session_token = None
        try: st.experimental_set_cookie(SESSION_COOKIE_NAME, "", 0)
        except Exception: pass
        st.rerun()

# --------------------------
# Login/Signup Tabs
# --------------------------
def render_login_signup_tabs():

    tab1, tab2 = st.tabs(["🛡️ Login", "🆕 Signup"])

    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Login to Your Account")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login", type="primary"):
            if email and password:
                user = login_user(email, password)
                if user:
                    st.session_state.user = user
                    try:
                        token = create_session(user["id"], ttl_hours=SESSION_TTL_HOURS)
                        st.session_state.session_token = token
                        st.experimental_set_cookie(SESSION_COOKIE_NAME, token, max_age=SESSION_TTL_HOURS*3600)
                    except Exception: pass
                    st.success(f"✅ Logged in as {user['name']}")
                    st.rerun()
                else:
                    st.error("❌ Invalid email or password")
            else:
                st.error("⚠️ Please enter email and password")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Create New Account")
        name = st.text_input("Full Name", key="signup_name")
        new_email = st.text_input("Gmail Address", placeholder="example@gmail.com", key="signup_email")
        new_password = st.text_input("Password", type="password", key="signup_password")
        app_password = st.text_input("Gmail App Password", type="password", placeholder="16-character app password", key="signup_app_password")
        if st.button("Create Account", type="primary"):
            if name and new_email and new_password and app_password:
                msg = signup_user(name, new_email, new_password, app_password)
                if "✅" in msg:
                    st.success(msg)
                    st.info("✅ Now you can log in with your credentials.")
                else:
                    st.error(msg)
            else:
                st.error("⚠️ Please fill all fields")
        st.markdown('</div>', unsafe_allow_html=True)

# --------------------------
# Footer
# --------------------------
def main():
    load_custom_css()
   
    handle_authentication()
    render_main_header()

    if st.session_state.user:
        render_logged_in_view()
    else:
        render_login_signup_tabs()

    render_footer()

if __name__ == "__main__":
    main()
