import psycopg2
import json
import re
from datetime import datetime, timedelta
from utils.config import DB_URL

def clean_json_response(response_text: str) -> str:
    """Clean LLM response to extract valid JSON"""
    try:
        # Remove markdown code blocks
        cleaned = re.sub(r'```json\s*', '', response_text)
        cleaned = re.sub(r'```\s*$', '', cleaned)
        cleaned = cleaned.strip()
        
        # Validate it's proper JSON
        json.loads(cleaned)
        return cleaned
    except json.JSONDecodeError:
        # If parsing fails, create a fallback JSON structure
        fallback = {
            "match_percentage": "0%",
            "matching_skills": [],
            "missing_skills": [],
            "raw_response": response_text
        }
        return json.dumps(fallback)

def save_application(resume_text: str, jd_text: str, skills: str, cover_letter: str):
    """Save application data to database with proper error handling"""
    conn = None
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        # Clean the skills JSON if needed
        clean_skills = clean_json_response(skills)
        
        cur.execute("""
            INSERT INTO applications (resume_text, jd_text, skills_match, cover_letter)
            VALUES (%s, %s, %s, %s)
        """, (resume_text, jd_text, clean_skills, cover_letter))
        
        conn.commit()
        cur.close()
        
    except Exception as e:
        print(f"Database error: {e}")
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

def fetch_applications():
    """Fetch all applications from database"""
    conn = None
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        cur.execute("""
            SELECT id, skills_match, cover_letter, created_at 
            FROM applications 
            ORDER BY created_at DESC
        """)
        
        rows = cur.fetchall()
        cur.close()
        
        return rows
        
    except Exception as e:
        print(f"Database fetch error: {e}")
        return []
    finally:
        if conn:
            conn.close()
        
def delete_application(app_id: int):
    """Delete a specific application by ID"""
    conn = None
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("DELETE FROM applications WHERE id = %s", (app_id,))
        conn.commit()
        cur.close()
    except Exception as e:
        print(f"Database delete error: {e}")
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()
            
            

