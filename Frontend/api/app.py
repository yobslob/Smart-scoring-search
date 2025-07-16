from flask import Flask, request, jsonify
import os
import json
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document

app = Flask(__name__)
EMBEDDING_MODEL = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
K = 3

def load_startup_data():
    startup_data_list = []
    startups_path = os.path.join(os.getcwd(), 'data', 'Startups')
    for file_name in os.listdir(startups_path):
        if file_name.endswith(".json"):
            file_path = os.path.join(startups_path, file_name)
            with open(file_path, 'r') as file:
                startup_data = json.load(file)
                startup_data_list.append(startup_data)
    return startup_data_list

def get_investor_profile(investor_data):
    investor_profile = f"""
    Investor Profile:
    Designation: {investor_data.get('designation', 'N/A')}
    Bio: {investor_data.get('bio', 'N/A')}
    Stage Preference: {', '.join(investor_data.get('stage_preference', []))}
    Sector Focus: {', '.join(investor_data.get('sector_focus', []))}
    Regions Preferred: {', '.join(investor_data.get('regions_preferred', []))}
    """
    return investor_profile

def get_startup_profiles(startup_data_list):
    startup_profiles = []
    for startup_data in startup_data_list:
        startup_profile = f"""
        Startup Profile:
        Industry: {startup_data.get('industry', 'N/A')}
        Stage: {startup_data.get('startup_stage', 'N/A')}
        Tagline: {startup_data.get('tagline', 'N/A')}
        Description: {startup_data.get('description', 'N/A')}
        Problem: {startup_data.get('problem', 'N/A')}
        Solution: {startup_data.get('solution', 'N/A')}
        Mission: {startup_data.get('mission', 'N/A')}
        """
        doc = Document(
            page_content=startup_profile,
            metadata={
                "startup_name": startup_data.get('startup_name', 'Unknown'),
                "website": startup_data.get('website_url', 'Unknown'),
                "tagline": startup_data.get('tagline', 'Unknown'),
                "cac_inr": startup_data.get('key_metrics', {}).get('cac_inr', 'N/A'),
                "mrr_inr": startup_data.get('key_metrics', {}).get('mrr_inr', 'N/A'),
                "monthly_revenue": startup_data.get('key_metrics', {}).get('monthly_revenue_inr', 'Unknown'),
                "active_users": startup_data.get('key_metrics', {}).get('active_users', 'Unknown'),
                "funding_ask_inr": startup_data.get('funding_ask', {}).get('amount_inr', 'Unknown'),
                "equity_offered": startup_data.get('funding_ask', {}).get('equity_offered_percent', 'Unknown')
            }
        )
        startup_profiles.append(doc)
    vectorstore = Chroma.from_documents(
        documents=startup_profiles,
        embedding=EMBEDDING_MODEL,
    )
    return vectorstore

def search(investor_profile, vectorstore):
    results = vectorstore.similarity_search_with_score(
        query=investor_profile,
        k=K
    )
    final_result = []
    for (startup, score) in results:
        startup_data = startup.metadata.copy()
        startup_data['score'] = round((1 - score) * 100, 2)
        startup_data['profile'] = startup.page_content
        final_result.append(startup_data)
    return final_result

@app.route('/search', methods=['POST'])
def search_startups():
    investor_data = request.json
    startup_data_list = load_startup_data()
    investor_profile = get_investor_profile(investor_data)
    vectorstore = get_startup_profiles(startup_data_list)
    final_result = search(investor_profile, vectorstore)
    return jsonify(final_result)

if __name__ == '__main__':
    app.run()