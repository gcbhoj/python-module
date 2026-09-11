import re
from enum import Enum
from sentence_transformers import SentenceTransformer, util


from config.logger_config import configure_logging

from profile_assistant.const_enums import (
    BotsInformation,
    DateTimeInformation,
    DeveloperInformation,
    GeographicInformation,
    NormalGreetings,
    ProfileInformation,
    TimedGreeting,
)
from app_constants.logging_enums import ApplicationLayerLogging, LogEvent, LoggingComponent

class PersonCall(Enum):
    BOT = "you"
    PROFILE_OWNER = "he/his"
    USER = "my"

logger = configure_logging()
class SentenceAnalyzer:
    """Analyzes user input and determines the most likely profile assistant intent."""
    def __init__(self, threshold: float = 0.35):
        logger.info(
            "[%s] [%s] [%s] initializing sentence analyzer",
            ApplicationLayerLogging.PROFILE_ASSISTANT.value,
            LoggingComponent.QUESTION_ANALYZER.value,
            LogEvent.STARTED.value,
        )
        self.threshold = threshold
        logger.info(
            "[%s] [%s] [%s] loading sentence transformer model",
            ApplicationLayerLogging.PROFILE_ASSISTANT.value,
            LoggingComponent.QUESTION_ANALYZER.value,
            LogEvent.STARTED.value,
        )
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        logger.info(
            "[%s] [%s] [%s] sentence transformer model loaded",
            ApplicationLayerLogging.PROFILE_ASSISTANT.value,
            LoggingComponent.QUESTION_ANALYZER.value,
            LogEvent.COMPLETED.value,
        )

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
        logger.info(
            "[%s] [%s] [%s] building question index",
            ApplicationLayerLogging.PROFILE_ASSISTANT.value,
            LoggingComponent.QUESTION_ANALYZER.value,
            LogEvent.STARTED.value,
        )

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
        logger.debug(
            "[%s] [%s] indexed %s question variations",
            ApplicationLayerLogging.PROFILE_ASSISTANT.value,
            LoggingComponent.QUESTION_ANALYZER.value,
            len(self.questions_text),
        )

        logger.info(
            "[%s] [%s] [%s] question index built",
            ApplicationLayerLogging.PROFILE_ASSISTANT.value,
            LoggingComponent.QUESTION_ANALYZER.value,
            LogEvent.COMPLETED.value,
        )

        logger.info(
            "[%s] [%s] [%s] generating question embeddings",
            ApplicationLayerLogging.PROFILE_ASSISTANT.value,
            LoggingComponent.QUESTION_ANALYZER.value,
            LogEvent.STARTED.value,
        )

        # Pre-compute target sentence embeddings
        self.question_embeddings = self.model.encode(
            self.questions_text, convert_to_tensor=True
        )
        logger.info(
            "[%s] [%s] [%s] question embeddings generated",
            ApplicationLayerLogging.PROFILE_ASSISTANT.value,
            LoggingComponent.QUESTION_ANALYZER.value,
            LogEvent.COMPLETED.value,
        )

        logger.info(
            "[%s] [%s] [%s] sentence analyzer initialized",
            ApplicationLayerLogging.PROFILE_ASSISTANT.value,
            LoggingComponent.QUESTION_ANALYZER.value,
            LogEvent.COMPLETED.value,
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
        logger.info(
            "[%s] [%s] [%s] analyzing user input",
            ApplicationLayerLogging.PROFILE_ASSISTANT.value,
            LoggingComponent.QUESTION_ANALYZER.value,
            LogEvent.STARTED.value,
        )
        # 1. Normalize entity pronouns in query
        normalized_query = self._normalize_entity_references(user_input)
        logger.debug(
            "[%s] [%s] normalized user input=[%s]",
            ApplicationLayerLogging.PROFILE_ASSISTANT.value,
            LoggingComponent.QUESTION_ANALYZER.value,
            normalized_query,
        )

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
        logger.debug(
            "[%s] [%s] semantic match category=[%s], intent=[%s], confidence=[%.4f]",
            ApplicationLayerLogging.PROFILE_ASSISTANT.value,
            LoggingComponent.QUESTION_ANALYZER.value,
            matched_member.__class__.__name__,
            matched_member.name,
            best_score,
        )

        if best_score < self.threshold:
            logger.debug(
            "[%s] [%s] semantic match category=[%s], intent=[%s], confidence=[%.4f]",
            ApplicationLayerLogging.PROFILE_ASSISTANT.value,
            LoggingComponent.QUESTION_ANALYZER.value,
            matched_member.__class__.__name__,
            matched_member.name,
            best_score,
        )
            # Keyword check for short single-word queries like "purpose"
            query_tokens = set(normalized_query.split())
            target_tokens = set(self.questions_text[best_idx].split())

            # Overlap check
            if query_tokens.intersection(target_tokens) and any(
                len(w) > 3 for w in query_tokens
            ):
                logger.info(
                    "[%s] [%s] keyword fallback matched user input",
                    ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                    LoggingComponent.QUESTION_ANALYZER.value,
                )
                best_score = max(best_score, 0.40)  # Boost confidence score

        # 5. Return matched intent structure
        if best_score >= self.threshold:
            result =  {
                "matched": True,
                "confidence": round(best_score, 4),
                "category": matched_member.__class__.__name__,
                "intent": matched_member.name,
                "matched_question": matched_member.value,
            }
            logger.info(
                "[%s] [%s] [%s] user input matched category=[%s], intent=[%s], confidence=[%.4f]",
                ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                LoggingComponent.QUESTION_ANALYZER.value,
                LogEvent.COMPLETED.value,
                result["category"],
                result["intent"],
                result["confidence"],
            )
            return result
        # No match
        logger.warning(
            "[%s] [%s] no matching intent found, confidence=[%.4f] [%s]",
            ApplicationLayerLogging.PROFILE_ASSISTANT.value,
            LoggingComponent.QUESTION_ANALYZER.value,
            best_score,
            LogEvent.FAILED.value,
        )
        return {
            "matched": False,
            "confidence": round(best_score, 4),
            "category": None,
            "intent": None,
            "matched_question": None,
        }