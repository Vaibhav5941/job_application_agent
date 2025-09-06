import psycopg2
import bcrypt
from utils.config import DB_URL

def create_users_table():
    """Create users table if not exists"""
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
            
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


def signup_user(name: str, email: str, password: str, app_password: str) -> str:
    """Signup user with app password validation"""
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    try:
        # Hash the login password (not app password)
        hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        
        # Validate email is Gmail
        if not email.endswith('@gmail.com'):
            return "❌ Only Gmail accounts are supported for email sending"
        
        # Basic validation for app password (should be 16 characters)
        if len(app_password.replace(' ', '')) != 16:
            return "❌ Gmail App Password should be 16 characters (spaces will be removed)"
        
        # Remove spaces from app password
        clean_app_password = app_password.replace(' ', '')
        
        cur.execute(
            "INSERT INTO users (name, email, password, app_password) VALUES (%s, %s, %s, %s)",
            (name, email, hashed_pw, clean_app_password)
        )
        conn.commit()
        return "✅ Signup successful! Please login."
        
    except psycopg2.IntegrityError:
        return "❌ Email already exists. Please use a different email."
    except Exception as e:
        return f"❌ Signup failed: {str(e)}"
    finally:
        cur.close()
        conn.close()


def login_user(email: str, password: str) -> dict:
    """Check login credentials"""
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("SELECT id, name, email, password FROM users WHERE email=%s", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user and bcrypt.checkpw(password.encode("utf-8"), user[3].encode("utf-8")):
        return {"id": user[0], "name": user[1], "email": user[2]}
    return None
