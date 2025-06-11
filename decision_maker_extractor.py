# decision_maker_extractor.py

import streamlit as st
import pandas as pd
import requests
from urllib.parse import quote
import re

# --- Config ---
SERPAPI_KEY = "# Replace with your actual SerpAPI key"
HEADERS = {"User-Agent": "Mozilla/5.0"}

# --- Utility Functions ---
def serpapi_search(query):
    url = f"https://serpapi.com/search.json?q={quote(query)}&engine=google&api_key={SERPAPI_KEY}"
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else {}
    except:
        return {}

def crunchbase_search(company):
    query = quote(company + " site:crunchbase.com")
    url = f"https://serpapi.com/search.json?q={query}&engine=google&api_key={SERPAPI_KEY}"
    try:
        r = requests.get(url)
        for res in r.json().get("organic_results", []):
            if "crunchbase.com/organization/" in res.get("link", ""):
                return res.get("link")
        return ""
    except:
        return ""

def extract_profiles(results, keywords, company):
    leads = []
    for result in results.get("organic_results", []):
        title = result.get("title", "")
        link = result.get("link", "")
        snippet = result.get("snippet", "")
        lower = title.lower() + " " + snippet.lower()
        if any(k.lower() in lower for k in keywords) and company.lower() in lower:
            name = title.split("-")[0].strip()
            email = guess_email(name, link)
            confidence = compute_confidence_score(title, snippet, email)
            leads.append({
                "Name": name,
                "Role": title,
                "LinkedIn": link,
                "Email": email,
                "Confidence": confidence
            })
    return leads

def guess_email(name, website_url):
    name_parts = re.findall(r"[a-zA-Z]+", name.lower())
    domain = website_url.replace("https://", "").replace("http://", "").split("/")[0]
    if len(name_parts) >= 2:
        formats = [
            f"{name_parts[0]}.{name_parts[1]}@{domain}",
            f"{name_parts[0][0]}{name_parts[1]}@{domain}",
            f"{name_parts[0]}@{domain}"
        ]
        return formats[0]  # default format
    return f"info@{domain}"

def compute_confidence_score(title, snippet, email):
    score = 0
    if any(keyword in title.lower() for keyword in ["ceo", "founder", "head", "chief", "director"]):
        score += 40
    if email and "@" in email:
        score += 30
    if len(snippet) > 30:
        score += 30
    return score

# --- Streamlit UI ---
st.title("🧠 Decision Maker Extractor - Advanced")
st.markdown("Upload a CSV with company names and optionally domains. We'll find decision-makers based on your target roles.")

uploaded = st.file_uploader("Upload CSV with 'Company' column", type=["csv"])
custom_roles = st.text_input("Enter target roles (comma-separated, e.g., CEO,Founder,CTO,Marketing)", "CEO,Founder")
target_keywords = [x.strip() for x in custom_roles.split(",") if x.strip()]

if uploaded and target_keywords:
    df = pd.read_csv(uploaded)
    all_leads = []

    for _, row in df.iterrows():
        company = row['Company']
        query = f"site:linkedin.com/in {company} {' '.join(target_keywords)}"
        serp_results = serpapi_search(query)
        leads = extract_profiles(serp_results, target_keywords, company)
        crunchbase_link = crunchbase_search(company)

        for lead in leads:
            lead['Company'] = company
            lead['Crunchbase'] = crunchbase_link
        all_leads.extend(leads)

    if all_leads:
        df_leads = pd.DataFrame(all_leads)
        df_leads = df_leads.sort_values(by="Confidence", ascending=False)
        st.dataframe(df_leads)
        st.download_button("📥 Download Leads", df_leads.to_csv(index=False).encode("utf-8"), "leads.csv", "text/csv")
    else:
        st.info("No leads found with the specified roles.")
