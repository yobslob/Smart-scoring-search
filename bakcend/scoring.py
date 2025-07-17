from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
import os
from dotenv import load_dotenv

load_dotenv()

EMBEDDING_MODEL = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

def score_startups(investor_profile, startups):
    startup_docs = []
    for startup in startups:
        startup_profile = f"""
        Startup Profile:
        Industry: {startup.get('industry', 'N/A')}
        Stage: {startup.get('startup_stage', 'N/A')}
        Region: {startup.get('region', 'N/A')}
        Tagline: {startup.get('tagline', 'N/A')}
        Description: {startup.get('description', 'N/A')}
        Problem: {startup.get('problem', 'N/A')}
        Solution: {startup.get('solution', 'N/A')}
        Mission: {startup.get('mission', 'N/A')}
        """
        doc = Document(
            page_content=startup_profile,
            metadata={
                "startup_name": startup.get('startup_name', 'Unknown'),
                "website": startup.get('website_url', 'Unknown'),
                "tagline": startup.get('tagline', 'Unknown'),
                "industry": startup.get('industry', 'N/A'),
                "stage": startup.get('startup_stage', 'N/A'),
                "region": startup.get('region', 'N/A')
            }
        )
        startup_docs.append(doc)

    vectorstore = Chroma.from_documents(
        documents=startup_docs,
        embedding=EMBEDDING_MODEL
    )

    results = vectorstore.similarity_search_with_score(
        query=investor_profile,
        k=len(startup_docs)
    )

    sorted_results = sorted(results, key=lambda x: x[1])

    final_result = []
    for startup, score in sorted_results:
        result = {
            "startup_name": startup.metadata["startup_name"],
            "score": round((1 - score) * 100, 2),
            "industry": startup.metadata["industry"],
            "stage": startup.metadata["stage"],
            "region": startup.metadata["region"],
            "tagline": startup.metadata["tagline"],
            "website": startup.metadata["website"]
        }
        final_result.append(result)

    return final_result