def build_prompt(
    user_input,
    history
):

    prompt = """
You are a helpful AI assistant.

Conversation History:
"""

    for user_msg, bot_msg in history:

        prompt += f"""

User: {user_msg}

Assistant: {bot_msg}
"""

    prompt += f"""

Current User Question:

{user_input}
"""

    return prompt