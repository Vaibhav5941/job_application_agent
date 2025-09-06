from langchain_cohere import ChatCohere
from langchain_core.messages import HumanMessage
from utils.config import COHERE_API_KEY

llm = ChatCohere(model="command-r-plus", temperature=0.3, cohere_api_key=COHERE_API_KEY)

def generate_cover_letter(resume_text: str, jd_text: str) -> str:
    """
    Generates a tailored cover letter for the given job description.
    """
    prompt = f"""
    Write a professional cover letter tailored to this job description
    using the candidate's resume.

    Resume: {resume_text}
    Job Description: {jd_text}
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content
