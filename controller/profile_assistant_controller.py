from flask import jsonify, request

from services.profile_assistant_services import ProfileAssistantService

class ProfileAssistantController:
    def __init__(self):
        self.service = ProfileAssistantService()
    
    def initialize_profile_assistant(self):
        return self.service.init_profile_assistant_repo()
    
    def initialize_chat(self):

        result = self.service.init_new_chat()

        return jsonify(result), 201