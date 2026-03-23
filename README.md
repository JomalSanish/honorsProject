# Resume Analyzer – AI Resume Ranking System

## 📌 Overview

Resume Analyzer is an AI-powered resume screening system designed to help **recruiters efficiently shortlist candidates**.
It analyses multiple resumes against a job description and ranks candidates using a combination of **semantic similarity and structured scoring**.

The system reduces manual effort and provides **explainable insights** into candidate suitability.

---

## 🎯 Key Features

* Upload **Job Description** (PDF/DOCX or text)
* Upload **multiple resumes** (PDF/DOCX)
* AI-based **semantic similarity matching (Sentence-BERT)**
* Hybrid scoring using:

  * Semantic relevance
  * Skill matching
  * Experience
  * Projects
  * Education
* Automatic **candidate ranking**
* **Explainable results**:

  * Extracted skills
  * Matched skills
  * Missing skills
  * Score breakdown
* Basic **candidate name extraction**

---

## 🧠 Methodology (Pipeline)

### 1. Input Module

* Accept resumes and job descriptions (PDF/DOCX/text)
* Extract raw text using file parsers

---

### 2. Text Processing Module

* Clean and normalise text (lowercasing, removing noise)
* Used for semantic comparison

---

### 3. Feature Extraction

From resumes and job descriptions:

* Skills
* Experience (years)
* Projects
* Education
* Name

---

### 4. Semantic Matching

* Use **Sentence-BERT (all-MiniLM-L6-v2)**
* Compute cosine similarity:

  * Resume ↔ Job Description

---

### 5. Scoring System (Hybrid)

Final score is computed using weighted features:

* Semantic similarity
* Skill match ratio
* Experience score
* Project score
* Education match

#### ⚠️ Role-Aware Adjustment

* If semantic similarity is low, a **penalty is applied**
* Prevents mismatched roles (e.g., developer resume for sales job)

---

### 6. Ranking

* Candidates are ranked based on final score
* Highest score = best match

---

### 7. Explainability

For each candidate:

* Matched skills
* Missing skills
* Score breakdown (semantic, skills, experience, etc.)

---

## 🏗️ Tech Stack

### Backend

* FastAPI
* Sentence-Transformers (SBERT)
* pdfplumber, python-docx
* Regex-based parsing

### Frontend

* React (Vite)
* JSX
* CSS

---

## 📂 Project Structure

```text
honorsProject/
│── main.py
│── services/
│   ├── resume_parser.py
│   ├── semantic_matcher.py
│   ├── scoring_engine.py
│   ├── text_processor.py
│   ├── file_parser.py
│
│── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
```

---

## 🚀 Setup Instructions

### 🔹 Backend

```bash
cd honorsProject
python -m venv venv
venv\Scripts\activate   # Windows

pip install -r requirements.txt
```

Run server:

```bash
uvicorn main:app --reload
```

---

### 🔹 Frontend

```bash
cd honorsProject/frontend
npm install
npm run dev
```

---

## 📡 API Endpoint

### `POST /rank-resumes-files`

#### Inputs:

* `resumes`: multiple resume files
* `jd_file`: job description file (optional)
* `job_description`: text (optional)

#### Output:

```json
[
  {
    "rank": 1,
    "name": "John Doe",
    "score": 0.78,
    "details": {
      "skills": ["python", "sql"],
      "matched_skills": ["python"],
      "missing_skills": ["react"],
      "explanation": "Semantic: 0.72, Skills: 0.50, Experience: 0.60, Projects: 0.80, Education: 1.00"
    }
  }
]
```

---

## 📊 Workflow

1. Upload Job Description (file or text)
2. Upload multiple resumes
3. Click **Analyse**
4. System returns:

   * Ranked candidates
   * Skill match insights
   * Score breakdown

---

## ⚠️ Limitations

* Skill extraction is rule-based (limited skill list)
* Experience extraction is regex-based (approximate)
* Name extraction is heuristic
* No database or persistence layer
* Uses pre-trained embeddings (not fine-tuned)

---

## 🔮 Future Improvements

* Expanded skill ontology (100+ skills)
* Named Entity Recognition (NER) for better parsing
* Fine-tuned embedding models
* Resume–JD highlighting
* Dashboard with filters and analytics
* Feedback-based learning system

---

## 📌 Conclusion

Resume Analyzer demonstrates how **NLP and transformer-based models** can automate resume screening by combining **semantic understanding with structured scoring**, making recruitment faster and more consistent.

---

## 👨‍💻 Author

Developed as part of an academic project on intelligent recruitment systems.
