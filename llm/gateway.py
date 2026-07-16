from llm.groq_client import get_groq_response

def generate_response(prompt):

    try:
        return get_groq_response(prompt)

    except Exception as e:
        return f"Error: {e}"