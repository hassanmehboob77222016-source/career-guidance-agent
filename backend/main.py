from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import StudentProfile, GuidanceResponse
from agent import run_agent

app = FastAPI(title="Career Guidance Agent API")

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/guidance", response_model=GuidanceResponse)
async def get_guidance(profile: StudentProfile):
    try:
        result = run_agent(profile)
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        return GuidanceResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
