import streamlit as st

def render_footer():
    """Render a fixed footer at the bottom of the page"""
    st.markdown("""
    <style>
        /* Push main content up so footer is visible */
        .stApp {
            padding-bottom: 70px; /* equal to footer height */
        }

        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
            color: white;
            text-align: center;
            padding: 0.8rem;
            font-size: 0.9rem;
            font-weight: 500;
            z-index: 1000; /* ensure it stays above other elements */
            box-shadow: 0 -4px 15px rgba(0,0,0,0.2);
        }
        .footer a {
            color: #ffeb3b;
            text-decoration: none;
            margin: 0 0.6rem;
            font-weight: 600;
        }
        .footer a:hover {
            text-decoration: underline;
        }
    </style>

    <div class="footer">
        © 2025 AI Job Application Agent | Built by Vaibhav Gupta  
        <a href="https://github.com/your-github" target="_blank">GitHub</a> | 
        <a href="https://www.linkedin.com/in/your-linkedin" target="_blank">LinkedIn</a> | 
        <a href="mailto:your-email@example.com">Contact</a>
    </div>
    """, unsafe_allow_html=True)
