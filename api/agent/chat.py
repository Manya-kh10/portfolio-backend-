import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from api.database import get_db

load_dotenv(override=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = None
agent_executor = None

if GROQ_API_KEY:
    llm = ChatOpenAI(
        model="llama-3.3-70b-versatile",
        api_key=GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1",
        temperature=0.5,
        max_retries=1
    )


@tool
def get_portfolio_data(endpoint: str):
    """
    Fetches real-time portfolio data about Manya's background.
    Input must be exactly one of: 'projects', 'skills', 'experience', 'certifications', or 'achievements'.
    """
    allowed_endpoints = {"projects", "skills", "experience", "certifications", "achievements"}
    endpoint = endpoint.strip().lower()
    
    if endpoint not in allowed_endpoints:
        return f"Error: '{endpoint}' is not a valid portfolio category. Choose from {allowed_endpoints}."

    try:
        db = get_db()
        collection = db[endpoint]
        data = list(collection.find({}, {'_id': 0}))
        
        if not data or len(data) == 0:
            return "Manya is currently updating that specific section of her portfolio."
            
        return data
    except Exception:
        return "Manya is currently updating that specific section of her portfolio."

tools = [get_portfolio_data]

SYSTEM_PROMPT = """You are Manya Khandelwal's portfolio chatbot. You represent her professionally to visitors on her portfolio website.

WHO YOU ARE:
Manya is an engineering student working majorly in the domain of AI/ML. She builds AI systems — RAG pipelines, multi-agent platforms, automation workflows. She's skilled in Python, LangChain, and n8n.

STRICT RULES:
1. SHORT ANSWERS ONLY. Maximum 2-3 lines. Never write essays or long paragraphs. Be extremely concise.
2. Always fetch from your tool before answering questions about projects, skills, certifications, or achievements. Never guess or hallucinate.
3. If someone asks what Manya has built, list project names with one-line descriptions and tell them to check the Projects section for details.
4. Redirect naturally — if someone wants to know more, point them: "You can explore the Projects section", "Check out her Skills section", etc.
5. Be friendly and human. No corporate buzzwords. Just clear, warm, direct replies.
6. If a section is empty, say: "Manya's updating that section — check back soon!"
7. Never mention tools, databases, APIs, JSON, or any technical internals.
8. For contact/hiring, say: "You can reach out to Manya directly via email by clicking the button below." and provide the Email button link.
9. For Resume, LinkedIn, GitHub, or Email: DO NOT provide raw text links. Instead, use markdown link syntax [Button Text](URL) so the frontend can render them as buttons. Use the following URLs:
   - Resume: [Access Resume](https://github.com/Manya-kh10/Manya-resume/blob/main/Manya_Khandelwal_resume%20%282%29.pdf)
   - GitHub: [GitHub Profile](https://github.com/Manya-kh10)
   - LinkedIn: [LinkedIn Profile](https://www.linkedin.com/in/manya-khandelwal-b821492a3)
   - Email: [Send Email](mailto:khandelwalmanya8@gmail.com)
   Always introduce the button with a professional sentence, e.g., "Please click on the button below to access Manya's resume." or "You can explore her projects on GitHub via the button below."
10. If asked about AI projects or AI skills, suggest ONLY the properly AI-centered projects: "NEXUS — Multi-Agent Data Analysis Platform" and "Personal RAG Chatbot". Do not suggest other projects.
11. If asked about professional experience, always reply with: "Manya has no industry experience yet, but she is currently gaining practical experience by building real world projects." Do not list any other experience.

RESPONSE FORMAT:
- Greetings: 1 line max
- Project/skill questions: bullet points, 2 max, then redirect
- General questions: 1-2 lines max
"""

if llm:
    agent_executor = create_react_agent(llm, tools, prompt=SYSTEM_PROMPT)
else:
    agent_executor = None


def ask_agent(question: str) -> str:
    """
    Sends a query to the Digital Twin agent and returns its response.
    """
    if not agent_executor:
        return "Manya's AI Twin is currently offline as the GROQ_API_KEY is not configured. Please check back later!"
    try:
        response = agent_executor.invoke({"messages": [("user", question)]})
        if "messages" in response and len(response["messages"]) > 0:
            content = response["messages"][-1].content
            
            if isinstance(content, list):
                text_blocks = []
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        text_blocks.append(block.get("text", ""))
                    elif isinstance(block, str):
                        text_blocks.append(block)
                return "".join(text_blocks)
                
            return str(content)
            
        return "Sorry, I didn't catch that — could you ask again?"
    except Exception as e:
        err_msg = str(e).lower()
        if "429" in err_msg or "rate_limit" in err_msg or "rate limit" in err_msg or "limit_exceeded" in err_msg:
            return "Manya's AI Twin is currently receiving a lot of messages. Please try again in a few seconds!"
        return "I'm having a small hiccup. Please try again in a moment!"