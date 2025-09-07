import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
import json
from datetime import datetime
from backend.database import fetch_applications, delete_application

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
        <h1>Past Applications</h1>
        <p>Easily access and review all your previous job applications to stay organized and track progress</p>
        <div class="feature-badges">
            <div class="badge">🚀 Delete with confirmation</div>
            <div class="badge">📝 filter options</div>
            <div class="badge">⚡ Application details</div>
            <div class="badge">📊 Sort applications list</div>
        </div>
    </div>
    
""", unsafe_allow_html=True)

# Authentication check
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

st.success(f"Welcome back, {user_name}! 👋")

# Fetch user's applications only
apps = fetch_applications(user_id)

if apps:
    st.info(f"Found {len(apps)} applications in your history")
    
    # Add search and filter options
    col1, col2 = st.columns(2)
    
    with col1:
        search_term = st.text_input("🔍 Search applications", placeholder="Search by company, skills, etc.")
    
    with col2:
        sort_order = st.selectbox("📅 Sort by", ["Newest First", "Oldest First"])
    
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
        # Get all user apps in creation order to assign proper numbers
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
                        
                        # Detailed JSON view with toggle instead of nested expander
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
                    
                    # Copy button for cover letter - make text area smaller and add copy functionality
                    if st.checkbox(f"📄 Show Cover Letter Text", key=f"show_cover_{app_id}"):
                        st.text_area("Copy Cover Letter:", cover_letter, height=200, key=f"cover_{app_id}")
                else:
                    st.info("No cover letter generated")
                
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
    
    else:
        st.warning("No applications found matching your search criteria")
        
else:
    st.info("📝 No applications found in your history")
    st.markdown("### Get Started")
    st.write("Upload your first resume and job description to start tracking your applications!")
    
    if st.button("📊 Go to Analysis Page", type="primary"):
        st.switch_page("pages/2_📊_Analysis.py")

# Summary statistics
if apps:
    st.markdown("---")
    st.subheader("📈 Your Application History")
    
    total_apps = len(apps)
    recent_apps = len([app for app in apps if (datetime.now() - app[3]).days <= 30])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Applications", total_apps)
    
    with col2:
        st.metric("This Month", recent_apps)
    
    with col3:
        avg_per_month = round(total_apps / max(1, (datetime.now() - min(app[3] for app in apps)).days / 30), 1)
        st.metric("Avg per Month", avg_per_month)

# Quick actions
st.markdown("---")
st.subheader("⚡ Quick Actions")

action_col1, action_col2 = st.columns(2)

with action_col1:
    if st.button("📊 New Analysis", type="primary"):
        st.switch_page("pages/2_📊_Analysis.py")

with action_col2:
    if st.button("📈 View Dashboard"):
        st.switch_page("pages/5_📊_Dashboard.py")