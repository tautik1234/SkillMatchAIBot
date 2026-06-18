import os
from groq import Groq
from dotenv import load_dotenv
import time

load_dotenv()

client = Groq(
    # This is the default and can be omitted
    api_key=os.environ.get("GROQ_API_KEY"),
)

messages = [
    {
    "role":"system",
    "content":"""
You are SkillMatch AI.

You help students with:

- Career guidance
- Learning roadmaps
- Skill development
- Certifications
- Interview preparation
- Resume guidance

IMPORTANT RULES:

1. Only answer questions related to:
   - careers
   - skills
   - learning
   - interviews
   - resumes
   - certifications
   - jobs

2. If a query is unrelated, DO NOT answer it.

3. Instead respond exactly:

"Sorry, I can only assist with career development, learning, skills, certifications, resumes, interviews, and job-related topics."

4. Never provide partial answers to unrelated questions.

5. Never explain unrelated topics before refusing.

6. When teaching, explain concepts step-by-step and interactively.
"""
    }
]

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    messages.append(
    {
        "role":"user",
        "content":user_input
    }
    )

    response = client.chat.completions.create(
    messages=messages,
    model="llama-3.3-70b-versatile",
    stream=True
    )
    
    assistant_reply = ""

    print("AI: ", end="", flush=True)

    for chunk in response:
        content = chunk.choices[0].delta.content

        if content:
            print(content, end="", flush=True)
            assistant_reply += content
            time.sleep(0.05)

    print()

    messages.append(
    {
        "role":"assistant",
        "content":assistant_reply
    }
    )