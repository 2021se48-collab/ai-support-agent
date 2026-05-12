import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

conversation_history = {}

def get_ai_response(message: str, session_id: str = "default") -> str:
    if session_id not in conversation_history:
        conversation_history[session_id] = [
            {
                "role": "system",
                "content": "You are a helpful AI customer support agent. You help customers with their questions professionally and friendly."
            }
        ]

    conversation_history[session_id].append({
        "role": "user",
        "content": message
    })

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=conversation_history[session_id],
        max_tokens=500,
        temperature=0.7
    )

    reply = response.choices[0].message.content

    conversation_history[session_id].append({
        "role": "assistant",
        "content": reply
    })

    return reply