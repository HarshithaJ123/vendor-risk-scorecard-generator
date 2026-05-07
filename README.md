# AI Service for Vendor Risk Scorecard Generator

AI-powered vendor risk assessment system using Flask, Groq AI, and ChromaDB.

---

# Setup

1. Install dependencies

```bash
pip install -r requirements.txt
```

2. Configure environment variables

Create `.env` file:

```env
GROQ_API_KEY=your_api_key
```

3. Run application

```bash
python app.py
```

---

# Tech Stack

- Python
- Flask
- Groq API
- ChromaDB
- Docker
- Postman

---

# Run Instructions

### Local Run

```bash
python app.py
```

### Docker Run

```bash
docker build -t ai-service .
docker run -p 5000:5000 ai-service
```

---

# API Reference

## POST /ai/describe

### Input

```json
{
  "vendor": "Infosys",
  "risk_score": "High"
}
```

### Output

```json
{
  "risk_level": "Medium",
  "reasons": [
    "AI service temporarily unavailable"
  ]
}
```

---

## POST /ai/recommend

### Input

```json
{
  "vendor": "Infosys",
  "risk_score": "High"
}
```

### Output

```json
{
  "recommendations": [
    {
      "action_type": "Security",
      "description": "Retry AI request later",
      "priority": "Medium"
    }
  ]
}
```

---

## POST /ai/analyze

### Output

```json
{
  "risk_level": "Medium",
  "reasons": [],
  "recommendations": []
}
```

---

## POST /ai/generate-report

### Output

```json
{
  "vendor": "Infosys",
  "risk": "High",
  "insights": []
}
```

---

## GET /ai/health

### Output

```json
{
  "status": "OK",
  "model": "llama-3.1-8b-instant"
}
```

---

# Features

- AI vendor risk analysis
- Recommendation generation
- ChromaDB knowledge retrieval
- Secure Flask APIs
- Docker support
- Health monitoring
- Input sanitization
- Response caching

---

# Final Outcome

Successfully implemented a secure AI-powered Vendor Risk Scorecard backend with intelligent risk analysis and REST API integration.
