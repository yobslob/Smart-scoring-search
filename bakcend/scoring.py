from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from kmScore import kmScore
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
                "region": startup.get('region', 'N/A'),
                "key_metrics" : startup.get('key_metrics', [])
            }
        )
        startup_docs.append(doc)

    vectorstore = FAISS.from_documents(
        documents=startup_docs,
        embedding=EMBEDDING_MODEL
    )

    results = vectorstore.similarity_search_with_score(
        query=investor_profile,
        k=len(startup_docs)
    )
    final_result = []
    for startup, scores in results:
        semantic_score = (1 - float(scores)) * 100
        keyMetrics = kmScore(startup.metadata["key_metrics"])
        keyScores = keyMetrics.score()
        score = round(0.7*semantic_score + 0.3*float(keyScores),2)
        result ={
            "startup_name": startup.metadata["startup_name"],
            "score": score,
            "industry": startup.metadata["industry"],
            "stage": startup.metadata["stage"],
            "region": startup.metadata["region"],
            "tagline": startup.metadata["tagline"],
            "website": startup.metadata["website"]
        }
        final_result.append((score, result))
        final_result.sort(key=lambda x: x[0], reverse=True)

    update = []
    for score, a in final_result:
        update.append(a)

    return update