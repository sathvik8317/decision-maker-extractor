# 🧠 Decision Maker Extractor

The **Decision Maker Extractor** is a Streamlit-based tool that helps identify key decision-makers like CEOs, Founders, and CMOs from a list of companies. Using SerpAPI and Google search results, it extracts public LinkedIn profile data, guesses work emails, assigns confidence scores, and allows users to download enriched leads as a CSV. Ideal for sales teams, recruiters, and marketers looking to streamline B2B outreach.

---

## 🚀 Features

- 📄 Upload a CSV file with company names
- 🎯 Target specific job roles (e.g., CEO, Founder, CTO)
- 🔎 Automatically scrapes public Google search results via SerpAPI
- 🔗 Finds LinkedIn and Crunchbase profiles
- 📧 Guesses work email formats
- 📊 Confidence score ranking
- 📥 One-click CSV download of enriched leads

---

## 💡 Business Use Case

This tool is designed to enhance lead generation workflows by automating the discovery of decision-makers at potential client companies. It’s especially useful for outbound sales campaigns, recruiting efforts, and partnerships.

---

## 📂 Example Input

Upload a CSV file named `companies.csv`:

```csv
Company
Google
Microsoft
OpenAI
Infosys
Zoho Corporation
````

---

## 🧪 Example Output

| Name          | Role             | LinkedIn                     | Email                                                             | Confidence | Company   | Crunchbase                            |
| ------------- | ---------------- | ---------------------------- | ----------------------------------------------------------------- | ---------- | --------- | ------------------------------------- |
| Sundar Pichai | CEO at Google    | linkedin.com/in/sundarpichai | [sundar.pichai@google.com](mailto:sundar.pichai@google.com)       | 100        | Google    | crunchbase.com/organization/google    |
| Satya Nadella | CEO at Microsoft | linkedin.com/in/satyanadella | [satya.nadella@microsoft.com](mailto:satya.nadella@microsoft.com) | 100        | Microsoft | crunchbase.com/organization/microsoft |
| Sam Altman    | CEO at OpenAI    | linkedin.com/in/samaltman    | [sam.altman@openai.com](mailto:sam.altman@openai.com)             | 100        | OpenAI    | crunchbase.com/organization/openai    |

> 📌 Confidence is scored based on role match, email format, and snippet content.

---

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/decision-maker-extractor.git
cd decision-maker-extractor
```

### 2. Install Dependencies

```bash
pip install streamlit pandas requests
```

### 3. Add Your SerpAPI Key

Open `decision_maker_extractor.py` and replace:

```python
SERPAPI_KEY = "YOUR_SERPAPI_KEY_HERE"
```

with your actual API key from [SerpAPI](https://serpapi.com/).

### 4. Run the Streamlit App

```bash
streamlit run decision_maker_extractor.py
```

---

## 🛠️ How It Works

1. You upload a CSV of companies.
2. You enter job titles to target (e.g., CEO, Founder).
3. The app queries Google using SerpAPI and extracts:

   * LinkedIn titles and snippets
   * Estimated work emails
   * Crunchbase profile (if available)
4. It scores the lead based on:

   * Seniority in job title
   * Validity of guessed email
   * Richness of snippet
5. Results are shown and downloadable in one click.

---

## 📄 License

This project is licensed under the MIT License.
