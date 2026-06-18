import { useState, useEffect, useRef } from "react";
import "./Chat.css";

function Chat({
  mode = "global",
  skill = null,
  role = null
}) {

  const initialMessage =
    mode === "skill_gap"
      ? `I noticed that ${skill} is a missing skill for your target role: ${role}.

Would you like:
• Learning Roadmap
• Resources
• Projects
• Certifications
• Interview Preparation`
      : `Hi! I'm SkillMatch AI.

I can help with:

• Learning skills
• Career roadmaps
• Interview preparation
• Resume guidance
• Certifications

What would you like help with?`;

  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: initialMessage
    }
  ]);

  const [input, setInput] = useState("");

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth"
    });
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!input.trim()) return;

    const userMessage = {
      role: "user",
      content: input
    };

    const newMessages = [
    ...messages,
    userMessage
];

setMessages(newMessages);

    setInput("");

    setLoading(true);

    setError("");

    try {
      const response = await fetch(
    "http://localhost:5000/api/chat",
    {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
          messages: newMessages,
          mode,
          skill,
          role
        })
    }
);

const data = await response.json();

const aiReply = {
    role: "assistant",
    content: data.reply
};

setMessages(prev => [
    ...prev,
    aiReply
]);

setLoading(false);

    } catch (err) {

      setError("Failed to connect.");

      setLoading(false);
    }
  };

  const suggestions =
mode === "skill_gap"
? [
    `${skill} Roadmap`,
    `${skill} Projects`,
    `${skill} Certifications`,
    `${skill} Interview Questions`
]
: [
    "How do I learn React?",
    "Backend Developer roadmap",
    "Prepare me for Python interviews",
    "Give me Docker projects"
];

const startNewChat = () => {

    setMessages([
        {
            role: "assistant",
            content: initialMessage
        }
    ]);

    setInput("");

    setError("");

};

  return (
    <div className="chat-container">
      <div className="chat-card">
          <div className="chat-header">

            <div>
              <div className="branding">

                <div className="branding-icon">
                  🧠
                </div>

                <div>
                  <h1>SkillMatch AI</h1>

                  <p>
                    {mode === "skill_gap"
                      ? `Focused on ${skill}`
                      : "Career Mentor"}
                  </p>
                </div>

              </div>
            </div>

            <button className="new-chat-btn" onClick={startNewChat}>New Chat</button>

          </div>

          {mode === "skill_gap" && (

            <div className="skill-banner">

              <div className="skill-card">

                <span className="skill-label">
                  Missing Skill
                </span>

                <span className="skill-value">
                  {skill}
                </span>

              </div>

              <div className="skill-card">

                <span className="skill-label">
                  Target Role
                </span>

                <span className="skill-value">
                  {role}
                </span>

              </div>

            </div>

          )}

          {messages.length === 1 && (

            <div className="suggestions">

              {
                suggestions.map((item,index)=>(

                  <button
                    key={index}
                    type="button"
                    className="suggestion-chip"
                    onClick={() => setInput(item)}
                  >
                    {item}
                  </button>

                ))
              }

            </div>

          )}

          <div className="chat-messages">

            {messages.map((message, index) => (

              <div
                key={index}
                className={
                  message.role === "user"
                    ? "message user-message"
                    : "message assistant-message"
                }
              >
                {message.content}
              </div>

            ))}

            {loading && (
              <div className="message assistant-message">
                Typing...
              </div>
            )}

            <div ref={messagesEndRef} />

          </div>

          {error && (
            <div className="chat-error">
              {error}
            </div>
          )}

          <form
            className="chat-input-container"
            onSubmit={handleSubmit}
          >

            <textarea
              placeholder="Ask about careers, skills or interviews..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={loading}
              onKeyDown={(e)=>{
                if(
                  e.key === "Enter" &&
                  !e.shiftKey
                ){
                  e.preventDefault();
                  handleSubmit(e);
                }

              }}
            />

            <button
              type="submit"
              disabled={loading}
            >
              Send
            </button>

          </form>
      </div>
    </div>
  );
}

export default Chat;