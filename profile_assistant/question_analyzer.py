import re
from enum import Enum
from sentence_transformers import SentenceTransformer, util

from profile_assistant.const_enums import (
    BotsInformation,
    DateTimeInformation,
    DeveloperInformation,
    GeographicInformation,
    NormalGreetings,
    ProfileInformation,
    TimedGreeting,
)


class PersonCall(Enum):
    BOT = "you"
    PROFILE_OWNER = "he/his"
    USER = "my"


class SentenceAnalyzer:

    def __init__(self, threshold: float = 0.35):
        self.threshold = threshold
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.question_enums = [
            TimedGreeting,
            NormalGreetings,
            BotsInformation,
            DeveloperInformation,
            DateTimeInformation,
            GeographicInformation,
            ProfileInformation,
        ]

        self.enum_members = []
        self.questions_text = []

        # Build index mapping every sample string to its enum member
        for q_enum_cls in self.question_enums:
            for question_member in q_enum_cls:
                val = question_member.value

                # Support both single strings and lists/tuples of question variations
                variations = val if isinstance(val, (list, tuple)) else [val]

                for phrase in variations:
                    normalized_phrase = self._normalize_entity_references(
                        phrase
                    )
                    self.enum_members.append(question_member)
                    self.questions_text.append(normalized_phrase)

        # Pre-compute target sentence embeddings
        self.question_embeddings = self.model.encode(
            self.questions_text, convert_to_tensor=True
        )

    @staticmethod
    def _normalize_entity_references(text: str) -> str:
        """Normalizes possessive and personal pronouns into standardized entities."""
        text = text.lower()

        # Map 'your', 'yours', 'you' -> 'bot'
        text = re.sub(r"\b(your|yours|you)\b", PersonCall.BOT.value, text)

        # Map 'his', 'he', 'developer', 'dev' -> 'developer'
        text = re.sub(
            r"\b(his|he|developer's|developer|dev)\b",
            PersonCall.PROFILE_OWNER.value,
            text,
        )

        # Map 'my', 'mine', 'i' -> 'user'
        text = re.sub(r"\b(my|mine|i)\b", PersonCall.USER.value, text)

        return text.strip()

    def analyse_user_input(self, user_input: str) -> dict:
        """Analyzes normalized user input using hybrid semantic embedding + keyword fallback."""

        # 1. Normalize entity pronouns in query
        normalized_query = self._normalize_entity_references(user_input)

        # 2. Encode normalized input
        input_embedding = self.model.encode(
            normalized_query, convert_to_tensor=True
        )

        # 3. Compute cosine similarity
        cosine_scores = util.cos_sim(
            input_embedding, self.question_embeddings
        )[0]
        best_idx = int(cosine_scores.argmax())
        best_score = float(cosine_scores[best_idx])

        # 4. Hybrid Keyword Fallback (if score is close to threshold)
        matched_member = self.enum_members[best_idx]

        if best_score < self.threshold:
            # Keyword check for short single-word queries like "purpose"
            query_tokens = set(normalized_query.split())
            target_tokens = set(self.questions_text[best_idx].split())

            # Overlap check
            if query_tokens.intersection(target_tokens) and any(
                len(w) > 3 for w in query_tokens
            ):
                best_score = max(best_score, 0.40)  # Boost confidence score

        # 5. Return matched intent structure
        if best_score >= self.threshold:
            return {
                "matched": True,
                "confidence": round(best_score, 4),
                "category": matched_member.__class__.__name__,
                "intent": matched_member.name,
                "matched_question": matched_member.value,
            }

        return {
            "matched": False,
            "confidence": round(best_score, 4),
            "category": None,
            "intent": None,
            "matched_question": None,
        }