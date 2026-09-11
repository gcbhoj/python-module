from config.logger_config import configure_logging

from profile_assistant.const_enums import ChatType
from repository.profile_assistant_repo import ProfileAssistantRepo
from profile_assistant.profile_assistant import ProfileAssistant

from app_constants.logging_enums import (
    ApplicationLayerLogging,
    LogEvent,
    LoggingComponent,
)


logger = configure_logging()


class ProfileAssistantService:
    """
    Service layer for managing Profile Assistant operations.

    This class acts as an intermediary between the controller,
    ProfileAssistantRepo, and ProfileAssistant components.
    """

    def __init__(self):
        """
        Initialize the Profile Assistant service and its dependencies.
        """

        logger.info(
            "[%s] [%s] initializing profile assistant service [%s]",
            ApplicationLayerLogging.SERVICE.value,
            LoggingComponent.PROFILE_ASSISTANT_SERVICE.value,
            LogEvent.STARTED.value,
        )

        # Initialize the repository responsible for chat and profile data.
        self.repo = ProfileAssistantRepo()

        # Initialize the Profile Assistant responsible for processing
        # user queries and generating responses.
        self.profile_assistant = ProfileAssistant()

        logger.info(
            "[%s] [%s] profile assistant service initialized [%s]",
            ApplicationLayerLogging.SERVICE.value,
            LoggingComponent.PROFILE_ASSISTANT_SERVICE.value,
            LogEvent.COMPLETED.value,
        )

    def init_profile_assistant_repo(self):
        """
        Initialize the Profile Assistant repository data.

        Returns:
            Result returned by the repository initialization method.
        """

        logger.info(
            "[%s] [%s] initializing profile assistant repository [%s]",
            ApplicationLayerLogging.SERVICE.value,
            LoggingComponent.PROFILE_ASSISTANT_SERVICE.value,
            LogEvent.STARTED.value,
        )

        logger.info(
            "[%s] [%s] calling profile assistant repository [%s]",
            ApplicationLayerLogging.SERVICE.value,
            LoggingComponent.PROFILE_ASSISTANT.value,
            LogEvent.CALLED.value,
        )

        # Initialize the repository and required profile data.
        result = self.repo.initialize_profile_assistant()

        logger.info(
            "[%s] [%s] profile assistant repository initialization completed [%s]",
            ApplicationLayerLogging.SERVICE.value,
            LoggingComponent.PROFILE_ASSISTANT_SERVICE.value,
            LogEvent.COMPLETED.value,
        )

        return result

    def fetch_name(self):
        """
        Retrieve the profile assistant user's name.

        Returns:
            The name retrieved from the repository.
        """

        logger.info(
            "[%s] [%s] fetching profile name [%s]",
            ApplicationLayerLogging.SERVICE.value,
            LoggingComponent.PROFILE_ASSISTANT_SERVICE.value,
            LogEvent.STARTED.value,
        )

        # Retrieve the user's name from the repository.
        result = self.repo.retrieve_name()

        logger.info(
            "[%s] [%s] profile name retrieved [%s]",
            ApplicationLayerLogging.SERVICE.value,
            LoggingComponent.PROFILE_ASSISTANT_SERVICE.value,
            LogEvent.COMPLETED.value,
        )

        return result

    def init_new_chat(self):
        """
        Initialize a new Profile Assistant chat session.

        Returns:
            Result returned by the repository.
        """

        logger.info(
            "[%s] [%s] initializing new chat session [%s]",
            ApplicationLayerLogging.SERVICE.value,
            LoggingComponent.PROFILE_ASSISTANT_SERVICE.value,
            LogEvent.STARTED.value,
        )

        # Request the repository to create a new chat session.
        result = self.repo.initialize_new_chat_session()

        logger.info(
            "[%s] [%s] new chat session initialized [%s]",
            ApplicationLayerLogging.SERVICE.value,
            LoggingComponent.PROFILE_ASSISTANT_SERVICE.value,
            LogEvent.COMPLETED.value,
        )

        return result

    def enable_speech_mode(self):
        """
        Enable speech/voice mode for the Profile Assistant.

        Returns:
            Result returned by the Profile Assistant.
        """

        logger.info(
            "[%s] [%s] enabling speech mode [%s]",
            ApplicationLayerLogging.SERVICE.value,
            LoggingComponent.PROFILE_ASSISTANT_SERVICE.value,
            LogEvent.STARTED.value,
        )

        # Delegate voice-mode activation to the Profile Assistant.
        result = self.profile_assistant.enable_voice()

        logger.info(
            "[%s] [%s] speech mode enabled [%s]",
            ApplicationLayerLogging.SERVICE.value,
            LoggingComponent.PROFILE_ASSISTANT_SERVICE.value,
            LogEvent.COMPLETED.value,
        )

        return result

    def disable_speech_mode(self):
        """
        Disable speech/voice mode for the Profile Assistant.

        Returns:
            Result returned by the Profile Assistant.
        """

        logger.info(
            "[%s] [%s] disabling speech mode [%s]",
            ApplicationLayerLogging.SERVICE.value,
            LoggingComponent.PROFILE_ASSISTANT_SERVICE.value,
            LogEvent.STARTED.value,
        )

        # Delegate voice-mode deactivation to the Profile Assistant.
        result = self.profile_assistant.disable_voice()

        logger.info(
            "[%s] [%s] speech mode disabled [%s]",
            ApplicationLayerLogging.SERVICE.value,
            LoggingComponent.PROFILE_ASSISTANT_SERVICE.value,
            LogEvent.COMPLETED.value,
        )

        return result

    def start_chat(self, chat_id, text):
        """
        Process a user's chat request through the Profile Assistant.

        Args:
            chat_id: Identifier of the current chat session.
            text: User's chat message.

        Returns:
            Dictionary containing the Profile Assistant response.

        Raises:
            ValueError: If chat_id is missing or text is empty.
        """

        logger.info(
            "[%s] [%s] starting profile assistant conversation [%s]",
            ApplicationLayerLogging.SERVICE.value,
            LoggingComponent.PROFILE_ASSISTANT_SERVICE.value,
            LogEvent.STARTED.value,
        )

        # Validate the chat session identifier before processing
        # the user's request.
        if not chat_id:
            logger.warning(
                "[%s] [%s] chat ID is missing [%s]",
                ApplicationLayerLogging.SERVICE.value,
                LoggingComponent.PROFILE_ASSISTANT_SERVICE.value,
                LogEvent.FAILED.value,
            )

            raise ValueError(
                "Chat ID is required to add chat data."
            )

        # Validate that the user provided a non-empty message.
        if not text or not text.strip():
            logger.warning(
                "[%s] [%s] chat text is empty or missing [%s]",
                ApplicationLayerLogging.SERVICE.value,
                LoggingComponent.PROFILE_ASSISTANT_SERVICE.value,
                LogEvent.FAILED.value,
            )

            raise ValueError(
                "Text cannot be empty."
            )

        logger.info(
            "[%s] [%s] adding user request to chat history [%s]",
            ApplicationLayerLogging.SERVICE.value,
            LoggingComponent.PROFILE_ASSISTANT_SERVICE.value,
            LogEvent.CALLED.value,
        )

        # Store the user's request before sending it to the assistant.
        self.repo.add_chat_data(
            chat_id,
            ChatType.REQUEST,
            text,
        )

        logger.info(
            "[%s] [%s] calling profile assistant [%s]",
            ApplicationLayerLogging.SERVICE.value,
            LoggingComponent.PROFILE_ASSISTANT.value,
            LogEvent.CALLED.value,
        )

        # Process the user's request through the Profile Assistant.
        result = self.profile_assistant.start(text)

        logger.info(
            "[%s] [%s] profile assistant response generated [%s]",
            ApplicationLayerLogging.SERVICE.value,
            LoggingComponent.PROFILE_ASSISTANT.value,
            LogEvent.COMPLETED.value,
        )

        # Extract the assistant's response message and store it
        # in the current chat session.
        response_message = result.get("message")

        self.repo.add_chat_data(
            chat_id,
            ChatType.RESPONSE,
            response_message,
        )

        logger.info(
            "[%s] [%s] assistant response stored [%s]",
            ApplicationLayerLogging.SERVICE.value,
            LoggingComponent.PROFILE_ASSISTANT_SERVICE.value,
            LogEvent.COMPLETED.value,
        )

        logger.info(
            "[%s] [%s] profile assistant conversation completed [%s]",
            ApplicationLayerLogging.SERVICE.value,
            LoggingComponent.PROFILE_ASSISTANT_SERVICE.value,
            LogEvent.COMPLETED.value,
        )

        # Do not log the actual user text or response content here.
        # Chat messages may contain sensitive or private information.
        return result