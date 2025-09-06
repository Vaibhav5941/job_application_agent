# import streamlit as st
# from backend.email_sender import send_email
# import sys, os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# st.title("✉️ Send Application Email")

# # Pre-fill recipient as logged-in user's email
# if "user" in st.session_state and st.session_state.user:
#     recipient = st.text_input("Recipient Email", value=st.session_state.user["email"])
# else:
#     recipient = st.text_input("Recipient Email")

# subject = st.text_input("Email Subject", "Job Application")
# body = st.text_area("Email Body")

# if st.button("Send Email"):
#     if recipient and subject and body:
#         if "user" in st.session_state and st.session_state.user:
#             # Pass user email (from login session) to send_email
#             status = send_email(recipient, subject, body, st.session_state.user["email"])
#             st.success(status)
#         else:
#             st.error("⚠️ You must log in first to send an email.")
import streamlit as st
from backend.email_sender import send_email
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

st.title("✉️ Send Application Email")

# Check if user is logged in
if "user" not in st.session_state or not st.session_state.user:
    st.warning("⚠️ Please log in first to send emails")
    st.info("👈 Go to the User Authentication page to log in")
    st.stop()

# Show logged-in user info
st.success(f"📧 Sending from: {st.session_state.user['email']}")

# Email form
recipient = st.text_input("Recipient Email", 
                         placeholder="hr@company.com",
                         help="Email address of the hiring manager or HR")

subject = st.text_input("Email Subject", 
                       value="Job Application - [Your Name]",
                       help="Clear subject line for your application")

body = st.text_area("Email Body", 
                   height=300,
                   placeholder="""Dear Hiring Manager,

I am writing to express my interest in the [Job Title] position at [Company Name].

Please find attached my resume for your consideration. I believe my skills and experience make me a strong candidate for this role.

Thank you for your time and consideration. I look forward to hearing from you.

Best regards,
[Your Name]""",
                   help="Write your cover letter or application message")

# Send email button
if st.button("Send Email", type="primary"):
    if recipient and subject and body:
        with st.spinner("Sending email..."):
            status = send_email(recipient, subject, body, st.session_state.user["email"])
            
            if "✅" in status:
                st.success(status)
                st.balloons()
            else:
                st.error(status)
                
                # Show troubleshooting tips for common errors
                if "authentication failed" in status.lower():
                    st.info("""
                    🔧 **Troubleshooting Gmail Authentication:**
                    1. Make sure you've enabled 2-Factor Authentication
                    2. Generate a new App Password from Google Account settings
                    3. Use the App Password, not your regular Gmail password
                    4. Make sure there are no spaces in the App Password
                    """)
    else:
        st.error("⚠️ Please fill all fields before sending")

# Add helpful tips
with st.expander("💡 Email Tips"):
    st.markdown("""
    **For better results:**
    - Use a clear, professional subject line
    - Personalize the email with company and position details
    - Keep it concise but comprehensive
    - Include relevant attachments (resume, portfolio)
    - Proofread before sending
    - Follow up after a week if no response
    """)