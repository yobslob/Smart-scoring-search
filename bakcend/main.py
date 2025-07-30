from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import get_investor_profile, search_startups
from scoring import score_startups
from cache import get_parsed_query
import os

INVESTOR_ID = os.getenv("INVESTOR_ID")

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
    print(f"DEBUG: Received search request: keyword='{request.keyword}', stage_preferences={request.stage_preferences}, sector_focus={request.sector_focus}, regions_preferred={request.regions_preferred}")
    
    # Construct investor profile dynamically
    investor_profile = get_investor_profile(INVESTOR_ID) or "Investor Profile:\n"
    # 2) Append any runtime filters
    if request.stage_preferences:
        investor_profile += f"Stage Preference: {', '.join(request.stage_preferences)}\n"
    if request.sector_focus:
        investor_profile += f"Sector Focus: {', '.join(request.sector_focus)}\n"
    if request.regions_preferred:
        investor_profile += f"Regions Preferred: {', '.join(request.regions_preferred)}\n"
        
    print("Investor's profile:",investor_profile)
    
    print(f"DEBUG: Calling get_parsed_query for keyword: '{request.keyword}'")
    # Parse query
    parsed = get_parsed_query(request.keyword)
    print(f"DEBUG: Parsed query result from cache/LLM: {parsed}")
    
    # Determine industry_filter
    if request.sector_focus:
        industry_filter = request.sector_focus
    elif parsed['primary_industry'] != 'None':
        industry_filter = [parsed['primary_industry']]
    else:
        industry_filter = []
        
    stage_prefs = request.stage_preferences or parsed.get("stage_preferences", [])

    regions = request.regions_preferred or parsed.get("regions_preferred", [])
    
    text_query = parsed['text_search']
    print(f"DEBUG: Final filters → industry={industry_filter}, stages={stage_prefs}, regions={regions}, text_query={text_query!r}")
    
    print(f"DEBUG: Calling search_startups with industry_filter={industry_filter}, text_query='{text_query}', stage_preferences={stage_prefs}, regions_preferred={regions}")
    # Fetch startups
    startups = search_startups(
        industry_filter=industry_filter,
        text_query=text_query,
        stage_preferences=stage_prefs,
        regions_preferred=regions
    )
    print(f"DEBUG: Number of startups fetched: {len(startups) if startups else 0}")
    if not startups:
        return []
    
    # Score startups
    sorted_startups = score_startups(investor_profile, startups)
    return sorted_startups