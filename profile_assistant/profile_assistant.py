import os
import re
import base64

from repository.resume_reader import ResumeReader
from repository.profile_assistant_repo import ProfileAssistantRepo

from profile_assistant.const_enums import (
    ExitInformation,
    NormalGreetings,
    TimedGreeting,
    BotsInformation,
    DateTimeInformation,
)

from profile_assistant.greetings_manager import GreetingsManager
from profile_assistant.profile_assistant_manager import ProfileAssistantManager
from profile_assistant.question_analyzer import SentenceAnalyzer
from profile_assistant.speaker import Speaker


class ProfileAssistant:

    def __init__(self):

        self.name = "Bahire"
        self.date_of_birth = "2026-08-19"

        self.final_query = [
            enum.value
            for enum in ExitInformation
        ]

        self.is_final_query = False

        # ---------------------------------------------
        # Voice state
        # ---------------------------------------------

        self.is_voice_enabled = False
        # if os.getenv("DEV_ENV") == "development":
        #     self.is_voice_enabled = True


        # ---------------------------------------------
        # Dependencies
        # ---------------------------------------------

        self.resume_reader = ResumeReader()

        self.greeting_manager = GreetingsManager()

        self.myAssistant = ProfileAssistantManager()

        self.question_analyzer = SentenceAnalyzer()

        self.speaker = Speaker()

        self.repo = ProfileAssistantRepo()

    # =================================================
    # PROCESS USER MESSAGE
    # =================================================

    def start(self, user_input: str):

        if not user_input or not user_input.strip():

            return {
                "success": False,
                "message": "User input cannot be empty.",
                "audio": None,
            }

        normalized_input = self._normalize_input(
            user_input
        )

        # ---------------------------------------------
        # Exit
        # ---------------------------------------------

        if normalized_input in self.final_query:

            self.is_final_query = True

            reply = (
                f"Goodbye! "
                f"{self.greeting_manager.generate_exit_greeting()}"
            )

            return self._build_response(reply)

        # ---------------------------------------------
        # Analyze question
        # ---------------------------------------------

        analysis = (
            self.question_analyzer
            .analyse_user_input(
                normalized_input
            )
        )

        category = analysis.get("category")
        intent = analysis.get("intent")

        # ---------------------------------------------
        # Generate response
        # ---------------------------------------------

        reply = self._generate_reply(
            category,
            intent
        )

        return self._build_response(reply)

    # =================================================
    # GENERATE RESPONSE
    # =================================================

    def _generate_reply(self, category, intent):

        match category:

            case NormalGreetings.__name__:

                return (
                    self.greeting_manager
                    .generate_normal_greeting()
                )

            case TimedGreeting.__name__:

                return (
                    self.greeting_manager
                    .generate_timed_greeting()
                )

            case BotsInformation.__name__:

                return (
                    self.myAssistant
                    .generate_bot_info_reply(
                        intent,
                        self.name,
                        self.date_of_birth,
                    )
                )

            case DateTimeInformation.__name__:

                return (
                    self.myAssistant
                    .generate_date_time_reply(
                        intent
                    )
                )

            case _:

                return (
                    "I am not sure how to answer that."
                )

    # =================================================
    # RESPONSE
    # =================================================

    def _build_response(self, reply):

        if not reply:

            return {
                "success": False,
                "message": "",
                "audio": None,
            }

        reply = self._format_reply(reply)

        audio = None

        # Generate audio only when enabled
        if self.is_voice_enabled:

            audio_bytes = self.speak(reply)
            
            if audio_bytes:
                audio = base64.b64encode(audio_bytes).decode("utf-8")

        return {
            "success": True,
            "message": reply,
            "audio": audio,
        }

    # =================================================
    # VOICE BUTTON ACTIONS
    # =================================================

    def enable_voice(self):

        self.is_voice_enabled = True

        return {
            "success": True,
            "voiceEnabled": True,
            "message": "Voice mode enabled.",
        }

    def disable_voice(self):

        self.is_voice_enabled = False

        return {
            "success": True,
            "voiceEnabled": False,
            "message": "Voice mode disabled.",
        }

    def get_voice_status(self):

        return {
            "voiceEnabled": self.is_voice_enabled
        }

    # =================================================
    # SPEAKER
    # =================================================

    def speak(self, text):

        if not text:
            return None

        return self.speaker.speak(text)

    # =================================================
    # STARTUP
    # =================================================

    def get_startup_greeting(self):

        profile_alias = (
            self.resume_reader.get_alias()
        )

        timed = (
            self.greeting_manager
            .generate_timed_greeting()
        )

        startup = (
            self.greeting_manager
            .generate_startup_greeting(
                self.name,
                profile_alias,
            )
        )

        reply = (
            f"{timed}\n"
            f"{startup}"
        )

        return self._build_response(reply)

    # =================================================
    # HELPERS
    # =================================================

    @staticmethod
    def _format_reply(reply):

        if isinstance(reply, (list, tuple)):

            return ". ".join(
                str(item)
                for item in reply
            )

        return str(reply).strip()

    @staticmethod
    def _normalize_input(user_input: str):

        if not user_input:
            return ""

        normalized = (
            user_input
            .strip()
            .lower()
        )

        normalized = normalized.replace(
            "?",
            ""
        )

        normalized = re.sub(
            r"\s+",
            " ",
            normalized
        )

        return normalized.strip()