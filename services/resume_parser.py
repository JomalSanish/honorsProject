import re

class ResumeParser:
    def __init__(self):
        # Skill dictionary (basic ontology)
        self.skills_list = [
            "python", "java", "machine learning", "ml",
            "react", "node", "node.js", "sql"
        ]

    def extract_name(self, text):
        lines = text.strip().split("\n")
        if len(lines) > 0:
            return lines[0].strip()
        return "Unknown"

    def extract_skills(self, text):
        text_lower = text.lower()
        found = set()

        for skill in self.skills_list:
            if skill in text_lower:
                # normalize variants
                if skill in ["ml", "machine learning"]:
                    found.add("machine learning")
                elif skill in ["node", "node.js"]:
                    found.add("node")
                else:
                    found.add(skill)

        return list(found)

    def extract_experience(self, text):
        text_lower = text.lower()

        # match: 2 years, 3 yr, 1 year etc.
        matches = re.findall(r'(\d+)\s*(year|yr)', text_lower)
        years = sum(int(m[0]) for m in matches)

        return years

    def extract_projects(self, text):
        text_lower = text.lower()

        # count keywords
        return text_lower.count("project") + text_lower.count("developed")

    def parse(self, text):
        skills = self.extract_skills(text)
        experience_years = self.extract_experience(text)
        project_count = self.extract_projects(text)

        education = "Bachelor"
        if "master" in text.lower():
            education = "Master"

        internship_count = 1 if "intern" in text.lower() else 0

        return {
            "name": self.extract_name(text),
            "skills": skills,
            "experience_years": experience_years,
            "project_count": project_count,
            "internship_count": internship_count,
            "education_degree": education
        }