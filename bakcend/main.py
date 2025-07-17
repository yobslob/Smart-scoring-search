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
    # Construct investor profile dynamically from user-selected filters
    stage_prefs = ', '.join(request.stage_preferences) if request.stage_preferences else "Not specified"
    sector_foci = ', '.join(request.sector_focus) if request.sector_focus else "Not specified"
    regions_prefs = ', '.join(request.regions_preferred) if request.regions_preferred else "Not specified"
    
    investor_profile = f"""
    Investor Profile:
    Stage Preference: {stage_prefs}
    Sector Focus: {sector_foci}
    Regions Preferred: {regions_prefs}
    """
    print(investor_profile)
    
    # Fetch startups from MongoDB using the keyword only
    startups = search_startups(request.keyword)
    if not startups:
        return []
    
    # Score startups based on the dynamic investor profile
    sorted_startups = score_startups(investor_profile, startups)
    return sorted_startups