def create_enhanced_tables():
    """Create enhanced database schema for application tracking"""
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    try:
        # Companies table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL UNIQUE,
                industry VARCHAR(100),
                website VARCHAR(255),
                glassdoor_rating FLOAT,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        
        # Jobs table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id SERIAL PRIMARY KEY,
                company_id INT REFERENCES companies(id) ON DELETE CASCADE,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                requirements TEXT,
                salary_min INT,
                salary_max INT,
                location VARCHAR(255),
                job_type VARCHAR(50) DEFAULT 'full-time', -- full-time, part-time, contract
                remote BOOLEAN DEFAULT FALSE,
                posted_date DATE DEFAULT CURRENT_DATE,
                deadline DATE,
                source VARCHAR(100) DEFAULT 'manual', -- manual, linkedin, indeed
                job_url VARCHAR(500),
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        
        # Enhanced applications table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS job_applications (
                id SERIAL PRIMARY KEY,
                user_id INT REFERENCES users(id) ON DELETE CASCADE,
                job_id INT REFERENCES jobs(id) ON DELETE CASCADE,
                company_name VARCHAR(255) NOT NULL, -- Denormalized for quick access
                position_title VARCHAR(255) NOT NULL,
                status VARCHAR(50) DEFAULT 'applied', 
                -- Status options: applied, viewed, phone_screen, interview, technical, offer, rejected, withdrawn
                priority VARCHAR(20) DEFAULT 'medium', -- high, medium, low
                resume_version TEXT,
                cover_letter TEXT,
                skills_match TEXT, -- JSON data
                notes TEXT,
                applied_date DATE DEFAULT CURRENT_DATE,
                last_updated TIMESTAMP DEFAULT NOW(),
                deadline DATE,
                salary_expectation INT,
                follow_up_date DATE,
                interview_date TIMESTAMP,
                offer_amount INT
            )
        """)
        
        # Application timeline/activity log
        cur.execute("""
            CREATE TABLE IF NOT EXISTS application_timeline (
                id SERIAL PRIMARY KEY,
                application_id INT REFERENCES job_applications(id) ON DELETE CASCADE,
                status VARCHAR(50) NOT NULL,
                notes TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        
        # Interview tracking
        cur.execute("""
            CREATE TABLE IF NOT EXISTS interviews (
                id SERIAL PRIMARY KEY,
                application_id INT REFERENCES job_applications(id) ON DELETE CASCADE,
                interview_type VARCHAR(50), -- phone, video, onsite, technical
                scheduled_date TIMESTAMP,
                interviewer_name VARCHAR(255),
                interviewer_email VARCHAR(255),
                notes TEXT,
                feedback TEXT,
                result VARCHAR(50), -- passed, failed, pending
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        
        conn.commit()
        print("✅ Enhanced database tables created successfully!")
        
    except Exception as e:
        print(f"Database creation error: {e}")
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

# Application Management Functions
def add_job_application(user_id, company_name, position_title, job_description="", 
                       status="applied", priority="medium", notes="", deadline=None,
                       salary_expectation=None):
    """Add new job application"""
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    try:
        cur.execute("""
            INSERT INTO job_applications 
            (user_id, company_name, position_title, status, priority, notes, 
             deadline, salary_expectation)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (user_id, company_name, position_title, status, priority, 
              notes, deadline, salary_expectation))
        
        app_id = cur.fetchone()[0]
        
        # Add to timeline
        cur.execute("""
            INSERT INTO application_timeline (application_id, status, notes)
            VALUES (%s, %s, %s)
        """, (app_id, status, f"Application created: {notes}"))
        
        conn.commit()
        return app_id
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

def update_application_status(app_id, new_status, notes=""):
    """Update application status and log timeline"""
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    try:
        # Update application
        cur.execute("""
            UPDATE job_applications 
            SET status = %s, last_updated = NOW()
            WHERE id = %s
        """, (new_status, app_id))
        
        # Add to timeline
        cur.execute("""
            INSERT INTO application_timeline (application_id, status, notes)
            VALUES (%s, %s, %s)
        """, (app_id, new_status, notes))
        
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

def get_user_applications(user_id, status_filter=None):
    """Get all applications for a user"""
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    try:
        query = """
            SELECT id, company_name, position_title, status, priority, 
                   applied_date, deadline, salary_expectation, notes
            FROM job_applications 
            WHERE user_id = %s
        """
        params = [user_id]
        
        if status_filter:
            query += " AND status = %s"
            params.append(status_filter)
            
        query += " ORDER BY last_updated DESC"
        
        cur.execute(query, params)
        applications = cur.fetchall()
        
        return applications
        
    except Exception as e:
        print(f"Error fetching applications: {e}")
        return []
    finally:
        cur.close()
        conn.close()

def get_application_stats(user_id):
    """Get application statistics"""
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    try:
        # Overall stats
        cur.execute("""
            SELECT 
                COUNT(*) as total_applications,
                COUNT(CASE WHEN status = 'applied' THEN 1 END) as applied,
                COUNT(CASE WHEN status IN ('phone_screen', 'interview', 'technical') THEN 1 END) as in_progress,
                COUNT(CASE WHEN status = 'offer' THEN 1 END) as offers,
                COUNT(CASE WHEN status = 'rejected' THEN 1 END) as rejected
            FROM job_applications 
            WHERE user_id = %s
        """, (user_id,))
        
        stats = cur.fetchone()
        
        # This month stats
        cur.execute("""
            SELECT COUNT(*) as this_month
            FROM job_applications 
            WHERE user_id = %s 
            AND applied_date >= DATE_TRUNC('month', CURRENT_DATE)
        """, (user_id,))
        
        this_month = cur.fetchone()[0]
        
        return {
            'total': stats[0],
            'applied': stats[1],
            'in_progress': stats[2],
            'offers': stats[3],
            'rejected': stats[4],
            'this_month': this_month,
            'success_rate': round((stats[3] / max(stats[0], 1)) * 100, 1)
        }
        
    except Exception as e:
        print(f"Error getting stats: {e}")
        return {}
    finally:
        cur.close()
        conn.close()            
  