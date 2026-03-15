from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os


class ResumeATS:

    def __init__(self):

        print("Loading AI model...")

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        print("Model loaded successfully!")

        self.skills_db = [
            "python","java","c++","javascript","nodejs","react",
            "sql","mongodb","mysql","aws","docker","kubernetes",
            "git","html","css","fastapi","flask",
            "machine learning","deep learning","nlp",
            "tensorflow","pytorch","pandas","numpy"
        ]


    def extract_skills(self, text):

        text = text.lower()

        found = []

        for skill in self.skills_db:
            if skill in text:
                found.append(skill)

        return list(set(found))


    def rank_resumes(self, jd_text, resume_texts):

        jd_embedding = self.model.encode([jd_text])
        resume_embeddings = self.model.encode(resume_texts)

        scores = cosine_similarity(jd_embedding, resume_embeddings)[0]

        jd_skills = self.extract_skills(jd_text)

        results = []

        for i, score in enumerate(scores):

            resume_skills = self.extract_skills(resume_texts[i])

            matched = list(set(jd_skills) & set(resume_skills))
            missing = list(set(jd_skills) - set(resume_skills))

            skill_match = 0
            if len(jd_skills) > 0:
                skill_match = len(matched) / len(jd_skills)

            final_score = (0.7 * score) + (0.3 * skill_match)

            results.append({
                "resume_id": i,
                "score": round(float(final_score), 3),
                "skill_match": round(skill_match * 100, 2),
                "matched_skills": matched,
                "missing_skills": missing
            })

        results = sorted(results, key=lambda x: x["score"], reverse=True)

        # GROUP SAME SCORES

        grouped = {}

        for r in results:

            score = r["score"]

            if score not in grouped:
                grouped[score] = []

            grouped[score].append(r)

        bundled = []

        for score, candidates in grouped.items():

            bundled.append({
                "score": score,
                "candidates": candidates
            })

        return bundled