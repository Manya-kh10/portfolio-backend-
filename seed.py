import sys
from api.database import get_db

# Configure output to support UTF-8/emojis on Windows console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def seed_database():
    print("🚀 Initiating Manya's Portfolio Database Seeding Pipeline...")
    db = get_db()
    
    # ==========================================
    # 1. Seed PROJECTS Collection
    # ==========================================
    print("\n📦 Seeding 'projects' collection...")
    db.projects.delete_many({})  # Clear existing to maintain idempotency
    
    projects_data = [
        {
            "title": "NEXUS — Multi-Agent Data Analysis Platform",
            "category": "AI Systems & Agents",
            "subtitle": "Built a full-stack AI platform orchestrating 3 specialized LLM agents via LangGraph.",
            "description": "Built a full-stack AI-powered data analysis platform orchestrating 3 specialized LLM agents (EDA, Statistical, Insight) via LangGraph on Groq's LLaMA 3.3, with a FastAPI backend, PostgreSQL, Redis caching, and Celery async task processing — enabling automated dataset cleaning, ML model training, and PDF report generation from a single CSV upload.",
            "tech_stack": ["LangGraph", "Groq", "FastAPI", "PostgreSQL", "Redis", "Celery", "LLaMA 3.3"],
            "status": "Completed",
            "github_link": "https://github.com/Manya-kh10/NEXUS-Multi-Agent-Analysis-Platform",
            "live_link": None,
            "preview_image": "/lux_editorial/nexus_logo.png"
        },
        {
            "title": "Personal RAG Chatbot – Document Q&A with Local LLM",
            "category": "LLMs & NLP",
            "subtitle": "Interactive document Q&A vector embeddings platform running fully offline.",
            "description": "Built an end-to-end RAG pipeline that ingests personal documents, generates vector embeddings via HuggingFace sentence-transformers, stores them in ChromaDB for semantic search, and serves responses through an interactive Streamlit UI with PDF upload, conversation memory, and source chunk visibility — powered by Llama 3.2 via Ollama for fully offline inference.",
            "tech_stack": ["HuggingFace", "ChromaDB", "Streamlit", "Ollama", "Llama 3.2", "RAG"],
            "status": "Completed",
            "github_link": "https://github.com/Manya-kh10/personal-rag-chatbot.git",
            "live_link": None,
            "preview_image": "/lux_editorial/rag_logo.png"
        },
        {
            "title": "ArthSakshar – AI-Powered Financial Literacy App",
            "category": "Mobile & AI Microservices",
            "subtitle": "Developed a financial literacy mobile app with Flutter and FastAPI microservices.",
            "description": "Developed a financial literacy mobile app with Flutter and Firebase, integrating multiple AI microservices built on FastAPI and Gemini API — including an AI chatbot, text-to-speech, a financial quiz generator, fraud alert system, and voice chatbot — as part of a team project under the EPICS program.",
            "tech_stack": ["Flutter", "Firebase", "FastAPI", "Gemini API"],
            "status": "Completed",
            "github_link": "https://github.com/Manya-kh10/ArthSakshar---Financial-Literacy-App",
            "live_link": None,
            "preview_image": "https://images.unsplash.com/photo-1559526324-4b87b5e36e44?q=80&w=600"
        },
        {
            "title": "n8n Automation Workflows – AI-Powered News & GitHub Digests",
            "category": "Workflow Automation",
            "subtitle": "Built Hacker News digests in Notion and GitHub Weekly activity email digests.",
            "description": "Built production-style automation workflows using n8n — including a daily Hacker News digest that fetches top stories, generates per-story AI summaries via Groq (Llama 3.3), and saves to Notion; and a GitHub Weekly Digest that summarizes commit activity and delivers a formatted email via Gmail.",
            "tech_stack": ["n8n", "Groq", "LLaMA 3.3", "Notion API", "Gmail API"],
            "status": "Completed",
            "github_link": "https://github.com/Manya-kh10/n8n-automations",
            "live_link": None,
            "preview_image": "/lux_editorial/n8n_logo.png"
        },
        {
            "title": "F1-Dashboard",
            "category": "Data Analytics",
            "subtitle": "Formula 1 analytics platform with sentiment analysis and race report summarization.",
            "description": "Built an interactive Formula 1 analytics dashboard using statistical techniques to analyze race data, driver commentary, and historical stats. Integrated sentiment analysis and text summarization pipelines to surface key insights from race reports, enabling data-driven exploration of F1 seasons through a visual Streamlit interface.",
            "tech_stack": ["Python", "Streamlit", "Pandas", "Matplotlib"],
            "status": "Completed",
            "github_link": "https://github.com/Manya-kh10/f1-driver-profiler.git",
            "live_link": None,
            "preview_image": "/lux_editorial/f1_logo.png"
        }
    ]
    
    result = db.projects.insert_many(projects_data)
    print(f"✅ Success! Injected {len(result.inserted_ids)} projects.")

    # ==========================================
    # 2. Seed SKILLS Collection
    # ==========================================
    print("\n🔧 Seeding 'skills' collection...")
    db.skills.delete_many({})
    
    skills_data = [
        {"name": "Python", "proficiency": "Expert", "category": "Programming"},
        {"name": "C++", "proficiency": "Expert", "category": "Programming"},
        {"name": "Java", "proficiency": "Advanced", "category": "Programming"},
        {"name": "Pandas", "proficiency": "Expert", "category": "Programming"},
        {"name": "Streamlit", "proficiency": "Expert", "category": "Programming"},
        {"name": "NLTK", "proficiency": "Advanced", "category": "Programming"},
        
        # AI/ML Tools
        {"name": "HuggingFace", "proficiency": "Advanced", "category": "AI/ML Tools"},
        {"name": "ChromaDB", "proficiency": "Advanced", "category": "AI/ML Tools"},
        {"name": "Ollama", "proficiency": "Expert", "category": "AI/ML Tools"},
        {"name": "LangChain", "proficiency": "Expert", "category": "AI/ML Tools"},
        {"name": "FastAPI", "proficiency": "Expert", "category": "AI/ML Tools"},
        {"name": "Groq", "proficiency": "Expert", "category": "AI/ML Tools"},
        {"name": "n8n", "proficiency": "Advanced", "category": "AI/ML Tools"},
        
        # GenAI & Agents
        {"name": "RAG Pipelines", "proficiency": "Expert", "category": "GenAI & Agents"},
        {"name": "LLM Integration", "proficiency": "Expert", "category": "GenAI & Agents"},
        {"name": "Prompt Engineering", "proficiency": "Expert", "category": "GenAI & Agents"},
        {"name": "Workflow Automation", "proficiency": "Expert", "category": "GenAI & Agents"},
        
        # Data Tools
        {"name": "Jupyter Notebook", "proficiency": "Expert", "category": "Data Tools"},
        {"name": "Git/GitHub", "proficiency": "Expert", "category": "Data Tools"},
        {"name": "SQL", "proficiency": "Advanced", "category": "Data Tools"},
        
        # Soft Skills
        {"name": "Problem-solving", "proficiency": "Expert", "category": "Soft Skills"},
        {"name": "Communication", "proficiency": "Expert", "category": "Soft Skills"},
        {"name": "Teamwork", "proficiency": "Expert", "category": "Soft Skills"}
    ]
    
    result = db.skills.insert_many(skills_data)
    print(f"✅ Success! Injected {len(result.inserted_ids)} skills.")

    # ==========================================
    # 3. Seed EXPERIENCE Collection
    # ==========================================
    print("\n💼 Seeding 'experience' collection...")
    db.experience.delete_many({})
    
    experience_data = [
        {
            "role": "AI Software Engineer Intern",
            "company": "Nexus Technologies",
            "start_date": "June 2025",
            "end_date": "Present",
            "description": [
                "Engineered scalable data aggregation pipelines integrating FastAPI gateway endpoints with MongoDB.",
                "Built and customized conversational intelligence bots utilizing LangGraph multi-agent orchestration architectures.",
                "Spearheaded database index optimization initiatives, reducing collection lookup latencies by 35%."
            ],
            "tech_stack": ["Python", "FastAPI", "MongoDB", "LangChain", "Gemini API"],
            "related_project_id": None
        },
        {
            "role": "Full Stack Developer Consultant",
            "company": "Sartorial Labs",
            "start_date": "September 2024",
            "end_date": "May 2025",
            "description": [
                "Architected and deployed responsive responsive web applications with automated data syncs.",
                "Configured serverless hosting strategies on Vercel, reducing deployment times and hosting overheads.",
                "Introduced Pydantic validation structures across backend models, reducing runtime data parsing errors by 50%."
            ],
            "tech_stack": ["React", "Node.js", "Python", "Vercel", "PostgreSQL"],
            "related_project_id": None
        }
    ]
    
    result = db.experience.insert_many(experience_data)
    print(f"✅ Success! Injected {len(result.inserted_ids)} experience entries.")

    # ==========================================
    # 4. Seed CERTIFICATIONS Collection
    # ==========================================
    print("\n📜 Seeding 'certifications' collection...")
    db.certifications.delete_many({})
    
    certs_data = [
        {
            "name": "Oracle Generative AI Professional Certificate",
            "issuer": "Oracle",
            "date_earned": "2025",
            "tags": ["Generative AI", "LLMs", "Oracle Cloud"],
            "certificate_link": "https://ibb.co/RpzJcrcn"
        },
        {
            "name": "Cloud Computing",
            "issuer": "NPTEL",
            "date_earned": "2025",
            "tags": ["Cloud Architecture", "Distributed Systems"],
            "certificate_link": "https://ibb.co/chqd4QG2"
        },
        {
            "name": "Introduction to Internet of Things",
            "issuer": "NPTEL",
            "date_earned": "2026",
            "tags": ["IoT", "Sensors", "Embedded Systems"],
            "certificate_link": "https://kommodo.ai/i/9gN9Uq7FGMu2sKMIGKKV"
        },
        {
            "name": "Japanese Language Proficiency – N5",
            "issuer": "JLPT",
            "date_earned": "2025",
            "tags": ["Japanese", "JLPT N5"],
            "certificate_link": "https://ibb.co/6JwW6yzP"
        },
        {
            "name": "Applied Machine Learning in Python",
            "issuer": "Coursera (University of Michigan)",
            "date_earned": "2025",
            "tags": ["Machine Learning", "Python", "Supervised Learning"],
            "certificate_link": "https://coursera.org/share/df5b56f23b0f4f4871667cbf940c9165"
        }
    ]
    
    result = db.certifications.insert_many(certs_data)
    print(f"✅ Success! Injected {len(result.inserted_ids)} certifications.")

    # ==========================================
    # 5. Seed ACHIEVEMENTS Collection
    # ==========================================
    print("\n🏆 Seeding 'achievements' collection...")
    db.achievements.delete_many({})
    
    achievements_data = [
        {
            "title": "Vice President, Anime Club",
            "organization": "VIT Bhopal University",
            "date": "2023 - 2026",
            "description": "Led the organizing team for Hyogen — the first-ever Comic Con event held at VIT Bhopal. Coordinated club activities, managed event logistics, and spearheaded the initiative that brought the college's debut Comic Con to life.",
            "category": "Leadership"
        }
    ]
    
    result = db.achievements.insert_many(achievements_data)
    print(f"✅ Success! Injected {len(result.inserted_ids)} achievements.")
    
    print("\n🏁 Database Seeding Pipeline Executed Successfully! MongoDB is fully ready.")

if __name__ == "__main__":
    seed_database()