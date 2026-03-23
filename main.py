import os
os.environ['TRANSFORMERS_NO_TF'] = '1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from services.resume_parser import ResumeParser
from services.semantic_matcher import SemanticMatcher
from services.file_parser import FileParser

app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SERVICES
resume_parser = ResumeParser()
semantic_matcher = SemanticMatcher()
file_parser = FileParser()


@app.post("/rank-resumes-files")
async def rank_resumes_files(
    resumes: List[UploadFile] = File(...),
    jd_file: UploadFile = File(None),
    job_description: str = Form("")
):
    try:
        # -------- JD PROCESSING --------
        jd_text = job_description or ""

        if jd_file:
            jd_bytes = await jd_file.read()

            if jd_file.filename.endswith(".pdf"):
                jd_text += file_parser.parse_pdf(jd_bytes)
            elif jd_file.filename.endswith(".docx"):
                jd_text += file_parser.parse_docx(jd_bytes)

        # 🔥 Extract JD skills dynamically (IMPORTANT)
        jd_skills = resume_parser.extract_skills(jd_text)

        # -------- RESUME PROCESSING --------
        results = []

        for file in resumes:
            file_bytes = await file.read()

            if file.filename.endswith(".pdf"):
                text = file_parser.parse_pdf(file_bytes)
            elif file.filename.endswith(".docx"):
                text = file_parser.parse_docx(file_bytes)
            else:
                text = file_bytes.decode()

            parsed = resume_parser.parse(text)

            # 🔥 PURE JD MATCH
            score = semantic_matcher.compute_similarity(text, jd_text)

            candidate_skills = parsed.get("skills", [])

            matched = list(set(candidate_skills) & set(jd_skills))
            missing = list(set(jd_skills) - set(candidate_skills))

            results.append({
                "name": parsed.get("name", "Unknown"),
                "score": score,
                "skills": candidate_skills,
                "matched_skills": matched,
                "missing_skills": missing
            })

        # -------- RANKING --------
        results.sort(key=lambda x: x["score"], reverse=True)

        output = []
        for i, r in enumerate(results):

            explanation = f"""
Matched Skills: {', '.join(r['matched_skills']) if r['matched_skills'] else 'None'}
Missing Skills: {', '.join(r['missing_skills']) if r['missing_skills'] else 'None'}
"""

            output.append({
                "rank": i + 1,
                "name": r["name"],
                "score": round(r["score"], 2),
                "details": {
                    "skills": r["skills"],
                    "matched_skills": r["matched_skills"],
                    "missing_skills": r["missing_skills"],
                    "explanation": explanation.strip()
                }
            })

        return output

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))