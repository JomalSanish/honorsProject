class ScoringEngine:

    def calculate_skill_match(self, skills, required):
        if not required:
            return 0.5
        return len(set(skills) & set(required)) / len(required)

    def calculate_experience_score(self, exp, min_exp):
        if min_exp == 0:
            return 1
        return min(exp / max(min_exp, 1), 1)

    def calculate_project_score(self, proj, intern):
        return min((proj + intern) / 5, 1)

    def calculate_education_match(self, edu, req):
        if not req:
            return 1
        return 1 if req.lower() in edu.lower() else 0

    def compute_final_score(self, f):
        return (
            0.4 * f["semantic_similarity"] +
            0.2 * f["skill_match_ratio"] +
            0.15 * f["experience_score"] +
            0.15 * f["project_score"] +
            0.1 * f["education_match_score"]
        )