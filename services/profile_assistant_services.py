from config.logger_config import configure_logging
from profile_assistant.const_enums import ChatType
from repository.profile_assistant_repo import ProfileAssistantRepo

from profile_assistant.profile_assistant import ProfileAssistant

logger = configure_logging()
class ProfileAssistantService:
    def __init__(self):
        self.repo = ProfileAssistantRepo()
        self.profile_assistant = ProfileAssistant()
        
    
    def init_profile_assistant_repo(self):
        logger.info("Service call to initialize profile assistant repository. Calling Repo..")
        
        return self.repo.initialize_profile_assistant()
    
    def fetch_name(self):
        return self.repo.retrieve_name()
    
    
    def init_new_chat(self):
        logger.info("Service call to initialize new chat with profile assistant. Calling Repo...")
        return self.repo.initialize_new_chat_session()
    
    
    def enable_speech_mode(self):
        logger.info("Service call to enable speech mode. Calling Profile Assistant")
        return self.profile_assistant.enable_voice()
    
    def disable_speech_mode(self):
        logger.info("Service call to disable speech mode. Calling Profile Assistant")
        return self.profile_assistant.disable_voice()
    
    def start_chat(self, chat_id, text):
        logger.info("Profile Assistant conversation service layer. Service layer initialized")
        if not chat_id:
            logger.warning("Profile Assistant conversation service layer. Chat Id is not provided")
            
            raise ValueError("Chat ID is required to add chat data.")

        if not text or not text.strip():
            logger.warning("Profile Assistant conversation service Layer. Text is not provided")
            raise ValueError("Text cannot be empty.")
            
        logger.info("Profile Assistant Conversation Service Layer. Calling repo to add request")
            
        self.repo.add_chat_data(chat_id,ChatType.REQUEST,text)
        logger.info("Profile Assistant conversation service layer. Calling Profile Assistant...")
        result = self.profile_assistant.start(text)
        logger.info("Profile Assistant conversation service layer. Calling repo to add response")
        self.repo.add_chat_data(chat_id,ChatType.RESPONSE, result.get("message"))
        logger.info("Profile Assistant conversation service layer. Response: %s",result)
        return result
            
        