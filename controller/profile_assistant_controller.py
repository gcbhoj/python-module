from services.profile_assistant_services import ProfileAssistantService

class ProfileAssistantController:
    def __init__(self):
        self.service = ProfileAssistantService()
    
    def initialize_profile_assistant(self):
        return self.service.init_profile_assistant_repo()