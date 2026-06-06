from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.agent import job_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {
        "message": "Agentic Job Search Backend Running"
    }


@app.post("/chat")
def chat(request: ChatRequest):
    print("CHAT ENDPOINT HIT") 

    result = job_agent.invoke(
        {

            "user_query": request.message,
            "role": "",
            "location": "",
            "experience": "",
            "jobs": [],
            "response": ""   

        }
    )

    return {
        "reply": result["response"]
    }