from sentence_transformers import SentenceTransformer, util

class SemanticMatcher:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def compute_similarity(self, resume_text, jd_text):
        return float(util.cos_sim(
            self.model.encode(resume_text, convert_to_tensor=True),
            self.model.encode(jd_text, convert_to_tensor=True)
        ))