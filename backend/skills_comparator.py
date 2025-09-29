from langchain_cohere import ChatCohere
from langchain_core.messages import HumanMessage
import json
import re
from utils.config import COHERE_API_KEY

# Initialize Cohere model
llm = ChatCohere(model="command-a-03-2025", temperature=0, cohere_api_key=COHERE_API_KEY)

def clean_llm_response(response: str) -> str:
    """Clean LLM response to extract valid JSON"""
    try:
        # Remove markdown code blocks
        cleaned = re.sub(r'```json\s*', '', response)
        cleaned = re.sub(r'```\s*', '', cleaned)
        cleaned = cleaned.strip()
        
        # Find JSON object in the response
        json_match = re.search(r'\{.*\}', cleaned, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            # Validate JSON
            json.loads(json_str)
            return json_str
        else:
            raise ValueError("No JSON object found in response")
            
    except (json.JSONDecodeError, ValueError) as e:
        print(f"JSON cleaning error: {e}")
        # Return minimal valid JSON
        return json.dumps({
            "match_percentage": "0%",
            "matching_skills": [],
            "missing_skills": [],
            "recommendations": ["Unable to parse analysis results"]
        })

def compare_skills(resume_text: str, jd_text: str) -> str:
    """
    Compare resume and job description, return skills match analysis.
    Returns clean JSON string.
    """
    try:
        prompt = f"""
        Compare the following resume and job description and analyze the skill match.

        Resume: {resume_text}

        Job Description: {jd_text}

        Please analyze and return ONLY a valid JSON response with this exact structure:
        {{
          "match_percentage": "XX%",
          "matching_skills": ["skill1", "skill2", "skill3"],
          "missing_skills": ["missing_skill1", "missing_skill2"],
          "recommendations": ["Add experience in...", "Consider learning..."]
        }}

        Important: Return ONLY the JSON object, no markdown formatting, no explanations.
        """
        
        response = llm.invoke([HumanMessage(content=prompt)])
        response_content = response.content.strip()
        
        # Clean the response
        cleaned_response = clean_llm_response(response_content)
        
        return cleaned_response
        
    except Exception as e:
        print(f"Skills comparison error: {e}")
        # Return fallback JSON
        fallback = {
            "match_percentage": "0%",
            "matching_skills": [],
            "missing_skills": [],
            "recommendations": [f"Error occurred during analysis: {str(e)}"],
            "error": True
        }
        return json.dumps(fallback)