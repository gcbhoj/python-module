import os
import re
import base64

from config.logger_config import configure_logging

from repository.resume_reader import ResumeReader
from repository.profile_assistant_repo import ProfileAssistantRepo

from app_constants.logging_enums import ApplicationLayerLogging, LogEvent, LoggingComponent
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

logger = configure_logging()
class ProfileAssistant:
    """
    Coordinates the Profile Assistant conversation flow.

    This class receives user input, analyzes the input, generates an
    appropriate response, and optionally converts the response to
    MP3 audio when voice mode is enabled.
    """
    def __init__(self):
        """Initialize the Profile Assistant and its dependencies."""
        self.name = ""
        self.date_of_birth = ""
        # Supported commands that terminate the conversation.
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

        self.profile_assistant_manager = ProfileAssistantManager()

        self.question_analyzer = SentenceAnalyzer()

        self.speaker = Speaker()

        self.repo = ProfileAssistantRepo()

    # =================================================
    # PROCESS USER MESSAGE
    # =================================================

    def start(self, user_input: str):
        logger.info(
        "[%s] [%s] processing user message [%s]",
        ApplicationLayerLogging.PROFILE_ASSISTANT.value,
        LoggingComponent.PROFILE_ASSISTANT.value,
        LogEvent.STARTED.value
    )        
        """
        Process a user's message and generate an assistant response.

        The method validates the input, checks for an exit command,
        analyzes the user's intent, generates a response, and builds
        the final response object.
        """

        if not user_input or not user_input.strip():
            logger.warning("[%s] [%s] user input is  empty [%s]",
                          ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                          LoggingComponent.PROFILE_ASSISTANT.value,
                          LogEvent.FAILED.value)

            return {
                "success": False,
                "message": "User input cannot be empty.",
                "audio": None,
            }

        normalized_input = self._normalize_input(
            user_input
        )
        logger.debug(
            "[%s] [%s] normalized user input: [%s]",
            ApplicationLayerLogging.PROFILE_ASSISTANT.value,
            LoggingComponent.PROFILE_ASSISTANT.value,
            normalized_input
        )

        # Check whether the user wants to end the conversation. 
        if normalized_input in self.final_query:
            logger.info(
            "[%s] [%s] exit command detected [%s]",
            ApplicationLayerLogging.PROFILE_ASSISTANT.value,
            LoggingComponent.PROFILE_ASSISTANT.value,
            LogEvent.CALLED.value
        )
            self.is_final_query = True

            reply = (
                f"Goodbye! "
                f"{self.greeting_manager.generate_exit_greeting()}"
            )

            return self._build_response(reply)

        # Analyze the normalized user input to determine its
        # category and intent.
        logger.info(
        "[%s] [%s] analyzing user input [%s]",
        ApplicationLayerLogging.PROFILE_ASSISTANT.value,
        LoggingComponent.PROFILE_ASSISTANT.value,
        LogEvent.STARTED.value
    )
        analysis = self.question_analyzer.analyse_user_input(normalized_input)

        category = analysis.get("category")
        intent = analysis.get("intent")
        logger.debug(
        "[%s] [%s] analysis category=[%s], intent=[%s]",
        ApplicationLayerLogging.PROFILE_ASSISTANT.value,
        LoggingComponent.QUESTION_ANALYZER.value,
        category,
        intent
    )

        logger.info(
        "[%s] [%s] user input analysis [%s]",
        ApplicationLayerLogging.PROFILE_ASSISTANT.value,
        LoggingComponent.QUESTION_ANALYZER.value,
        LogEvent.COMPLETED.value
    )
        # Generate the appropriate response based on the
        # detected category and intent.

        reply = self._generate_reply(
            category,
            intent
        )

        return self._build_response(reply)

    # =================================================
    # GENERATE RESPONSE
    # =================================================

    def _generate_reply(self, category, intent):
        """
        Generate a text response based on the detected category.

        The category determines which Profile Assistant component
        should handle the request.
        """
        logger.info(
        "[%s] [%s] generating response for category: [%s], intent: [%s] [%s]",
        ApplicationLayerLogging.PROFILE_ASSISTANT.value,
        LoggingComponent.PROFILE_ASSISTANT.value,
        category,
        intent,
        LogEvent.STARTED.value
    )
        match category:

            case NormalGreetings.__name__:
                logger.debug("[%s] [%s] generating normal greeting",
                ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                LoggingComponent.PROFILE_ASSISTANT.value
            )
                return self.greeting_manager.generate_normal_greeting()
            

            case TimedGreeting.__name__:
                logger.debug("[%s] [%s] generating timed greeting",
                ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                LoggingComponent.PROFILE_ASSISTANT.value
            )
                return self.greeting_manager.generate_timed_greeting()
                

            case BotsInformation.__name__:
                logger.debug("[%s] [%s] generating bots information",
                ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                LoggingComponent.PROFILE_ASSISTANT.value
            )
                return self.profile_assistant_manager.generate_bot_info_reply(intent,self.name,self.date_of_birth)

            case DateTimeInformation.__name__:
                logger.debug("[%s] [%s] generating date time information",
                ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                LoggingComponent.PROFILE_ASSISTANT.value
            )
                return self.profile_assistant_manager.generate_date_time_reply(intent)

            case _:
                logger.debug("[%s] [%s] generating default answer",
                ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                LoggingComponent.PROFILE_ASSISTANT.value
            )
                return (
                    "I am not sure how to answer that."
                )

    # =================================================
    # RESPONSE
    # =================================================

    def _build_response(self, reply):
        """
        Build the standardized Profile Assistant response.

        Text is always returned. MP3 audio is generated and Base64
        encoded only when voice mode is enabled.
        """
        logger.info("[%s] [%s] building response [%s]",
                    ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                    LoggingComponent.PROFILE_ASSISTANT.value,
                    LogEvent.STARTED.value)
        
        if not reply:
            logger.warning("[%s] [%s] reply is empty [%s]",
                           ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                           LoggingComponent.PROFILE_ASSISTANT.value,
                           LogEvent.FAILED.value)
            return {
                "success": False,
                "message": "",
                "audio": None,
            }
            
        logger.info("[%s] [%s] formatting reply [%s]",
                    ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                    LoggingComponent.PROFILE_ASSISTANT.value,
                    LogEvent.CALLED.value)
        reply = self._format_reply(reply)
        logger.info("[%s] [%s] formatting reply [%s]",
                    ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                    LoggingComponent.PROFILE_ASSISTANT.value,
                    LogEvent.COMPLETED.value)        

        audio = None

        # Generate audio only when enabled
        if self.is_voice_enabled:
            logger.info("[%s] [%s] verify voice enable and speak method [%s]",
                        ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                        LoggingComponent.PROFILE_ASSISTANT.value,
                        LogEvent.CALLED.value)

            audio_bytes = self.speak(reply)
            logger.info("[%s] [%s] result from speak method [%s]",
                        ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                        LoggingComponent.PROFILE_ASSISTANT.value,
                        LogEvent.COMPLETED.value)            
            if audio_bytes:
                audio = base64.b64encode(audio_bytes).decode("utf-8")
            logger.info("[%s] [%s] build response method completed [%s]",
                        ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                        LoggingComponent.PROFILE_ASSISTANT.value,
                        LogEvent.COMPLETED.value)   
        return {
            "success": True,
            "message": reply,
            "audio": audio,
        }

    # =================================================
    # VOICE BUTTON ACTIONS
    # =================================================

    def enable_voice(self):
        """
        Enable voice responses for subsequent assistant messages.

        Voice mode is controlled explicitly by the frontend rather
        than being determined from the user's detected intent.
        """
        logger.info("[%s] [%s] enable voice [$s]",
                    ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                    LoggingComponent.PROFILE_ASSISTANT.value,
                    LogEvent.STARTED.value)
        #enabling voice
        self.is_voice_enabled = True
        logger.info("[%s] [%s] enable voice [$s]",
                    ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                    LoggingComponent.PROFILE_ASSISTANT.value,
                    LogEvent.COMPLETED.value)
        return {
            "success": True,
            "voiceEnabled": True,
            "message": "Voice mode enabled.",
        }

    def disable_voice(self):
        """
        Disable voice responses for subsequent assistant messages.
        """
        logger.info("[%s] [%s] disable voice [$s]",
                    ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                    LoggingComponent.PROFILE_ASSISTANT.value,
                    LogEvent.STARTED.value)
        # disabling voice        
        self.is_voice_enabled = False
        logger.info("[%s] [%s] enable voice [$s]",
                    ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                    LoggingComponent.PROFILE_ASSISTANT.value,
                    LogEvent.COMPLETED.value)
        return {
            "success": True,
            "voiceEnabled": False,
            "message": "Voice mode disabled.",
        }

    def get_voice_status(self):
        """
        Return the current voice mode state.
        """
        return {
            "voiceEnabled": self.is_voice_enabled
        }

    # =================================================
    # SPEAKER
    # =================================================

    def speak(self, text):
        """
        Convert assistant text into MP3 audio bytes.

        The Speaker class handles the text-to-speech conversion.
        The returned bytes are later Base64 encoded by
        `_build_response()` so they can be returned through JSON.
        """
        logger.info("[%s] [%s] speak method [%s]",
                    ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                    LoggingComponent.PROFILE_ASSISTANT.value,
                    LogEvent.STARTED.value)
        if not text:
            return None
        logger.info("[%s] [%s] speak method [%s]",
                    ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                    LoggingComponent.SPEAKER.value,
                    LogEvent.CALLED.value)
        return self.speaker.speak(text)

    # =================================================
    # STARTUP
    # =================================================

    def get_startup_greeting(self):
        """
        Generate the initial greeting displayed when a chat starts.

        The startup response contains both the time-based greeting
        and the personalized Profile Assistant introduction.
        """
        logger.info("[%s] [%s] generating start up greeting [%s]",
                    ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                    LoggingComponent.PROFILE_ASSISTANT.value,
                    LogEvent.STARTED.value)
        logger.info("[%s] [%s] get alias from resume [%s]",
                    ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                    LoggingComponent.RESUME_READER.value,
                    LogEvent.CALLED.value)
        profile_alias = self.resume_reader.get_alias()
        
        logger.info("[%s] [%s] get timed greeting [%s]",
                    ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                    LoggingComponent.GREETINGS_MANAGER.value,
                    LogEvent.CALLED.value)
        timed = self.greeting_manager.generate_timed_greeting()
        
        logger.info("[%s] [%s] get start up greeting [%s]",
                    ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                    LoggingComponent.GREETINGS_MANAGER.value,
                    LogEvent.CALLED.value)

        startup = self.greeting_manager.generate_startup_greeting(self.name,profile_alias)

        reply = (
            f"{timed}\n"
            f"{startup}"
        )
        logger.info("[%s] [%s] building response [%s]",
                    ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                    LoggingComponent.PROFILE_ASSISTANT.value,
                    LogEvent.CALLED.value)

        return self._build_response(reply)

    # =================================================
    # HELPERS
    # =================================================

    @staticmethod
    def _format_reply(reply):
        """
        Normalize a generated response into a single string.

        Lists and tuples are converted into a sentence separated
        by periods.
        """
        if isinstance(reply, (list, tuple)):

            return ". ".join(
                str(item)
                for item in reply
            )

        return str(reply).strip()

    @staticmethod
    def _normalize_input(user_input: str):
        """
        Normalize user input before question analysis.

        Leading and trailing whitespace, question marks, and
        duplicate whitespace are removed, and the input is
        converted to lowercase.
        """
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