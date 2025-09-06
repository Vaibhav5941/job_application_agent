import smtplib
import psycopg2
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.config import DB_URL

def send_email(recipient_email: str, subject: str, body: str, user_email: str) -> str:
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("SELECT app_password FROM users WHERE email=%s", (user_email,))
    result = cur.fetchone()
    cur.close()
    conn.close()

    if not result:
        return "❌ No app password found. Please update your profile with a valid Gmail App Password.."
    # Validate Gmail account
    if not user_email.endswith('@gmail.com'):
        return "❌ Only Gmail accounts are supported for sending emails."
    app_password = result[0]

    msg = MIMEMultipart()
    msg["From"] = user_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        # Connect to Gmail SMTP server
        print(f"Attempting to send email from {user_email} to {recipient_email}")
        
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Enable security
            
            # Try to login with app password
            server.login(user_email, app_password)
            
            # Send email
            text = msg.as_string()
            server.sendmail(user_email, recipient_email, text)
            
        return "✅ Email sent successfully!"
        
    except smtplib.SMTPAuthenticationError as e:
        return f"❌ Gmail authentication failed. Please check your App Password. Error: {str(e)}"
    except smtplib.SMTPRecipientsRefused as e:
        return f"❌ Invalid recipient email address. Error: {str(e)}"
    except smtplib.SMTPException as e:
        return f"❌ SMTP error occurred: {str(e)}"
    except Exception as e:
        return f"❌ Failed to send email: {str(e)}"
