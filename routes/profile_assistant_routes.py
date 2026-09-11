from flask import Blueprint
from flasgger import swag_from

from controller.profile_assistant_controller import ProfileAssistantController


profile_assistant_bp = Blueprint("profile_assistant", __name__)

controller = ProfileAssistantController()

@profile_assistant_bp.route("/get-name",methods=["GET"])
@swag_from("../swaggerdocs/profile_assistant/get_name.yml")
def get_name():
    return controller.get_name()
                                                 

@profile_assistant_bp.route("/init-chat", methods=["POST"])
@swag_from("../swaggerdocs/profile_assistant/initialize_new_chat.yml")
def initialize_chat():
    return controller.initialize_chat()

@profile_assistant_bp.route("/enable-voice", methods=["GET"])
@swag_from("../swaggerdocs/profile_assistant/enable_voice.yml")
def enable_voice():
    return controller.enable_voice()

@profile_assistant_bp.route("/disable-voice", methods=["GET"])
@swag_from("../swaggerdocs/profile_assistant/disable_voice.yml")
def disable_voice():
    return controller.disable_voice()

@profile_assistant_bp.route("/post-query", methods=["POST"])
@swag_from("../swaggerdocs/profile_assistant/start_chat.yml")
def start_chat():
    return controller.start_chat()