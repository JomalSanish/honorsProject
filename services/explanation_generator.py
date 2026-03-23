class ExplanationGenerator:
    def generate(self, score, decision):
        return f"Score: {score:.2f} → {decision}"