import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.auth import create_users_table, signup_user, login_user

# Ensure users table exists
create_users_table()

st.title("👤 User Authentication")

if "user" not in st.session_state:
    st.session_state.user = None

# If logged in → show logout
if st.session_state.user:
    st.success(f"Welcome, {st.session_state.user['name']} 👋")
    st.info(f"📧 Logged in as: {st.session_state.user['email']}")
    
    if st.button("Logout",type="primary"):
        st.session_state.user = None
        st.rerun()

else:
    tab1, tab2 = st.tabs(["🔑 Login", "🆕 Signup"])

    # ------------------ LOGIN ------------------
    with tab1:
        st.subheader("Login to Your Account")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", type="primary"):
            if email and password:
                user = login_user(email, password)
                if user:
                    st.session_state.user = user
                    st.success(f"✅ Logged in as {user['name']}")
                    st.rerun()
                else:
                    st.error("❌ Invalid email or password")
            else:
                st.error("⚠️ Please enter email and password")

    # ------------------ SIGNUP ------------------
    with tab2:
        st.subheader("Create New Account")
        
        # Instructions for Gmail App Password
        with st.expander("📋 How to get Gmail App Password", expanded=True):
            st.markdown("""
            **Follow these steps:**
            1. Go to your Google Account settings
            2. Click on **Security** in the left sidebar
            3. Under "Signing in to Google", click **App passwords**
            4. Select **Mail** and **Other (Custom name)**
            5. Enter a name like "Resume App" 
            6. Copy the 16-character password and paste below
            
            ⚠️ **Important:** You need 2-Factor Authentication enabled to use App Passwords
            """)
        
        name = st.text_input("Full Name", key="signup_name")
        new_email = st.text_input("Gmail Address", 
                                 placeholder="example@gmail.com",
                                 key="signup_email")
        new_password = st.text_input("Password", type="password", key="signup_password")
        app_password = st.text_input("Gmail App Password", 
                                   type="password",
                                   placeholder="16-character app password",
                                   help="Generate from Google Account > Security > App Passwords",
                                   key="signup_app_password")
        
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
