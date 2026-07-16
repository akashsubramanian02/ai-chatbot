from llm.groq_client import get_groq_response

response = get_groq_response(
    "What is Machine Learning?"
)

print(response)