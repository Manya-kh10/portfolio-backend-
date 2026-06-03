from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List

class AchievementSchema(BaseModel):
    title: str = Field(..., description="Title of the achievement or award")
    organization: str = Field(..., description="Issuing organization or institution")
    date: Optional[str] = Field(None, description="Date or time period when earned (e.g. 'Oct 2025')")
    description: Optional[str] = Field(None, description="Detailed context or impact of the achievement")
    category: str = Field(..., description="Category classification of the achievement")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "1st Place - GenAI Hackathon",
                "organization": "Google Cloud Developer Group",
                "date": "November 2025",
                "description": "Led a team of three to build a real-time agentic system that analyzes and visualizes complex telemetry feeds using Gemini Flash.",
                "category": "Hackathons"
            }
        }

class ExperienceSchema(BaseModel):
    role: str = Field(..., description="Professional role or job title")
    company: str = Field(..., description="Organization or company name")
    start_date: str = Field(..., description="Starting date of employment (e.g., 'Jan 2024')")
    end_date: Optional[str] = Field("Present", description="Ending date of employment or 'Present'")
    description: List[str] = Field(..., description="Bullet points of key accomplishments and duties")
    tech_stack: List[str] = Field(..., description="List of technologies utilized during the tenure")
    related_project_id: Optional[str] = Field(None, description="Optional DB ID linking to a project showcase item")

    class Config:
        json_schema_extra = {
            "example": {
                "role": "AI Engineer Intern",
                "company": "Nexus Technologies",
                "start_date": "June 2025",
                "end_date": "Present",
                "description": [
                    "Engineered real-time data pipelines integrating FastAPI endpoints with MongoDB collections.",
                    "Configured LangGraph-based chatbot agents executing multi-turn semantic reasoning.",
                    "Improved API latency by 35% through custom indexation on high-frequency collections."
                ],
                "tech_stack": ["Python", "FastAPI", "MongoDB", "LangChain", "Gemini API"],
                "related_project_id": "6a1570384a1fbbd0b9377eca"
            }
        }

class SkillSchema(BaseModel):
    name: str = Field(..., description="Name of the technical skill or tool")
    proficiency: str = Field(..., description="Level of expertise, e.g. 'Expert', 'Advanced', 'Intermediate'")
    category: str = Field(..., description="Category group, e.g. 'Languages', 'Frameworks', 'Databases', 'AI/ML'")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Python",
                "proficiency": "Advanced",
                "category": "Languages"
            }
        }

class CertificationSchema(BaseModel):
    name: str = Field(..., description="Name of the professional certification")
    issuer: str = Field(..., description="The body that issued the certification")
    date_earned: str = Field(..., description="Date when the certification was successfully earned")
    tags: List[str] = Field(default_factory=list, description="Associated skills or tech tags")
    certificate_link: Optional[str] = Field(None, description="Direct URL linking to the certificate")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Google Cloud Certified: Professional Cloud Developer",
                "issuer": "Google Cloud",
                "date_earned": "August 2025",
                "tags": ["GCP", "Cloud Architecture", "Kubernetes"],
                "certificate_link": "https://ibb.co/RpzJcrcn"
            }
        }

class ContactSchema(BaseModel):
    name: str = Field(..., description="Name of the visitor submitting the contact form")
    email: EmailStr = Field(..., description="Email address for replies")
    message: str = Field(..., description="The main message body or inquiry text")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Alex Mercer",
                "email": "alex.mercer@innovate.io",
                "message": "Hey Manya! I love your telemetry analyzer project. Are you open to freelance contract work on a similar GenAI application?"
            }
        }

class ProjectSchema(BaseModel):
    title: str = Field(..., description="Title of the project")
    category: str = Field(..., description="Classification category (e.g., 'AI Automations', 'Data Analysis', or 'LLM & NLP')")
    subtitle: str = Field(..., description="One-sentence hook displayed on front widgets")
    description: str = Field(..., description="Detailed markdown-supported deep-dive description")
    tech_stack: List[str] = Field(..., description="Array of tools, libraries, and frameworks utilized")
    status: str = Field(..., description="Current project status (e.g., 'Completed', 'In Progress')")
    github_link: Optional[str] = Field(None, description="URL to the GitHub source code repository")
    live_link: Optional[str] = Field(None, description="URL to the live deployment or interactive demo")
    preview_image: Optional[str] = Field(None, description="Direct URL for the showcase banner artwork")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "F1 Telemetry Analyzer",
                "category": "Data Analysis",
                "subtitle": "Real-time F1 race strategy and telemetry visualization.",
                "description": "An interactive data pipeline engineered to parse historical telemetry data, mapping out cornering speeds, tyre degradation arrays, and driver acceleration patterns across multiple GP seasons.",
                "tech_stack": ["Python", "Pandas", "FastF1", "Plotly"],
                "status": "Completed",
                "github_link": "https://github.com/Manya-kh10",
                "live_link": "https://f1-analysis-demo.com",
                "preview_image": "https://yourportfolio.com/assets/f1-banner.jpg"
            }
        }

class ChatRequest(BaseModel):
    message: str = Field(..., description="The text question or query to send to Manya's Digital Twin AI")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Hi, can you tell me about Manya's experience with FastAPI and LangChain?"
            }
        }

class ChatResponse(BaseModel):
    response: str = Field(..., description="The conversational response from the AI agent")

    class Config:
        json_schema_extra = {
            "example": {
                "response": "Manya is highly experienced with FastAPI and LangChain! She recently built a robust, serverless API gateway powering this very portfolio system, integrated with a LangGraph multi-turn conversational agent."
            }
        }
