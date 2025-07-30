from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["Data"]

investors_collection = db["Investors"]
startups_collection = db["Startups"]
stage_statistics_collection = db["StageStatistics"]

def get_investor_profile(investor_id):
    investor = investors_collection.find_one({"_id": ObjectId(investor_id)})
    if investor:
        profile = f"""
        Investor Profile:
        Designation: {investor.get('designation', 'N/A')}
        Bio: {investor.get('bio', 'N/A')}
        Stage Preference: {', '.join(investor.get('stage_preference', []))}
        Sector Focus: {', '.join(investor.get('sector_focus', []))}
        Regions Preferred: {', '.join(investor.get('regions_preferred', []))}
        """
        return profile
    return None

def search_startups(industry_filter=None, text_query=None, stage_preferences=None, regions_preferred=None):
    query = {}
    if industry_filter:
        query["industry"] = {"$in": industry_filter}
    if stage_preferences:
        query["startup_stage"] = {"$in": stage_preferences}
    if regions_preferred:
        query["region"] = {"$in": regions_preferred}
    if text_query and text_query.strip():  # Only apply text_query if non-empty after stripping
        query["$text"] = {"$search": text_query}
    
    startups = list(startups_collection.find(query))
    return startups