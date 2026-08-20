from flask import jsonify, request

from config.logger_config import configure_logging

from services.profile_assistant_services import (
    ProfileAssistantService
)

logger = configure_logging()
class ProfileAssistantController:

    def __init__(self):
        self.service = ProfileAssistantService()

    def initialize_profile_assistant(self):

        return self.service.init_profile_assistant_repo()

    def initialize_chat(self):
        

        result = self.service.init_new_chat()

        return jsonify(result), 201
    
    def enable_voice(self):
        logger.info("Voice Enable End point started")
        result = self.service.enable_speech_mode()
        logger.info("Voice Enable Endpoint completed with : %s", result)
        return jsonify(result), 200
    
    def disable_voice(self):
        logger.info("Voice disable end point started")
        result = self.service.disable_speech_mode()
        logger.info("Voice disable endpoint completed with : %s", result)
        return jsonify(result), 200
    

    def start_chat(self):
        logger.info("Conversation with Profile Assistant Initialized")

        data = request.get_json(silent=True)

        if not data:
            logger.warning(
            "Profile Assistant conversation failed: "
            "request body is missing or invalid JSON."
        )
            return jsonify({
                "success": False,
                "message": "Request body is required."
            }), 400


        chat_id = data.get("chat_id")
        text = data.get("text")
        logger.info("Conversation with Profile Assistant started for chat_id=%s.",chat_id)

        logger.debug("Profile Assistant received text: %s",text)

        if not chat_id:
            logger.warning(
            "Profile Assistant conversation failed: "
            "Chat id is missing in JSON"
        )
            return jsonify({
                "success": False,
                "message": "Chat ID is required."
            }), 400

        if not text or not text.strip():
            logger.warning(
            "Profile Assistant conversation failed: "
            "request body is missing text field."
        )
            return jsonify({
                "success": False,
                "message": "Text cannot be empty."
            }), 400
            
        
        logger.info("Conversation with Profile Assistant. Service Call started")
        result = self.service.start_chat(
            chat_id,
            text.strip()
        )
        
        logger.info("Conversation with Profile Assistant response: %s", result)

        return jsonify(result), 200
    