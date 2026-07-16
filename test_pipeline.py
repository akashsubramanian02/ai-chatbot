from nlp.preprocess import clean_text
from nlp.sentiment import analyze_sentiment

from memory.memory_manager import (
    save_chat,
    get_recent_history
)

from utils.helpers import build_prompt

from llm.gateway import generate_response

user_input = """
I am preparing for AI interviews.
Can you explain machine learning?
"""

cleaned = clean_text(
    user_input
)

sentiment = analyze_sentiment(
    cleaned
)

history = get_recent_history(
    1
)

prompt = build_prompt(
    cleaned,
    history
)

response = generate_response(
    prompt
)

save_chat(
    1,
    user_input,
    response,
    sentiment
)

print(response)