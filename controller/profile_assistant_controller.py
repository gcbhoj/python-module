from flask import jsonify, request

from config.logger_config import configure_logging

from services.encoding_services import EncodingServices

from app_constants.logging_enums import ApplicationLayerLogging, LogEvent, LoggingComponent



from services.profile_assistant_services import ProfileAssistantService

logger = configure_logging()
class ProfileAssistantController:

    def __init__(self):
        self.service = ProfileAssistantService()
        self.encoding_service = EncodingServices()
        

    def initialize_profile_assistant(self):
        """Initializes Profile Assistant Repository."""

        logger.info(
            "[%s] [%s] initializing profile assistant [%s]",
            ApplicationLayerLogging.CONTROLLER.value,
            LoggingComponent.PROFILE_ASSISTANT.value,
            LogEvent.STARTED.value,
        )

        result = self.service.init_profile_assistant_repo()

        logger.info(
            "[%s] [%s] profile assistant initialization completed [%s]",
            ApplicationLayerLogging.CONTROLLER.value,
            LoggingComponent.PROFILE_ASSISTANT.value,
            LogEvent.COMPLETED.value,
        )

        return result
    
    
    def get_name(self):
        """Retrieving name of the profile assistant"""
        logger.info(
            "[%s] [%s] retrieving profile assistant name  [%s]",
            ApplicationLayerLogging.CONTROLLER.value,
            LoggingComponent.PROFILE_ASSISTANT.value,
            LogEvent.STARTED.value,
        )
        
        result = self.service.fetch_name()
        logger.info(
            "[%s] [%s] profile assistant initialization completed [%s]",
            ApplicationLayerLogging.CONTROLLER.value,
            LoggingComponent.PROFILE_ASSISTANT.value,
            LogEvent.COMPLETED.value,
        )
        return jsonify(result),200

    def initialize_chat(self):
        """ Initializing a new chat with profile assistant"""
        logger.info("[%s] [%s] initializing new chat with profile assistant [%s]", 
                    ApplicationLayerLogging.CONTROLLER.value,
                    LoggingComponent.PROFILE_ASSISTANT.value,
                    LogEvent.STARTED.value)

        result = self.service.init_new_chat()
        logger.info("[%s] [%s] initializing new chat with profile assistant  completed [%s]",
                    ApplicationLayerLogging.CONTROLLER.value,
                    LoggingComponent.PROFILE_ASSISTANT.value,
                    LogEvent.COMPLETED.value)

        return jsonify(result), 201
    
    def enable_voice(self):
        '''Enabling voice chat with profile assistant'''
        logger.info("[%s] [%s] enabling voice chat [%s]", 
                    ApplicationLayerLogging.CONTROLLER.value,
                    LoggingComponent.PROFILE_ASSISTANT.value,
                    LogEvent.STARTED.value)
        result = self.service.enable_speech_mode()
        logger.info("[%s] [%s] enabling voice chat completed [%s]",
                    ApplicationLayerLogging.CONTROLLER.value,
                    LoggingComponent.PROFILE_ASSISTANT.value,
                    LogEvent.COMPLETED.value)
        return jsonify(result), 200
    
    def disable_voice(self):
        '''Disabling voice chat with profile assistant'''
        logger.info("[%s] [%s]  disabling voice chat [%s]", 
                    ApplicationLayerLogging.CONTROLLER.value,
                    LoggingComponent.PROFILE_ASSISTANT.value,
                    LogEvent.COMPLETED.value)        
        result = self.service.disable_speech_mode()
        logger.info("[%s] [%s] disabling voice chat completed [%s]",
                    ApplicationLayerLogging.CONTROLLER.value,
                    LoggingComponent.PROFILE_ASSISTANT.value,
                    LogEvent.COMPLETED.value)
        return jsonify(result), 200
    

    def start_chat(self):
        logger.info("[%s] [%s] conversation with profile assistant [%s]",
                    ApplicationLayerLogging.CONTROLLER.value,
                    LoggingComponent.PROFILE_ASSISTANT.value,
                    LogEvent.STARTED.value)

        data = request.get_json(silent=True)

        if not data:
            logger.warning("[%s] [%s] request body is missing or invalid JSON [%s]",
                           ApplicationLayerLogging.CONTROLLER.value,
                           LoggingComponent.PROFILE_ASSISTANT.value,
                           LogEvent.FAILED.value)
            return jsonify({
                "success": False,
                "message": "Request body is required."
            }), 400


        chat_id = data.get("chat_id")
        text = data.get("text")
        logger.debug("[%s] [%s] profile assistant received data : [%s] [%s] [%s]",
                     ApplicationLayerLogging.CONTROLLER.value,
                     LoggingComponent.PROFILE_ASSISTANT.value,
                     self.encoding_service.fernet_encoding(chat_id),
                     self.encoding_service.fernet_encoding(text),
                     LogEvent.RECEIVED.value)

        if not chat_id:
            logger.warning(
                "[%s] [%s] received data missing chat id [%s]",
                ApplicationLayerLogging.CONTROLLER.value,
                LoggingComponent.PROFILE_ASSISTANT.value,
                LogEvent.FAILED.value)
            return jsonify({
                "success": False,
                "message": "Chat ID is required."
            }), 400

        if not text or not text.strip():
            logger.warning(
                "[%s] [%s] received data missing text [%s]",
                ApplicationLayerLogging.CONTROLLER.value,
                LoggingComponent.PROFILE_ASSISTANT.value,
                LogEvent.FAILED.value)
            return jsonify({
                "success": False,
                "message": "Text cannot be empty."
            }), 400
            
        
        logger.info("[%s] [%s] service call [%s]",
                    ApplicationLayerLogging.CONTROLLER.value,
                    LoggingComponent.PROFILE_ASSISTANT.value,
                    LogEvent.CALLED.value)
        result = self.service.start_chat(
            chat_id,
            text.strip()
        )
        
        logger.info("[%s] [%s] profile assistant response : [%s] [%s] [%s]",
                    ApplicationLayerLogging.CONTROLLER.value,
                    LoggingComponent.PROFILE_ASSISTANT.value,
                    self.encoding_service.fernet_encoding(chat_id),
                    self.encoding_service.fernet_encoding(result["message"]))

        return jsonify(result), 200
    