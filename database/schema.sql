-- Create applications table
CREATE TABLE IF NOT EXISTS applications (
    id SERIAL PRIMARY KEY,
    resume_text TEXT NOT NULL,
    jd_text TEXT NOT NULL,
    skills_match JSON,
    cover_letter TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
