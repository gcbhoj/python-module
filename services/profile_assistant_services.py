from repository.profile_assistant_repo import ProfileAssistantRepo

from profile_assistant.profile_assistant import ProfileAssistant
class ProfileAssistantService:
    def __init__(self):
        self.repo = ProfileAssistantRepo()
        self.profile_assistant = ProfileAssistant()
        
    
    def init_profile_assistant_repo(self):
        
        return self.repo.initialize_profile_assistant()
    
    
    def init_new_chat(self):
        return self.repo.initialize_new_chat_session()
    
    def enable_speech_mode(self):
        return self.profile_assistant.enable_voice()
    
    def disable_speech_mode(self):
        return self.profile_assistant.disable_voice()
    
    def start_conversation(self, chat_id, chat_type, text):
        return None
        