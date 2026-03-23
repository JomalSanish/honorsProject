import os
os.environ['TRANSFORMERS_NO_TF'] = '1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from services.resume_parser import ResumeParser
from services.semantic_matcher import SemanticMatcher
from services.file_parser import FileParser
from services.scoring_engine import ScoringEngine
from services.text_processor import TextProcessor

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SERVICES
parser = ResumeParser()
matcher = SemanticMatcher()
file_parser = FileParser()
scorer = ScoringEngine()
processor = TextProcessor()


@app.post("/rank-resumes-files")
async def rank_resumes_files(
    resumes: List[UploadFile] = File(...),
    jd_file: UploadFile = File(None),
    job_description: str = Form("")
):
    try:
        # -------- JD PROCESSING --------
        jd_text_raw = job_description.strip()

        if jd_file:
            jd_bytes = await jd_file.read()
            if jd_file.filename.endswith(".pdf"):
                jd_text_raw += " " + file_parser.parse_pdf(jd_bytes)
            elif jd_file.filename.endswith(".docx"):
                jd_text_raw += " " + file_parser.parse_docx(jd_bytes)

        if not jd_text_raw:
            raise HTTPException(status_code=400, detail="Job description required")

        # Clean only for semantic comparison
        jd_text_clean = processor.clean_text(jd_text_raw)

        # Extract features from RAW text
        jd_features = parser.parse(jd_text_raw)
        jd_skills = jd_features["skills"]

        results = []

        # -------- RESUME PROCESSING --------
        for file in resumes:
            file_bytes = await file.read()

            if file.filename.endswith(".pdf"):
                text_raw = file_parser.parse_pdf(file_bytes)
            elif file.filename.endswith(".docx"):
                text_raw = file_parser.parse_docx(file_bytes)
            else:
                try:
                    text_raw = file_bytes.decode()
                except:
                    continue

            # Clean only for similarity
            text_clean = processor.clean_text(text_raw)

            # Parse RAW text (IMPORTANT FIX)
            parsed = parser.parse(text_raw)

            # -------- FEATURE SCORES --------
            semantic_score = matcher.compute_similarity(text_clean, jd_text_clean)

            skill_score = scorer.calculate_skill_match(
                parsed["skills"], jd_skills
            )

            exp_score = scorer.calculate_experience_score(
                parsed["experience_years"], jd_features["experience_years"]
            )

            proj_score = scorer.calculate_project_score(
                parsed["project_count"],
                parsed["internship_count"]
            )

            edu_score = scorer.calculate_education_match(
                parsed["education_degree"],
                jd_features["education_degree"]
            )

            final_score = scorer.compute_final_score({
                "semantic_similarity": semantic_score,
                "skill_match_ratio": skill_score,
                "experience_score": exp_score,
                "project_score": proj_score,
                "education_match_score": edu_score
            })

            # 🔥 NEW: Role mismatch penalty
            if semantic_score < 0.55:
                final_score *= 0.7

            matched = list(set(parsed["skills"]) & set(jd_skills))
            missing = list(set(jd_skills) - set(parsed["skills"]))

            results.append({
                "name": parsed["name"],
                "score": final_score,
                "breakdown": {
                    "semantic": semantic_score,
                    "skills": skill_score,
                    "experience": exp_score,
                    "projects": proj_score,
                    "education": edu_score
                },
                "skills": parsed["skills"],
                "matched_skills": matched,
                "missing_skills": missing
            })

        # -------- RANKING --------
        results.sort(key=lambda x: x["score"], reverse=True)

        output = []
        for i, r in enumerate(results):
            explanation = (
                f"Semantic: {r['breakdown']['semantic']:.2f}, "
                f"Skills: {r['breakdown']['skills']:.2f}, "
                f"Experience: {r['breakdown']['experience']:.2f}, "
                f"Projects: {r['breakdown']['projects']:.2f}, "
                f"Education: {r['breakdown']['education']:.2f}\n"
                f"Matched Skills: {', '.join(r['matched_skills']) or 'None'}\n"
                f"Missing Skills: {', '.join(r['missing_skills']) or 'None'}"
            )

            output.append({
                "rank": i + 1,
                "name": r["name"],
                "score": round(r["score"], 3),
                "details": {
                    "skills": r["skills"],
                    "matched_skills": r["matched_skills"],
                    "missing_skills": r["missing_skills"],
                    "explanation": explanation
                }
            })

        return output

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))