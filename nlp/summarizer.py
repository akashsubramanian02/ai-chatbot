from llm.groq_client import get_groq_response


def summarize_text(text):

    prompt = f"""
    Summarize the following text in 3 lines:

    {text}
    """

    return get_groq_response(prompt)