import os

from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS

from groq import Groq

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

CORS(app)

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

SYSTEM_PROMPT = """
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

7. Allow generic greetings from user, but do not indulge in greetings. Quickly steer the conversation towards career guidance, learning, skills, certifications, resumes, interviews, and job-related topics. 

8. If the user asks for a roadmap, provide a detailed roadmap with steps, resources, and projects to learn the skill. Include certifications if applicable.

9. If the user asks for interview preparation, provide a detailed guide with steps, resources, and practice questions. Include tips for resume building and job search if applicable.

10. If the user enters any typos or misspellings, try to understand the intended meaning and respond accordingly. If you are unsure, ask for clarification.

11. Always maintain a professional and helpful tone. Be concise but informative in your responses.

12. If user asks irrelevant questions, do not answer them. Instead, respond with the refusal message mentioned in rule 3.
"""

GREETINGS = {
    "hi",
    "hello",
    "hey",
    "good morning",
    "good afternoon",
    "good evening",
    "thanks",
    "thank you",
    "bye"
}

ALLOWED_KEYWORDS = [

    "career",
    "job",
    "skill",
    "skills",
    "learn",
    "learning",
    "roadmap",
    "developer",
    "programming",
    "python",
    "java",
    "react",
    "node",
    "docker",
    "backend",
    "frontend",
    "interview",
    "resume",
    "cv",
    "certification",
    "course",
    "internship",
    "placement",
    "dsa",
    "database",
    "sql",
    "mongodb",
    "aws",
    "cloud"
]

def is_allowed_query(message):

    msg = message.lower()

    for keyword in ALLOWED_KEYWORDS:

        if keyword in msg:
            return True

    return False

def handle_greeting(message):

    msg = message.lower().strip()

    if msg in GREETINGS:

        return {
            "reply":
            """Hi! I'm SkillMatch AI.

            I can help with:

            • Career Guidance
            • Learning Roadmaps
            • Skill Development
            • Certifications
            • Interview Preparation

            What would you like help with today?"""
        }

    return None



@app.route("/chat", methods=["POST"])
def chat():

    data = request.json
    mode = data.get("mode")
    skill = data.get("skill")
    role = data.get("role")
    messages = data["messages"]
    latest_message = messages[-1]["content"]
    greeting_response = handle_greeting(latest_message)
    # if greeting_response:
    #     return jsonify(greeting_response)
    # if not is_allowed_query(latest_message):
    #     return jsonify({
    #         "reply":
    #         "Sorry, I can only assist with career development, learning, skills, certifications, resumes, interviews, and job-related topics."
    #     })
    dynamic_system_prompt = SYSTEM_PROMPT
    if mode == "skill_gap":

        dynamic_system_prompt += f"""

        The user was launched from
        Skill Gap Analysis.

        Missing Skill:
        {skill}

        Target Role:
        {role}

        Prioritize helping the user
        learn this skill.

        Guide them with:

        - Roadmaps
        - Resources
        - Projects
        - Certifications
        - Interview Prep
        """



    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role":"system",
                "content":dynamic_system_prompt
            },
            *messages
        ]
    )

    return jsonify({
        "reply":
        response.choices[0].message.content
    })

if __name__ == "__main__":
    app.run(
        port=5001,
        debug=True
    )