import psycopg2
import bcrypt
import uuid
from datetime import datetime, timedelta
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
            password TEXT NOT NULL,
            app_password TEXT
            
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


# ---------------- Session Management ----------------
def create_sessions_table():
    """Create persistent sessions table for login tokens"""
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            user_id INT REFERENCES users(id) ON DELETE CASCADE,
            expires_at TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


def create_session(user_id: int, ttl_hours: int = 72) -> str:
    """Create a session token for the user and store with expiry"""
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    token = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(hours=ttl_hours)
    cur.execute(
        "INSERT INTO sessions (token, user_id, expires_at) VALUES (%s, %s, %s)",
        (token, user_id, expires_at)
    )
    conn.commit()
    cur.close()
    conn.close()
    return token


def get_user_by_token(token: str) -> dict | None:
    """Return user dict if token valid and not expired"""
    if not token:
        return None
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT u.id, u.name, u.email
        FROM sessions s
        JOIN users u ON u.id = s.user_id
        WHERE s.token = %s AND s.expires_at > NOW()
        """,
        (token,)
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return {"id": row[0], "name": row[1], "email": row[2]}
    return None


def delete_session(token: str) -> None:
    """Invalidate a session token"""
    if not token:
        return
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("DELETE FROM sessions WHERE token = %s", (token,))
    conn.commit()
    cur.close()
    conn.close()

