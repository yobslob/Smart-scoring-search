from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import get_investor_profile, search_startups
from scoring import score_startups

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class SearchRequest(BaseModel):
    keyword: str
    stage_preferences: list[str]
    sector_focus: list[str]
    regions_preferred: list[str]

@app.post("/search")
def search(request: SearchRequest):
    # Construct investor profile dynamically, including only provided filters
    investor_profile = "Investor Profile:\n"
    if request.stage_preferences:
        investor_profile += f"Stage Preference: {', '.join(request.stage_preferences)}\n"
    if request.sector_focus:
        investor_profile += f"Sector Focus: {', '.join(request.sector_focus)}\n"
    if request.regions_preferred:
        investor_profile += f"Regions Preferred: {', '.join(request.regions_preferred)}\n"
    
    print(investor_profile)
    
    # Fetch startups using keyword and filters
    startups = search_startups(
        request.keyword,
        request.stage_preferences,
        request.sector_focus,
        request.regions_preferred
    )
    if not startups:
        return []
    
    # Score startups based on the dynamic investor profile
    sorted_startups = score_startups(investor_profile, startups)
    return sorted_startups