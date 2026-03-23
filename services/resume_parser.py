import re

class ResumeParser:
    def __init__(self):
        self.skills_list = [
            "python", "java", "machine learning",
            "react", "node", "sql"
        ]

    def extract_name(self, text):
        lines = text.strip().split("\n")

        for line in lines[:3]:  # check first few lines
            words = line.strip().split()
            if 2 <= len(words) <= 5:
                return line.strip()

        return "Unknown"

    def extract_skills(self, text):
        text_lower = text.lower()
        found = set()

        for skill in self.skills_list:
            if skill in text_lower:
                found.add(skill)

        return list(found)

    def extract_experience(self, text):
        matches = re.findall(r'(\d+)\s*(year|yr)', text.lower())
        return sum(int(m[0]) for m in matches)

    def extract_projects(self, text):
        text_lower = text.lower()
        return text_lower.count("project") + text_lower.count("developed")

    def parse(self, text):
        return {
            "name": self.extract_name(text),
            "skills": self.extract_skills(text),
            "experience_years": self.extract_experience(text),
            "project_count": self.extract_projects(text),
            "internship_count": 1 if "intern" in text.lower() else 0,
            "education_degree": "Master" if "master" in text.lower() else "Bachelor"
        }