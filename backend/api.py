from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess

app = FastAPI(title="GovEngine AI API")

# Allow your Vercel frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Change this to your Vercel URL later for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AuditResponse(BaseModel):
    message: str
    status: str

def run_ai_engine():
    """Runs your existing main.py script in the background"""
    subprocess.run(["python", "main.py"])

@app.get("/")
@app.head("/")
def health_check():
    return {"status": "GovEngine AI is Online and Ready."}

@app.post("/api/trigger-audit", response_model=AuditResponse)
def trigger_audit(background_tasks: BackgroundTasks):
    """
    This is the endpoint your Next.js 'Trigger' button will hit.
    It starts the CrewAI agents in the background so the web request doesn't timeout!
    """
    background_tasks.add_task(run_ai_engine)
    return {
        "message": "AI Governance Engine successfully triggered. Agents are now auditing.",
        "status": "processing"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)