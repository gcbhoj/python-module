from flask import Blueprint
from flasgger import swag_from

from controller.profile_assistant_controller import (
    ProfileAssistantController
)


profile_assistant_bp = Blueprint("profile_assistant", __name__)

controller = ProfileAssistantController()


@profile_assistant_bp.route("/init-chat", methods=["POST"])
@swag_from("../swaggerdocs/profile_assistant/initialize_new_chat.yml")
def initialize_chat():
    return controller.initialize_chat()