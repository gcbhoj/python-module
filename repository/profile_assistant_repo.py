import uuid

from datetime import datetime

from config.logger_config import configure_logging

from app_constants.logging_enums import (
    ApplicationLayerLogging,
    LogEvent,
    LoggingComponent,
)

from repository.base_repo import BaseRepository

from profile_assistant.const_enums import ChatType


logger = configure_logging()


class ProfileAssistantRepo(BaseRepository):
    """Repository responsible for Profile Assistant persistence."""

    collection_name = "profile_assistant"

    def __init__(self):
        """Initialize the Profile Assistant repository."""

        super().__init__()

        self.name = "Bahire"
        self.date_of_birth = "2026-08-19"

    def initialize_profile_assistant(self):
        """
        Initialize the default Profile Assistant in the database.

        If the assistant already exists, no new document is created.
        """

        logger.info(
            "[%s] [%s] initializing profile assistant [%s]",
            ApplicationLayerLogging.REPOSITORY.value,
            LoggingComponent.PROFILE_ASSISTANT.value,
            LogEvent.STARTED.value,
        )

        try:
            existing = self.collection.find_one(
                {
                    "assistantName": self.name
                }
            )

            if existing:
                logger.info(
                    "[%s] [%s] profile assistant already initialized [%s]",
                    ApplicationLayerLogging.REPOSITORY.value,
                    LoggingComponent.PROFILE_ASSISTANT.value,
                    LogEvent.COMPLETED.value,
                )

                return {
                    "success": True,
                    "message": "Repository had already been initialized.",
                }

            assistant = {
                "_id": str(uuid.uuid4()),
                "assistantName": self.name,
                "dateOfBirth": self.date_of_birth,
                "chatHistory": [],
            }

            result = self.collection.insert_one(
                assistant
            )

            logger.info(
                "[%s] [%s] profile assistant inserted successfully [%s]",
                ApplicationLayerLogging.REPOSITORY.value,
                LoggingComponent.PROFILE_ASSISTANT.value,
                LogEvent.COMPLETED.value,
            )

            return {
                "success": True,
                "message": "Repository successfully initialized.",
            }

        except Exception as error:
            logger.exception(
                "[%s] [%s] failed to initialize profile assistant: %s [%s]",
                ApplicationLayerLogging.REPOSITORY.value,
                LoggingComponent.PROFILE_ASSISTANT.value,
                error,
                LogEvent.FAILED.value,
            )

            raise

    def retrieve_name(self):
        """Retrieve the Profile Assistant name and date of birth from the database."""

        logger.info(
            "[%s] [%s] retrieving profile assistant name [%s]",
            ApplicationLayerLogging.REPOSITORY.value,
            LoggingComponent.PROFILE_ASSISTANT.value,
            LogEvent.STARTED.value,
        )

        try:
            result = self.collection.find_one(
                {},
                {
                    "_id": 0,
                    "assistantName": 1,
                },
            )

            assistant_name = result.get("assistantName")
            assistant_dob = result.get("dateOfBirth")
            

            logger.info(
                "[%s] [%s] profile assistant name retrieved successfully [%s]",
                ApplicationLayerLogging.REPOSITORY.value,
                LoggingComponent.PROFILE_ASSISTANT.value,
                LogEvent.COMPLETED.value,
            )

            return {
                "success": True,
                "assistName": assistant_name,
                "dateOfBirth": assistant_dob
            }

        except Exception as error:
            logger.exception(
                "[%s] [%s] failed to retrieve profile assistant name: %s [%s]",
                ApplicationLayerLogging.REPOSITORY.value,
                LoggingComponent.PROFILE_ASSISTANT.value,
                error,
                LogEvent.FAILED.value,
            )

            raise

    def initialize_new_chat_session(self):
        """Create and persist a new Profile Assistant chat session."""

        logger.info(
            "[%s] [%s] initializing new chat session [%s]",
            ApplicationLayerLogging.REPOSITORY.value,
            LoggingComponent.PROFILE_ASSISTANT.value,
            LogEvent.STARTED.value,
        )

        try:
            session_id = str(uuid.uuid4())

            new_session = {
                "_id": session_id,
                "history": [],
            }

            result = self.collection.update_one(
                {
                    "assistantName": self.name
                },
                {
                    "$push": {
                        "chatHistory": new_session
                    }
                },
            )

            if result.matched_count == 0:

                logger.warning(
                    "[%s] [%s] profile assistant not initialized [%s]",
                    ApplicationLayerLogging.REPOSITORY.value,
                    LoggingComponent.PROFILE_ASSISTANT.value,
                    LogEvent.FAILED.value,
                )

                return {
                    "success": False,
                    "message": (
                        "Profile assistant has not been initialized."
                    ),
                }

            logger.info(
                "[%s] [%s] new chat session initialized successfully [%s]",
                ApplicationLayerLogging.REPOSITORY.value,
                LoggingComponent.PROFILE_ASSISTANT.value,
                LogEvent.COMPLETED.value,
            )

            return {
                "success": True,
                "message": (
                    "New chat session initialized successfully."
                ),
                "sessionId": session_id,
            }

        except Exception as error:
            logger.exception(
                "[%s] [%s] failed to initialize chat session: %s [%s]",
                ApplicationLayerLogging.REPOSITORY.value,
                LoggingComponent.PROFILE_ASSISTANT.value,
                error,
                LogEvent.FAILED.value,
            )

            raise

    def add_chat_data(
        self,
        chat_id,
        chat_type,
        text,
    ):
        """Persist a request or response in an existing chat session."""

        logger.info(
            "[%s] [%s] adding chat data [%s]",
            ApplicationLayerLogging.REPOSITORY.value,
            LoggingComponent.PROFILE_ASSISTANT.value,
            LogEvent.STARTED.value,
        )

        try:
            if not chat_id:
                raise ValueError(
                    "Chat ID is required to add chat data."
                )

            if not isinstance(chat_type, ChatType):
                raise ValueError(
                    "Invalid chat type passed."
                )

            if not text or not text.strip():
                raise ValueError(
                    "Text cannot be empty."
                )

            timestamp = (
                datetime.now()
                .astimezone()
                .isoformat()
            )

            if chat_type == ChatType.REQUEST:

                data = {
                    "request_id": str(uuid.uuid4()),
                    "request": text.strip(),
                    "requestTime": timestamp,
                }

            elif chat_type == ChatType.RESPONSE:

                data = {
                    "response_id": str(uuid.uuid4()),
                    "response": text.strip(),
                    "responseTime": timestamp,
                }

            else:
                raise ValueError(
                    f"Unsupported chat type: {chat_type}"
                )

            result = self.collection.update_one(
                {
                    "chatHistory._id": chat_id
                },
                {
                    "$push": {
                        "chatHistory.$.history": data
                    }
                },
            )

            if result.matched_count == 0:

                logger.warning(
                    "[%s] [%s] chat session not found [%s]",
                    ApplicationLayerLogging.REPOSITORY.value,
                    LoggingComponent.PROFILE_ASSISTANT.value,
                    LogEvent.FAILED.value,
                )

                raise ValueError(
                    f"Chat session '{chat_id}' was not found."
                )

            logger.info(
                "[%s] [%s] chat data added successfully [%s]",
                ApplicationLayerLogging.REPOSITORY.value,
                LoggingComponent.PROFILE_ASSISTANT.value,
                LogEvent.COMPLETED.value,
            )

            return data

        except Exception as error:

            logger.exception(
                "[%s] [%s] failed to add chat data: %s [%s]",
                ApplicationLayerLogging.REPOSITORY.value,
                LoggingComponent.PROFILE_ASSISTANT.value,
                error,
                LogEvent.FAILED.value,
            )

            raise