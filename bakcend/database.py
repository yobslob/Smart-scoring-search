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

def search_startups(keyword):
    query = {"$text": {"$search": keyword}}
    startups = list(startups_collection.find(query))
    return startups