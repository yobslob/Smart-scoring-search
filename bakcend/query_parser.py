from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain_google_genai import GoogleGenerativeAI
import langchain
import json
import re
from database import startups_collection

langchain.debug = True

# Initialize LLM with the correct model
model = GoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.1)

# Define prompt
prompt_template = PromptTemplate.from_template("""
Industries: Fintech, SaaS, HealthTech, EdTech, E‑commerce, AI, Blockchain.
Stages: Pre-seed, Seed, Growth, Series A, Series B(in order of increasing growth)

For the query: "{keyword}"
1. Pick the one listed industry mentioned, or "None".
2. List any stages (only from the above mentioned) → stage_preferences.
3. List any regions (e.g. USA, Europe, India) → regions_preferred.
4. Give a cleaned text_search (remove extra words like “startups”, “based in”, etc).
Respond *only* with this JSON (no markdown fences):

{{"primary_industry":"…","stage_preferences":[…],"regions_preferred":[…],"text_search":"…"}}
""")

# Create chain
chain = prompt_template | model

def manual_parse_query(keyword):
    industries = startups_collection.distinct("industry")
    stages = startups_collection.distinct("startup_stage")
    regions = startups_collection.distinct("region")
    
    industry_map = {i.lower(): i for i in industries}
    stage_map = {s.lower(): s for s in stages}
    region_map = {r.lower(): r for r in regions}
    
    terms = keyword.lower().split()
    
    extracted_sectors = [industry_map[term] for term in terms if term in industry_map]
    extracted_stages = [stage_map[term] for term in terms if term in stage_map]
    extracted_regions = [region_map[term] for term in terms if term in region_map]
    
    remaining_terms = [term for term in terms if term not in industry_map and term not in stage_map and term not in region_map]
    
    # Define stop words
    stop_words = set(["in", "at", "the", "and", "or", "a", "an", "startups", "based", "on", "for", "with", "of", "to", "by", "from", "about", "as", "into", "like", "through", "after", "over", "between", "out", "against", "during", "without", "before", "under", "around", "among"])
    remaining_terms = [term for term in remaining_terms if term not in stop_words]
    
    text_search = " ".join(remaining_terms)
    
    primary_industry = extracted_sectors[0] if extracted_sectors else 'None'
    stage_preferences = extracted_stages
    regions_preferred = extracted_regions
    
    return {
        "primary_industry": primary_industry,
        "stage_preferences": stage_preferences,
        "regions_preferred": regions_preferred,
        "text_search": text_search
    }

def parse_query(keyword):
    try:
        result = chain.invoke({"keyword": keyword})
        print(f"DEBUG: LLM raw response for '{keyword}': '{result}'")
        if result.startswith("```"):
            result = re.sub(r"^```[^\n]*\n|```$", "", result, flags=re.MULTILINE)
        parsed = json.loads(result)
        print(f"DEBUG: LLM parsed JSON for '{keyword}': {parsed}")
        return parsed
    except Exception as e:
        print(f"Error parsing query with LLM: {e}")
        return manual_parse_query(keyword)