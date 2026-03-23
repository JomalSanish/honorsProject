from sentence_transformers import SentenceTransformer, util

class SemanticMatcher:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def compute_similarity(self, r, jd):
        return float(util.cos_sim(
            self.model.encode(r, convert_to_tensor=True),
            self.model.encode(jd, convert_to_tensor=True)
        ))

    def compute_role_similarity(self, r, role):
        return float(util.cos_sim(
            self.model.encode(r, convert_to_tensor=True),
            self.model.encode(role, convert_to_tensor=True)
        ))