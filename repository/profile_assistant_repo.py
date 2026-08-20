import uuid

from datetime import datetime

from repository.base_repo import BaseRepository

from profile_assistant.const_enums import ChatType


class ProfileAssistantRepo(BaseRepository):

    collection_name = "profile_assistant"

    def __init__(self):
        super().__init__()

        self.name = "Bahire"
        self.date_of_birth = "2026-08-19"

    def initialize_profile_assistant(self):
        """
        Initialize the default profile assistant if
        it does not already exist.
        """

        existing = self.collection.find_one(
            {"assistantName": self.name}
        )

        if existing:
            return {
            "success":True,
            "message":"Repository had already been initialized."
            }

        assistant = {
            "_id": str(uuid.uuid4()),
            "assistantName": self.name,
            "dateOfBirth": self.date_of_birth,
            "chatHistory": []
        }

        result = self.collection.insert_one(assistant)

        assistant["_id"] = result.inserted_id

        return {
            "success":True,
            "message":"Repository Successfully Initialized "
        }
        
    def retrieve_name(self):
        """Retrieves the name of the profile assistant."""

        result = self.collection.find_one(
            {},
            {"_id": 0, "assistantName": 1}
        )
        assit_name = result.get("assistantName") if result else None
        
        
        
        return {
            "success": True,
            "assistName":assit_name
        }
        
    def initialize_new_chat_session(self):
        """Create and initialize a new chat session."""

        session_id = str(uuid.uuid4())

        new_session = {
            "_id": session_id,
            "history": []
        }

        result = self.collection.update_one(
            {"assistantName": self.name},
            {
                "$push": {
                    "chatHistory": new_session
                }
            }
        )

        if result.matched_count == 0:
            return {
                "success": False,
                "message": "Profile assistant has not been initialized."
            }

        return {
            "success": True,
            "message": "New chat session initialized successfully.",
            "sessionId": session_id
        }
    
    def add_chat_data(self, chat_id, chat_type, text):

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
                "requestTime": timestamp
            }

        elif chat_type == ChatType.RESPONSE:

            data = {
                "response_id": str(uuid.uuid4()),
                "response": text.strip(),
                "responseTime": timestamp
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
            }
        )

        if result.matched_count == 0:
            raise ValueError(
                f"Chat session '{chat_id}' was not found."
            )

        return data
            
        
        

        
        