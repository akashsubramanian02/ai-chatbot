from memory.memory_manager import save_chat
from memory.memory_manager import get_recent_history

save_chat(
    1,
    "What is AI?",
    "AI means Artificial Intelligence",
    "Neutral"
)

history = get_recent_history(1)

print(history)