from llm.gemini_client import get_gemini_response

response = get_gemini_response(
    "What is Machine Learning?"
)

print(response)