import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Analyze this data issue: Column 'age' has 20% missing values. Is this a quality risk?",
        }
    ],
    model="llama-3.1-70b-versatile",
)

print("Groq Response:")
print(chat_completion.choices[0].message.content)