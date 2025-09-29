import streamlit as st

# Header component
def render_header():
    st.markdown(
        """
        <style>
        .header {
            background-color: #2E86C1;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            color: white;
            font-size: 24px;
            font-weight: bold;
        }
        </style>
        <div class="header">
            🚀 Job Application Agent
        </div>
        """,
        unsafe_allow_html=True
    )