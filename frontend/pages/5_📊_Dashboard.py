import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.database import (
    create_enhanced_tables, add_job_application, update_application_status,
    get_user_applications, get_application_stats
)

# Initialize enhanced database
create_enhanced_tables()

st.title("📊 Application Tracking Dashboard")

# Check authentication
if "user" not in st.session_state or not st.session_state.user:
    st.warning("⚠️ Please log in to view your dashboard")
    st.info("👈 Go to the Auth page to log in")
    st.stop()

user_id = st.session_state.user["id"]
user_name = st.session_state.user["name"]

st.success(f"Welcome back, {user_name}! 👋")

# ============================================================================
# DASHBOARD METRICS
# ============================================================================
stats = get_application_stats(user_id)

if stats:
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Applications", stats.get('total', 0))
    
    with col2:
        st.metric("In Progress", stats.get('in_progress', 0))
    
    with col3:
        st.metric("Offers Received", stats.get('offers', 0))
    
    with col4:
        st.metric("This Month", stats.get('this_month', 0))
    
    with col5:
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
st.subheader("⚡ Quick Actions")

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
        
        submitted = st.form_submit_button("Add Application")
        
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
                
                if st.button(f"Update", key=f"update_{app[0]}"):
                    if new_status != app[3]:
                        try:
                            update_application_status(app[0], new_status, f"Status updated to {new_status}")
                            st.success("✅ Status updated!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Update failed: {str(e)}")
            
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