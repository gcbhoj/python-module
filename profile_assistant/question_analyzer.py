from enum import Enum
from sentence_transformers import SentenceTransformer, util

# Import only Question Enums needed for intent recognition
from profile_assistant.const_enums import (
    TimedGreeting,
    NormalGreetings,
    BotsInformation,
    DateTimeInformation,
    DeveloperInformation,
    GeographicInformation,
    ProfileInformation,
)


class SentenceAnalyzer:

    def __init__(self, threshold: float = 0.45):
        self.threshold = threshold
        # 1. Load sentence-transformer model once
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # 2. List all Question Enum classes to analyze
        self.question_enums = [
            TimedGreeting,
            NormalGreetings,
            BotsInformation,
            DeveloperInformation,
            DateTimeInformation,
            GeographicInformation,
            ProfileInformation,
        ]

        # 3. Aggregate enum entries into unified lookup lists
        self.enum_members = []
        self.questions_text = []

        for q_enum_cls in self.question_enums:
            for question_member in q_enum_cls:
                self.enum_members.append(question_member)
                self.questions_text.append(question_member.value)

        # 4. Pre-compute vector embeddings once at application startup
        self.question_embeddings = self.model.encode(
            self.questions_text, convert_to_tensor=True
        )

    def analyse_user_input(self, user_input: str):
        """Analyzes user input across ALL question categories and identifies the matched intent."""
        # 1. Convert user query to vector embedding
        input_embedding = self.model.encode(user_input, convert_to_tensor=True)

        # 2. Measure cosine similarity against all stored question vectors
        cosine_scores = util.cos_sim(
            input_embedding, self.question_embeddings
        )[0]

        # 3. Find index of highest match score
        best_idx = int(cosine_scores.argmax())
        best_score = float(cosine_scores[best_idx])

        # 4. Return intent details if confidence passes threshold
        if best_score >= self.threshold:
            matched_question_member = self.enum_members[best_idx]

            return {
                "matched": True,
                "confidence": round(best_score, 4),
                "category": matched_question_member.__class__.__name__,
                "intent": matched_question_member.name,
                "matched_question": matched_question_member.value,
            }

        # Fallback when no category meets threshold
        return {
            "matched": False,
            "confidence": round(best_score, 4),
            "category": None,
            "intent": None,
            "matched_question": None,
        }