# Vendor Risk Scorecard Generator – AI Service

## 📌 Overview
This AI service analyzes vendor risk based on input data and generates structured insights using AI.

## 👩‍💻 Role

**AI Developer 1**

Responsible for:
* Prompt design
* API development
* AI integration
* Structured response generation

## Work Summary

### ✅ Day 1

* Setup Flask project structure
* Created folders: `routes/`, `services/`, `prompts/`
* Configured `app.py` entry point
* Added dependencies (`requirements.txt`)

### ✅ Day 2

* Designed and refined prompt template
* Tested with multiple real inputs
* Ensured consistent AI outputs

### ✅ Day 3

* Implemented POST API: `/ai/describe`
* Features:
  * Input validation
  * Prompt loading
  * Groq AI integration
  * Structured JSON response

## API Endpoint

### POST `/ai/describe`

### Request
json
{
  "vendor_name": "ABC Corp",
  "country": "India",
  "industry": "Finance",
  "revenue": "10M",
  "compliance": "ISO27001",
  "incidents": "None"
}

### Response

json
{
  "risk_level": "Low",
  "reasons": "Compliance status is ISO27001 and no past incidents",
  "recommendations": [
    {
      "desc": "Perform regular audits",
      "status": "Recommended"
    }
  ],
  "generated_at": "auto"
}

## Tech Stack
* Python
* Flask
* Groq API
* Postman

## Testing
Tested using Postman:

http://127.0.0.1:5000/ai/describe



# 🚀 Day 4 – AI Recommendation API

This module implements an AI-powered recommendation service for vendor risk analysis.
It exposes a REST API that generates **structured recommendations** based on vendor name and risk score.

## ⚙️ Tech Stack

* Python (Flask)
* Groq API (LLM)
* Postman (Testing)

## 🔗 API Endpoint

### POST `/ai/recommend`

#### Request Body

```json
{
  "vendor": "Infosys",
  "risk_score": "High"
}

#### Response

json
[
  {
    "action_type": "Review vendor credentials",
    "description": "Verify vendor identity and compliance",
    "priority": "High"
  },
  {
    "action_type": "Conduct security audit",
    "description": "Assess vendor security controls",
    "priority": "High"
  },
  {
    "action_type": "Establish communication",
    "description": "Ensure proper issue resolution channels",
    "priority": "Medium"
  }
]

## 🧪 Testing (Postman)

* Method: `POST`
* URL: `http://127.0.0.1:5000/ai/recommend`
* Body: JSON (as shown above)

## ⚠️ Error Handling

* Returns error if input is missing
* Handles invalid JSON from AI
* Provides fallback response if parsing fails

## ✅ Status

✔ API implemented
✔ AI integrated
✔ JSON output validated
✔ Tested successfully


###  🚀 Day 5 – AI Integration & Combined Analysis API

Day 5 focuses on integrating multiple AI responses into a single unified API.
The system combines **risk analysis (Day 3)** and **recommendations (Day 4)** into a structured and production-ready response.

## 🔗 API Endpoint

**POST** `/ai/recommend`

## 📥 Request Body

```json
{
  "vendor": "Infosys",
  "risk_score": "High"
}

## 📤 Response

```json
{
  "risk_level": "High",
  "reasons": [
    "Vendor has experienced data breaches",
    "Weak security infrastructure"
  ],
  "recommendations": [
    {
      "action_type": "Vendor Evaluation",
      "description": "Review vendor compliance with security standards",
      "priority": "High"
    },
    {
      "action_type": "Risk Mitigation Strategy",
      "description": "Develop a mitigation plan for identified risks",
      "priority": "High"
    }
  ],
  "generated_at": "2026-05-01T07:17:29"
}

## ⚙️ How It Works

### Step 1: Risk Analysis (Day 3)

* AI evaluates vendor risk
* Returns:

  * `risk_level`
  * `reasons`

### Step 2: Recommendations (Day 4)

* AI generates mitigation actions
* Returns:

  * List of recommendations

### Step 3: Combine Results (Day 5)

* Merge both outputs
* Add timestamp
* Return final structured response

## 🛡️ Error Handling

* Handles invalid AI responses
* Uses fallback if JSON parsing fails
* Prevents API crashes using try/except

## ✅ Status

* ✔ AI integration completed
* ✔ Combined API implemented
* ✔ Error handling added
* ✔ Tested using Postman






