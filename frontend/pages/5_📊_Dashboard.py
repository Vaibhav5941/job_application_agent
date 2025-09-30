import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.database import (
    create_enhanced_tables, add_job_application, update_application_status,
    get_user_applications, get_application_stats, delete_job_application
)
from backend.auth import get_user_by_token
from utils import SESSION_COOKIE_NAME
from frontend.components.footer import render_footer
from frontend.components.header import render_header

# Initialize enhanced database
create_enhanced_tables()

# --------------------------
# Page Configuration - FIXED FOR FULL WIDTH
# --------------------------
st.set_page_config(
    page_title="Application Dashboard - AI Job Application Agent",
    page_icon="📊",
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
# Load Custom CSS (EXACT MATCH with Auth page + Dashboard specific)
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

       
        /* Metrics card styling */
        .metrics-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
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

        /* Welcome card styling */
        .welcome-card {
            background: linear-gradient(135deg, #e3f2fd, #ede7f6);
            color: #1a237e;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            font-size: 1.1rem;
            font-weight: 600;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            border: 1px solid #c3e6cb;
            margin-bottom: 2rem;
            transition: all 0.3s ease;
        }
        .welcome-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.12);
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

        /* Form submit button - primary style */
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

        

        /* Application item styling */
        .app-item {
            background: rgba(255,255,255,0.9);
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 1rem;
            border: 1px solid #e0e0e0;
            transition: all 0.3s ease;
        }
        .app-item:hover {
            border-color: #667eea;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }

        /* Status badge styling */
        .status-badge {
            display: inline-block;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
        }
        .status-applied { background: #e3f2fd; color: #1976d2; }
        .status-viewed { background: #f3e5f5; color: #7b1fa2; }
        .status-interview { background: #e8f5e8; color: #388e3c; }
        .status-offer { background: #e8f5e8; color: #2e7d32; }
        .status-rejected { background: #ffebee; color: #d32f2f; }

        /* Deadline styling */
        .deadline-urgent { 
            background: #ffebee; 
            border-left: 4px solid #f44336; 
            padding: 0.8rem; 
            border-radius: 8px; 
            margin-bottom: 0.5rem; 
        }
        .deadline-warning { 
            background: #fff3e0; 
            border-left: 4px solid #ff9800; 
            padding: 0.8rem; 
            border-radius: 8px; 
            margin-bottom: 0.5rem; 
        }
        .deadline-info { 
            background: #e3f2fd; 
            border-left: 4px solid #2196f3; 
            padding: 0.8rem; 
            border-radius: 8px; 
            margin-bottom: 0.5rem; 
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

        /* Responsive design - Enhanced for full responsiveness */
        @media (max-width: 1200px) {
            .card { max-width: 100%; padding: 1.8rem; }
            .metrics-container { grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); }
        }

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
                grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
                gap: 0.8rem;
            }
            .metric-card { padding: 1rem; }
            .metric-value { font-size: 1.5rem; }
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
            .metrics-container { 
                grid-template-columns: 1fr 1fr;
                gap: 0.5rem;
            }
            .metric-card { 
                padding: 0.8rem; 
                border-radius: 8px;
            }
            
            .metric-value { font-size: 1.3rem; }
            .metric-label { font-size: 0.8rem; }
            
            /* Mobile form improvements */
            .stForm { padding: 0.5rem; }
            .stTextInput > div > input, 
            .stTextArea > div > textarea, 
            .stSelectbox > div > div {
                font-size: 16px; /* Prevents zoom on iOS */
            }
        }

        @media (max-width: 360px) {
            .metrics-container { grid-template-columns: 1fr; }
            .card { padding: 0.8rem; }
            .metric-card { padding: 0.6rem; }
            .metric-value { font-size: 1.2rem; }
        }
    </style>
    """, unsafe_allow_html=True)

# --------------------------
# Page Header
# --------------------------
def render_dashboard_header():
    st.markdown("""
    <div class="email-header">
        <div class="icon">📊</div>
        <h1>Application Tracking Dashboard</h1>
        <p>Track, manage, and analyze all your job applications in one place with clarity and efficiency</p>
        <div class="feature-badges">
            <div class="badge">🚀 Total Applications</div>
            <div class="badge">📝 Status Distribution</div>
            <div class="badge">⚡ Skills Match Scores</div>
            <div class="badge">📊 Recent Applications</div>
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
            <p>Please log in to access your Application Dashboard.</p>
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
# Dashboard Metrics Component
# --------------------------
def render_metrics(stats):
    if stats:
        st.markdown("""
        <div class="metrics-container">
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{stats.get('total', 0)}</div>
                <div class="metric-label">Total Applications</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{stats.get('in_progress', 0)}</div>
                <div class="metric-label">In Progress</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{stats.get('offers', 0)}</div>
                <div class="metric-label">Offers Received</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{stats.get('this_month', 0)}</div>
                <div class="metric-label">This Month</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{stats.get('rejected', 0)}</div>
                <div class="metric-label">Rejected</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col6:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{stats.get('success_rate', 0)}%</div>
                <div class="metric-label">Success Rate</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# --------------------------
# Application Pipeline Charts
# --------------------------
def render_charts(applications):
    if applications:
        # Convert to DataFrame for analysis
        df = pd.DataFrame(applications, columns=[
            'id', 'company_name', 'position_title', 'status', 'priority',
            'applied_date', 'deadline', 'salary_expectation', 'notes'
        ])
        
        
        
        
            # Create container for chart styling
        with st.container():
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                
                # Status distribution chart
                status_counts = df['status'].value_counts()
                
                fig_pie = px.pie(
                    values=status_counts.values,
                    names=status_counts.index,
                    title="Application Status Distribution",
                    color_discrete_sequence=['#667eea', '#764ba2', '#e3f2fd', '#ede7f6', '#90caf9', '#b39ddb']
                )
                
                # Enhanced styling to match theme
                fig_pie.update_layout(
                    paper_bgcolor='rgba(255,255,255,0.95)',
                    plot_bgcolor='rgba(255,255,255,0.95)',
                    font=dict(
                        family='Arial, sans-serif',
                        size=12,
                        color='#1a237e'
                    ),
                    title=dict(
                        font=dict(
                            size=16,
                            color='#1a237e',
                            family='Arial, sans-serif'
                        ),
                        x=0.5,
                        xanchor='center'
                    ),
                    margin=dict(l=20, r=20, t=60, b=20),
                    showlegend=True,
                    legend=dict(
                        orientation="v",
                        yanchor="middle",
                        y=0.5,
                        xanchor="left",
                        x=1.05,
                        font=dict(color='#1a237e')
                    )
                )
                
                # Update traces for better styling
                fig_pie.update_traces(
                    textposition='inside',
                    textinfo='percent+label',
                    textfont=dict(
                        size=11,
                        color='white'
                    ),
                    marker=dict(
                        line=dict(color='white', width=2)
                    ),
                    pull=[0.05 if i == 0 else 0 for i in range(len(status_counts))]  # Slightly pull out first slice
                )
                
                st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
                st.markdown('</div>', unsafe_allow_html=True)
        
        

# --------------------------
# Add Application Form
# --------------------------
def render_add_form(user_id):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### ➕ Add New Job Application")
    
    with st.form("add_application_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            company_name = st.text_input("Company Name*", placeholder="Google")
            position_title = st.text_input("Position Title*", placeholder="Software Engineer")
            priority = st.selectbox("Priority", ["high", "medium", "low"], index=1)
            
        with col2:
            status = st.selectbox("Status", [
                "applied", "viewed", "phone_screen", "interview", 
                "technical", "offer", "rejected", "withdrawn"
            ])
            salary_expectation = st.number_input("Expected Salary ($)", min_value=0, step=1000)
            deadline = st.date_input("Application Deadline", value=None)
        
        notes = st.text_area("Notes", placeholder="Additional information about this application...")
        
        # Form buttons
        button_col1, button_col2 = st.columns(2)
        
        with button_col1:
            submitted = st.form_submit_button("✅ Add Application", type="primary")
        
        with button_col2:
            cancelled = st.form_submit_button("❌ Cancel", type="secondary")
        
        # Handle form submission
        if submitted and company_name and position_title:
            try:
                app_id = add_job_application(
                    user_id=user_id,
                    company_name=company_name,
                    position_title=position_title,
                    status=status,
                    priority=priority,
                    notes=notes,
                    deadline=deadline,
                    salary_expectation=salary_expectation if salary_expectation > 0 else None
                )
                st.success(f"✅ Application added successfully! (ID: {app_id})")
                st.session_state.show_add_form = False
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error adding application: {str(e)}")
        elif submitted:
            st.error("⚠️ Please fill in required fields (Company Name and Position Title)")
        
        # Handle cancel button
        if cancelled:
            st.session_state.show_add_form = False
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# --------------------------
# Applications List
# --------------------------
def render_applications_list(applications, user_id):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📋 Your Applications")

    if applications:
        # Status filter
        status_options = ["All"] + list(set([app[3] for app in applications]))
        status_filter = st.selectbox("Filter by Status", status_options)
        
        # Filter applications
        filtered_apps = applications
        if status_filter != "All":
            filtered_apps = [app for app in applications if app[3] == status_filter]
        
        # Display as interactive table
        for app in filtered_apps:
            with st.expander(f"🏢 {app[1]} - {app[2]} ({app[3].replace('_', ' ').title()})"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Status:** {app[3].replace('_', ' ').title()}")
                    st.write(f"**Priority:** {app[4].title()}")
                    st.write(f"**Applied:** {app[5]}")
                
                with col2:
                    if app[6]:  # deadline
                        st.write(f"**Deadline:** {app[6]}")
                    if app[7]:  # salary_expectation
                        st.write(f"**Expected Salary:** ${app[7]:,}")
                        
                with col3:
                    # Status update
                    new_status = st.selectbox(
                        "Update Status",
                        ["applied", "viewed", "phone_screen", "interview", "technical", "offer", "rejected", "withdrawn"],
                        index=["applied", "viewed", "phone_screen", "interview", "technical", "offer", "rejected", "withdrawn"].index(app[3]),
                        key=f"status_{app[0]}"
                    )
                
                action_col1, action_col2 = st.columns(2)
                    
                with action_col1:    
                    if st.button("Update", key=f"update_{app[0]}"):
                        if new_status != app[3]:
                            try:
                                update_application_status(app[0], new_status, f"Status updated to {new_status}")
                                st.success("✅ Status updated!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Update failed: {str(e)}")
                                
                with action_col2:
                    if st.button("🗑️ Delete", key=f"delete_{app[0]}", type="secondary"):
                        st.session_state[f"confirm_delete_{app[0]}"] = True
                
                # Delete confirmation
                if st.session_state.get(f"confirm_delete_{app[0]}", False):
                    st.warning("⚠️ Are you sure you want to delete this application? This action cannot be undone.")
                    
                    confirm_col1, confirm_col2 = st.columns(2)
                    
                    with confirm_col1:
                        if st.button("✅ Yes, Delete", key=f"confirm_yes_{app[0]}", type="primary"):
                            try:
                                delete_job_application(app[0], user_id)
                                st.success("✅ Application deleted successfully!")
                                st.session_state[f"confirm_delete_{app[0]}"] = False
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Delete failed: {str(e)}")
                                st.session_state[f"confirm_delete_{app[0]}"] = False
                    
                    with confirm_col2:
                        if st.button("❌ Cancel", key=f"confirm_no_{app[0]}"):
                            st.session_state[f"confirm_delete_{app[0]}"] = False
                            st.rerun()                
                
                if app[8]:  # notes
                    st.write(f"**Notes:** {app[8]}")
                    
    else:
        st.info("📝 No applications yet. Add your first application using the button above!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# --------------------------
# Upcoming Deadlines
# --------------------------
def render_deadlines(applications):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### ⏰ Upcoming Deadlines")

    if applications:
        # Filter applications with deadlines
        upcoming = []
        today = datetime.now().date()
        
        for app in applications:
            if app[6] and app[6] >= today:  # deadline exists and is future
                days_left = (app[6] - today).days
                upcoming.append((app[1], app[2], app[6], days_left))
        
        if upcoming:
            # Sort by deadline
            upcoming.sort(key=lambda x: x[2])
            
            for company, position, deadline, days_left in upcoming:
                if days_left <= 3:
                    st.markdown(f"""
                    <div class="deadline-urgent">
                        <strong>🚨 {company} - {position}</strong><br>
                        Deadline: {deadline} ({days_left} days left)
                    </div>
                    """, unsafe_allow_html=True)
                elif days_left <= 7:
                    st.markdown(f"""
                    <div class="deadline-warning">
                        <strong>⚠️ {company} - {position}</strong><br>
                        Deadline: {deadline} ({days_left} days left)
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="deadline-info">
                        <strong>📅 {company} - {position}</strong><br>
                        Deadline: {deadline} ({days_left} days left)
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.success("✅ No upcoming deadlines!")
    else:
        st.info("No applications with deadlines set.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# --------------------------
# Recommendations
# --------------------------
def render_recommendations(applications):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 💡 Recommendations")

    if applications and len(applications) > 0:
        recent_apps = [app for app in applications if (datetime.now().date() - app[5]).days <= 7]
        
        recommendations = []
        
        if len(recent_apps) == 0:
            recommendations.append("🎯 Consider applying to 2-3 new positions this week")
        
        pending_apps = [app for app in applications if app[3] == 'applied']
        if len(pending_apps) > 3:
            recommendations.append("📞 Follow up on applications older than 1 week")
        
        interview_apps = [app for app in applications if app[3] in ['interview', 'technical']]
        if len(interview_apps) > 0:
            recommendations.append("📚 Prepare for upcoming interviews")
        
        if not recommendations:
            recommendations.append("🌟 Great job managing your applications!")
        
        for rec in recommendations:
            st.info(rec)
    
    st.markdown('</div>', unsafe_allow_html=True)

# --------------------------
# Quick Actions
# --------------------------
def render_quick_actions():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### ⚡ Quick Actions")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("📊 Analyze Resume", use_container_width=True):
            st.switch_page("pages/2_📊_Analysis.py")

    with col2:
        if st.button("✉️ Send Email", use_container_width=True):
            st.switch_page("pages/3_✉️_Email.py")

    with col3:
        if st.button("📚 View History", use_container_width=True):
            st.switch_page("pages/4_📂_History.py")

    with col4:
        if st.button("🏠 Home", use_container_width=True):
            st.switch_page("pages/1_🏠_Home.py")
    
    st.markdown('</div>', unsafe_allow_html=True)

# --------------------------
# Main Application
# --------------------------
def main():
    load_custom_css()
    render_dashboard_header()
    
    user_id, user_name = check_authentication()

    # Welcome message
    st.markdown(f"""
    <div class="welcome-card">
        👋 Welcome back, {user_name}! Ready to manage your applications?
    </div>
    """, unsafe_allow_html=True)

    # Dashboard Metrics
    stats = get_application_stats(user_id)
    render_metrics(stats)

    # Application Pipeline Charts
    applications = get_user_applications(user_id)
    render_charts(applications)

    # Quick Actions for adding applications
    st.markdown('<div class="card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        if st.button("➕ Add New Application", type="primary", use_container_width=True):
            st.session_state.show_add_form = True

    with col2:
        if st.button("📧 Send Follow-up Emails", use_container_width=True):
            st.switch_page("pages/3_✉️_Email.py")
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Add Application Form
    if st.session_state.get('show_add_form', False):
        render_add_form(user_id)

    # Applications List
    render_applications_list(applications, user_id)

    # Upcoming Deadlines
    render_deadlines(applications)

    # Recommendations
    render_recommendations(applications)

    # Quick Actions
    render_quick_actions()

    # Footer
    render_footer()

# Hide add form button
if 'show_add_form' not in st.session_state:
    st.session_state.show_add_form = False

if __name__ == "__main__":
    main()