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

st.title("Smart Startup Search Engine")

# Filters
st.sidebar.header("Investor Preferences")
sector = st.sidebar.selectbox("Sector Focus", ["FinTech", "HealthTech", "SaaS"])
stage = st.sidebar.multiselect("Preferred Stages", ["Idea", "MVP", "Seed", "Scaling", "Series A"], default=["Seed", "MVP"])
region = st.sidebar.multiselect("Geography", ["India", "SE Asia", "US", "Europe"], default=["India", "SE Asia"])
philosophy = st.sidebar.text_input("Investment Philosophy", "Invest in disruptive early-stage FinTech")
interests = st.sidebar.text_input("Interests (comma-separated)", "FinTech, Digital Inclusion")

st.sidebar.header("Search Filters")
keywords = st.sidebar.text_input("Keywords (comma-separated)", "")
min_mrr = st.sidebar.slider("Minimum MRR (₹)", 0, 150000, 0, step=5000)
min_growth_rate = st.sidebar.slider("Minimum Growth Rate (%)", 0, 50, 0, step=1)
max_burn_rate = st.sidebar.slider("Maximum Burn Rate (₹)", 0, 100000, 100000, step=5000)

if st.sidebar.button("Search"):
    # Build Investor Profile
    investor_profile = {
        "preferred_stages": stage,
        "sector_focus": [sector],
        "region_focus": region,
        "investment_philosophy": philosophy,
        "interests": [i.strip() for i in interests.split(",")]
    }

    # Filter Startups
    keyword_list = [kw.strip().lower() for kw in keywords.split(",")] if keywords else []
    filtered_startups = []
    for startup in startup_profiles:
        passes_filters = (
            startup["MRR"] >= min_mrr and
            startup["growth_rate"] * 100 >= min_growth_rate and
            startup["burn_rate"] <= max_burn_rate and
            startup["region"] in investor_profile["region_focus"] and
            startup["industry"] in investor_profile["sector_focus"]
        )
        if passes_filters:
            if keyword_list:
                search_text = " ".join([
                    startup["tagline"],
                    startup["description"],
                    startup["problem"],
                    startup["solution"],
                    startup["mission"]
                ]).lower()
                if all(kw in search_text for kw in keyword_list):  # All keywords must match
                    filtered_startups.append(startup)
            else:
                filtered_startups.append(startup)

    # Convert Startups to Documents for Semantic Search
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

    startup_docs = [startup_to_doc(p) for p in filtered_startups]
    if not startup_docs:
        st.write("No startups match your criteria.")
    else:
        vectorstore = FAISS.from_documents(startup_docs, embedding_model)

        # Investor Text for Semantic Search
        investor_text = "Represent: " + " | ".join([
            ", ".join(investor_profile["preferred_stages"]),
            ", ".join(investor_profile["sector_focus"]),
            ", ".join(investor_profile["region_focus"]),
            ", ".join(investor_profile["interests"]),
            investor_profile["investment_philosophy"]
        ])

        # Semantic Search
        semantic_matches = vectorstore.similarity_search_with_score(investor_text, k=len(filtered_startups))

        # Enhanced Smart Scoring Function
        def smart_score(startup, similarity_score):
            # Financial Metrics
            mrr_score = min(startup["MRR"] / 100000, 1.0)
            growth_score = min(startup["growth_rate"], 0.5)
            burn_score = 1.0 - min(startup["burn_rate"] / 100000, 1.0)
            engagement_score = startup["engagement"] / 100

            # Strategic Fit
            match_stage = 1 if startup["stage"] in investor_profile["preferred_stages"] else 0.5
            match_sector = 1 if startup["industry"] in investor_profile["sector_focus"] else 0.5
            match_region = 1 if startup["region"] in investor_profile["region_focus"] else 0.5
            strategic_fit_score = (match_stage + match_sector + match_region) / 3

            # MnA Factors (placeholders, to be refined with real algorithms)
            mna_score = (
                startup["team_experience_score"] * 0.4 +  # Weight for experienced team
                startup["market_potential_score"] * 0.3 +  # Weight for market appeal
                startup["tech_uniqueness_score"] * 0.3     # Weight for unique tech
            )

            # Weighted Total Score
            score = (
                0.25 * similarity_score +          # Semantic relevance
                0.15 * mrr_score +                 # Financial health
                0.15 * growth_score +              # Growth potential
                0.10 * burn_score +                # Financial efficiency
                0.10 * engagement_score +          # User traction
                0.15 * strategic_fit_score +       # Investor alignment
                0.10 * mna_score                   # Acquisition potential
            )
            return round(score * 100, 2)

        # Rank Startups
        ranked = []
        for doc, sim_score in semantic_matches:
            startup = doc.metadata["raw"]
            # Convert similarity score (lower is better in FAISS) to a 0-1 scale
            normalized_sim_score = 1 - min(sim_score, 1.0)
            score = smart_score(startup, normalized_sim_score)
            ranked.append((score, startup))
        ranked.sort(reverse=True)

        # Display Results
        st.subheader("Top Startup Matches")
        for score, startup in ranked:
            st.markdown("---")
            st.markdown(f"### {startup['tagline']}")
            st.markdown(f"**Sector:** {startup['industry']} | **Stage:** {startup['stage']} | **Region:** {startup['region']}")
            st.markdown(f"**Score:** `{score:.2f}/100`")
            st.markdown(f"**MRR:** ₹{startup['MRR']} | **Growth:** {int(startup['growth_rate']*100)}% | **Burn:** ₹{startup['burn_rate']}")
            st.markdown(f"**Engagement:** {startup['engagement']}% | **Team:** {startup['team_strength']}")
            st.markdown(f"**Mission:** *{startup['mission']}*")
            st.markdown(f"**Description:** {startup['description']}")
            # MnA Insights
            st.markdown(f"**MnA Potential:** Team: {startup['team_experience_score']}, Market: {startup['market_potential_score']}, Tech: {startup['tech_uniqueness_score']}")

else:
    st.write("Enter your preferences and filters, then click 'Search' to find matching startups.")