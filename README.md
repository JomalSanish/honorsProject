# IntelliPlace – AI Resume Ranking System

## 📌 Overview

IntelliPlace is an AI-powered resume screening system designed for **recruiters** to streamline candidate shortlisting.
It analyses multiple resumes against a job description and ranks candidates based on **semantic relevance**, making hiring faster and more consistent.

---

## 🎯 Key Features

* Upload **Job Description** (PDF/DOCX or text)
* Upload **multiple resumes** (PDF/DOCX)
* AI-based **semantic similarity matching (Sentence-BERT)**
* Automatic **candidate ranking**
* **Explainable results**:

  * Extracted skills
  * Matched skills
  * Missing skills
* Candidate **name extraction**

---

## 🧠 Methodology (ML Pipeline)

1. **Text Extraction**

   * Parse resumes and JD from PDF/DOCX
   * Convert to clean text

2. **Resume Parsing**

   * Extract:

     * Skills
     * Experience
     * Projects
     * Education
     * Name

3. **Semantic Matching**

   * Use **Sentence-BERT embeddings**
   * Compute similarity:

     * Resume ↔ Job Description

4. **Skill Comparison**

   * Extract skills from JD
   * Compare with resume:

     * Matched skills
     * Missing skills

5. **Ranking**

   * Rank candidates by **semantic similarity score**

6. **Explainability**

   * Provide insights into:

     * What matched
     * What is missing

---

## 🏗️ Tech Stack

### Backend

* FastAPI
* spaCy (NLP)
* Sentence-Transformers (SBERT)
* pdfplumber, python-docx

### Frontend

* React (Vite)
* JSX

---

## 📂 Project Structure

```text
honorsProject/
│── main.py
│── services/
│   ├── resume_parser.py
│   ├── semantic_matcher.py
│   ├── file_parser.py
│
│── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
```

---

## 🚀 Setup Instructions

### 🔹 Backend (inside honorsProject)

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
    "score": 0.82,
    "details": {
      "skills": ["python", "machine learning"],
      "matched_skills": ["python"],
      "missing_skills": ["react"],
      "explanation": "Matched Skills: python | Missing Skills: react"
    }
  }
]
```

---

## 📊 Workflow

1. Recruiter uploads JD (file or text)
2. Uploads multiple resumes
3. Clicks **Analyse**
4. System returns:

   * Ranked candidates
   * Skill match insights

---

## ⚠️ Limitations

* Name extraction is heuristic
* Skill extraction is rule-based
* Uses pre-trained embeddings (not fine-tuned)

---

## 🔮 Future Improvements

* Fine-tuned ML models
* Better skill ontology
* Resume–JD highlighting
* Feedback-based learning

---

## 📌 Conclusion

This project demonstrates how **NLP and transformer-based models** can automate resume screening and improve recruitment efficiency.

---

## 👨‍💻 Author

Developed as part of an academic ML project focused on intelligent recruitment systems.
