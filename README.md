# 🔎 RA's FactCheckAI

**AI-Powered Fact Checking Application**

RA's FactCheckAI is an AI-powered web application that verifies factual claims using real-time web search and Large Language Models (LLMs).

Users can submit one or multiple statements. The application extracts individual factual claims, searches the web for supporting information, and uses AI to analyze the available evidence and generate structured fact-checking results.

🌐 **Live Demo:** https://rasfactcheckai.streamlit.app/

## ✨ Features

- **Multiple Claim Detection:** Extracts individual factual claims from a single input.
- **AI-Powered Claim Extraction:** Uses Groq LLMs to identify and separate factual statements.
- **Web Search Integration:** Retrieves relevant search results using the Serper API.
- **AI Fact Checking:** Analyzes search evidence and generates independent verdicts for each claim.
- **Structured AI Responses:** Uses Pydantic to validate fact-checking results.
- **Evidence Analysis:** Displays supporting evidence, contradicting evidence, and limitations.
- **Confidence Score:** Provides an AI-estimated confidence score.
- **Source References:** Displays search sources and links.
- **Fact-Check History:** Stores previous fact-checks in an SQLite database.

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| LLM Integration | LangChain |
| AI Model Provider | Groq |
| Web Search | Serper API |
| Data Validation | Pydantic |
| Database | SQLite |
| Environment Management | Python Virtual Environment |
| Version Control | Git & GitHub |
| Deployment | Streamlit Community Cloud |

## 🏗️ Project Structure

```text
RA's Fact Check/
│
├── app.py
├── config.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── README.md
│
├── services/
│   ├── __init__.py
│   ├── claim_service.py
│   ├── search_service.py
│   └── factcheck_service.py
│
├── schemas/
│   ├── __init__.py
│   ├── claim_schema.py
│   └── factcheck_schema.py
│
├── database/
│   ├── __init__.py
│   └── db.py
│
└── test_factcheck.py
```

## ⚙️ How It Works

1. User submits one or more factual statements.
2. The claim extraction service identifies individual claims.
3. Each claim is independently submitted to the Serper search API.
4. Search results are passed to the Groq LLM through LangChain.
5. The AI analyzes the evidence and generates a structured response.
6. Pydantic validates the response.
7. The application displays the verdict, confidence, explanation, evidence, and sources.
8. Each successful fact-check is stored in the SQLite database.

## ⚖️ Supported Verdicts

- **True** – Available evidence supports the claim.
- **False** – Available evidence contradicts the claim.
- **Partially True** – Only part of the claim is supported.
- **Misleading** – The claim presents information in a misleading way.
- **Insufficient Evidence** – Available information is not adequate to reach a conclusion.

## 🚀 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/ravitejagorla/RAs_FactCheckAI.git
cd RAs_FactCheckAI
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Linux / macOS**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b
SERPER_API_KEY=your_serper_api_key
```

Obtain API credentials from:

- Groq: https://console.groq.com/
- Serper: https://serper.dev/

Never commit your `.env` file or expose API credentials publicly.

### 5. Run the application

```bash
streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

## ☁️ Deployment

The application is deployed using **Streamlit Community Cloud**.

Live Application: https://rasfactcheckai.streamlit.app/

GitHub Repository: https://github.com/ravitejagorla/RAs_FactCheckAI

## 🔐 Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | API key for Groq LLM access |
| `GROQ_MODEL` | Groq model identifier |
| `SERPER_API_KEY` | API key for web search |

For cloud deployment, configure these values through Streamlit Community Cloud secrets.

## ⚠️ Limitations

- Verdicts and confidence scores are AI-generated and may contain errors.
- Search result quality and availability affect fact-checking accuracy.
- Search snippets alone may not provide sufficient context.
- AI confidence scores are estimates, not statistically calibrated probabilities.
- SQLite storage on cloud hosting may not persist across application restarts or redeployments.

Always consult original sources for important decisions.

## 🔮 Future Improvements

- Source credibility and reliability analysis.
- Better evidence ranking and source prioritization.
- Improved contradiction detection.
- Persistent PostgreSQL database integration.
- User authentication and personalized history.
- Export fact-check reports.
- Improved user interface and visualizations.

## 👨‍💻 Author

**Ravi Teja Gorla**

Software Developer | Python | Django | Angular | AI & Generative AI

- GitHub: https://github.com/ravitejagorla
- LinkedIn: https://www.linkedin.com/in/ravitejagorla/

---

⭐ If you find this project interesting, consider starring the repository!

**Built with Python, AI, and curiosity.**