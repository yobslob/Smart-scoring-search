import streamlit as st
import requests
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    encode_kwargs={"normalize_embeddings": True}
)

def startup_to_doc(profile):
    text = " | ".join([
        profile["industry"],
        profile["stage"],
        profile["tagline"],
        profile["description"],
        profile["problem"],
        profile["solution"],
        profile["mission"],
        profile["team_strength"]
    ])
    metadata = {"id": profile["id"], "raw": profile}
    return Document(page_content="Represent: " + text, metadata=metadata)

st.title("Search Engine")

st.sidebar.header("Investor Preferences")
sector = st.sidebar.selectbox("Sector Focus", ["FinTech", "HealthTech", "SaaS", "Other"])
stage = st.sidebar.multiselect("Preferred Stages", ["Idea", "MVP", "Seed", "Scaling", "Series A"], default=["Seed", "MVP"])
region = st.sidebar.multiselect("Geography", ["India", "SE Asia", "US", "Europe"], default=["India"])
keywords = st.sidebar.text_input("Search Keywords", placeholder="e.g., AI, blockchain, sustainability")

if st.sidebar.button("Search"):
    investor_profile = {
        "sector_focus": sector,
        "preferred_stages": stage,
        "region_focus": region,
        "keywords": keywords.strip().lower()
    }

    response = requests.get('http://localhost:5000/startups')
    all_startups = response.json()

    filtered_startups = [
        s for s in all_startups
        if s["region"] in investor_profile["region_focus"]
        and s["stage"] in investor_profile["preferred_stages"]
        and s["industry"] == investor_profile["sector_focus"]
    ]

    keyword_matches = []
    if investor_profile["keywords"]:
        kw_list = [k.strip() for k in investor_profile["keywords"].split(",")]
        for s in all_startups:
            text = " ".join([
                s["tagline"], s["description"], s["problem"],
                s["solution"], s["mission"]
            ]).lower()
            if all(k in text for k in kw_list):
                keyword_matches.append(s)

    all_considered = {s["id"]: s for s in filtered_startups}
    for s in keyword_matches:
        all_considered[s["id"]] = s

    combined_startups = list(all_considered.values())

    if not combined_startups:
        st.write("No startups matched your filters or keywords.")
    else:
        parts = [investor_profile["sector_focus"]]
        if investor_profile["preferred_stages"]:
            parts.append(", ".join(investor_profile["preferred_stages"]))
        if investor_profile["keywords"]:
            parts.append(investor_profile["keywords"])
        investor_text = "Represent: " + " | ".join(parts)

        startup_docs = [startup_to_doc(p) for p in combined_startups]
        vectorstore = FAISS.from_documents(startup_docs, embedding_model)

        semantic_matches = vectorstore.similarity_search(investor_text, k=len(combined_startups))

        st.subheader("Top Startup Matches")
        for doc in semantic_matches:
            startup = doc.metadata["raw"]
            st.markdown("---")
            st.markdown(f"### {startup['tagline']}")
            st.markdown(f"**Sector:** {startup['industry']} | **Stage:** {startup['stage']} | **Region:** {startup['region']}")
            st.markdown(f"**Description:** {startup['description']}")
            st.markdown(f"**Mission:** *{startup['mission']}*")
            st.markdown(f"**Team:** {startup['team_strength']}")
else:
    st.write("Enter your preferences and keywords, then click 'Search' to find matching startups.")
