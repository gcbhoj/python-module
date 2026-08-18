from repository.profile_assistant_repo import ProfileAssistantRepo
class ProfileAssistantService:
    def __init__(self):
        self.repo = ProfileAssistantRepo()
        
    
    def init_profile_assistant_repo(self):
        
        return self.repo.initialize_profile_assistant()
    
    
        