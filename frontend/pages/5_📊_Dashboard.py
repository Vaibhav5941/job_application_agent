import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.database import (
    create_enhanced_tables, add_job_application, update_application_status,
    get_user_applications, get_application_stats,delete_job_application
)

# Initialize enhanced database
create_enhanced_tables()

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
        <h1>Application Tracking Dashboard</h1>
        <p>Track, manage, and analyze all your job applications in one place with clarity and efficiency</p>
        <div class="feature-badges">
            <div class="badge">🚀 Total applications</div>
            <div class="badge">📝 Status distribution</div>
            <div class="badge">⚡ Skills match scores</div>
            <div class="badge">📊 Recent applications list</div>
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

# ============================================================================
# DASHBOARD METRICS
# ============================================================================
stats = get_application_stats(user_id)

if stats:
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.metric("Total Applications", stats.get('total', 0))
    
    with col2:
        st.metric("In Progress", stats.get('in_progress', 0))
    
    with col3:
        st.metric("Offers Received", stats.get('offers', 0))
    
    with col4:
        st.metric("This Month", stats.get('this_month', 0))
        
    with col5:
        st.metric("Offers Rejected", stats.get('rejected', 0))        
    
    with col6:
        st.metric("Success Rate", f"{stats.get('success_rate', 0)}%")

# ============================================================================
# APPLICATION STATUS PIPELINE
# ============================================================================
st.subheader("📈 Application Pipeline")

applications = get_user_applications(user_id)

if applications:
    # Convert to DataFrame for analysis
    df = pd.DataFrame(applications, columns=[
        'id', 'company_name', 'position_title', 'status', 'priority',
        'applied_date', 'deadline', 'salary_expectation', 'notes'
    ])
    
    # Status distribution chart
    status_counts = df['status'].value_counts()
    
    fig_pie = px.pie(
        values=status_counts.values,
        names=status_counts.index,
        title="Application Status Distribution",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig_pie, use_container_width=True)
    
    # Applications over time
    df['applied_date'] = pd.to_datetime(df['applied_date'])
    monthly_apps = df.groupby(df['applied_date'].dt.to_period('M')).size()
    
    if len(monthly_apps) > 1:
        fig_line = px.line(
            x=monthly_apps.index.astype(str),
            y=monthly_apps.values,
            title="Applications Over Time",
            labels={'x': 'Month', 'y': 'Number of Applications'}
        )
        st.plotly_chart(fig_line, use_container_width=True)

# ============================================================================
# QUICK ACTIONS
# ============================================================================


col1, col2 = st.columns(2)

with col1:
    if st.button("➕ Add New Application", type="primary"):
        st.session_state.show_add_form = True

with col2:
    if st.button("📧 Send Follow-up Emails"):
        st.switch_page("pages/3_✉️_Email.py")

# ============================================================================
# ADD APPLICATION FORM
# ============================================================================
if st.session_state.get('show_add_form', False):
    st.subheader("➕ Add New Job Application")
    
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
# Form buttons in columns
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

# ============================================================================
# APPLICATIONS TABLE
# ============================================================================
st.subheader("📋 Your Applications")

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
        with st.expander(f"🏢 {app[1]} - {app[2]} ({app[3].title()})"):
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
                
                if st.button(f"Update", key=f"update_{app[0]}"):
                    if new_status != app[3]:
                        try:
                            update_application_status(app[0], new_status, f"Status updated to {new_status}")
                            st.success("✅ Status updated!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Update failed: {str(e)}")
                            
            with action_col2:
                    if st.button(f"🗑️ Delete", key=f"delete_{app[0]}", type="secondary"):
                        # Confirmation dialog using session state
                        st.session_state[f"confirm_delete_{app[0]}"] = True
            
            # Delete confirmation
            if st.session_state.get(f"confirm_delete_{app[0]}", False):
                st.warning("⚠️ Are you sure you want to delete this application? This action cannot be undone.")
                
                confirm_col1, confirm_col2 = st.columns(2)
                
                with confirm_col1:
                    if st.button(f"✅ Yes, Delete", key=f"confirm_yes_{app[0]}", type="primary"):
                        try:
                            delete_job_application(app[0], user_id)
                            st.success("✅ Application deleted successfully!")
                            # Clear confirmation state
                            st.session_state[f"confirm_delete_{app[0]}"] = False
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Delete failed: {str(e)}")
                            st.session_state[f"confirm_delete_{app[0]}"] = False
                
                with confirm_col2:
                    if st.button(f"❌ Cancel", key=f"confirm_no_{app[0]}"):
                        st.session_state[f"confirm_delete_{app[0]}"] = False
                        st.rerun()                
            
            if app[8]:  # notes
                st.write(f"**Notes:** {app[8]}")
                
else:
    st.info("📝 No applications yet. Add your first application using the button above!")

# ============================================================================
# UPCOMING DEADLINES
# ============================================================================
st.subheader("⏰ Upcoming Deadlines")

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
                st.error(f"🚨 **{company} - {position}** | Deadline: {deadline} ({days_left} days left)")
            elif days_left <= 7:
                st.warning(f"⚠️ **{company} - {position}** | Deadline: {deadline} ({days_left} days left)")
            else:
                st.info(f"📅 **{company} - {position}** | Deadline: {deadline} ({days_left} days left)")
    else:
        st.success("✅ No upcoming deadlines!")
else:
    st.info("No applications with deadlines set.")

# ============================================================================
# RECOMMENDATIONS
# ============================================================================
st.subheader("💡 Recommendations")

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

# Hide add form button
if 'show_add_form' not in st.session_state:
    st.session_state.show_add_form = False