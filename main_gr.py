import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from models.startup_profiles import startup_profiles
import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Load Embedding Model
embedding_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    encode_kwargs={"normalize_embeddings": True}
)

# Function to Convert Startup Profile to Document
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

# Streamlit UI
st.title("Search Engine")

# Sidebar for Investor Preferences
st.sidebar.header("Investor Preferences")
sector = st.sidebar.selectbox("Sector Focus", ["FinTech", "HealthTech", "SaaS", "Other"])
stage = st.sidebar.multiselect("Preferred Stages", ["Idea", "MVP", "Seed", "Scaling", "Series A"], default=["Seed", "MVP"])
region = st.sidebar.multiselect("Geography", ["India", "SE Asia", "US", "Europe"], default=["India"])
keywords = st.sidebar.text_input("Search Keywords", placeholder="e.g., AI, blockchain, sustainability")

if st.sidebar.button("Search"):
    # Build Investor Profile
    investor_profile = {
        "sector_focus": sector,
        "preferred_stages": stage,
        "region_focus": region,
        "keywords": keywords
    }

    # Filter Startups by Geography
    selected_regions = investor_profile["region_focus"]
    if selected_regions:
        filtered_startups = [s for s in startup_profiles if s["region"] in selected_regions]
    else:
        filtered_startups = startup_profiles  # Include all if no regions selected

    if not filtered_startups:
        st.write("No startups found in the selected geography.")
    else:
        # Build Query for Semantic Search
        parts = [investor_profile["sector_focus"]]
        if investor_profile["preferred_stages"]:
            parts.append(", ".join(investor_profile["preferred_stages"]))
        if investor_profile["keywords"]:
            parts.append(investor_profile["keywords"])
        investor_text = "Represent: " + " | ".join(parts)

        # Create FAISS Vector Store
        startup_docs = [startup_to_doc(p) for p in filtered_startups]
        vectorstore = FAISS.from_documents(startup_docs, embedding_model)

        # Perform Semantic Search
        semantic_matches = vectorstore.similarity_search(investor_text, k=5)

        # Display Results
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