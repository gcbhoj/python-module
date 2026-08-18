import uuid

from flasgger import Swagger
from flask import Flask,g,request,render_template
from flask_cors import CORS

from config.envconfig import PORT,DEBUG
from config.mongodb_config import connect_mongodb
from config.swagger_config import SWAGGER_CONFIG,SWAGGER_TEMPLATE
from config.logger_config import configure_logging

from middleware.error_handler import (register_error_handlers)

from controller.profile_assistant_controller import ProfileAssistantController







app = Flask(__name__,template_folder="doc")

# ============================================================
# LOGGING
# ============================================================

logger = configure_logging()

logger.info("Server Starting...")

# ============================================================
# CORS
# ============================================================
CORS(app)
# ============================================================
# REQUEST ID / CORRELATION ID
# ============================================================

@app.before_request
def start_request_tracking():

    # Use incoming request ID if provided.
    # Otherwise generate one.
    g.request_id = request.headers.get(
        "X-Request-ID",
        str(uuid.uuid4())[:8]
    )

    logger.info(
        "Started %s %s",
        request.method,
        request.path
    )


@app.after_request
def end_request_tracking(response):

    logger.info(
        "Finished request with Status Code: %s",
        response.status_code
    )

    response.headers["X-Request-ID"] = g.request_id

    return response
# ============================================================
# SWAGGER
# ============================================================

Swagger(
    app, 
    config=SWAGGER_CONFIG, 
    template=SWAGGER_TEMPLATE
    )

# ============================================================
# DB CONNECT
# ============================================================

db = connect_mongodb()


# ============================================================
# SETTING UP BASE URL
# ============================================================

BASE_URL = "/api/v1/python"

# ============================================================
# REPOSITORY / APPLICATION INITIALIZATION
# ============================================================

def initialize_application():
    """
    Initialize application-level repositories and
    required default data.
    """

    logger.info(
        "Initializing application repositories..."
    )

    profile_assistant_controller = (
        ProfileAssistantController()
    )

    profile_assistant_controller.initialize_profile_assistant()

    logger.info(
        "Profile Assistant repository initialized successfully."
    )

# ============================================================
# HOME
# ============================================================


@app.route("/")
def home():
    logger.info(
        "Home endpoint called from IP: %s",
        request.remote_addr
    )
    logger.info(
        "Following Repository Initialized: %s",
        "Profile Assistant Repo"
    )
    
    prod_url = f"{request.host_url.rstrip('/')}/api-docs"
    return render_template("index.html",prod_url=prod_url)
    
# @app.route("/debug/files")
# def debug_files():
#     import os

#     return {
#             "app_exists": os.path.exists("/app"),
#             "data_exists": os.path.exists("/app/data"),
#             "files": os.listdir("/app"),
#             "data_files": os.listdir("/app/data") if os.path.exists("/app/data") else []
#         }





# ============================================================
# ERROR HANDLERS
# ============================================================

register_error_handlers(app)

# ============================================================
# APPLICATION INITIALIZATION
# ============================================================

initialize_application()


# ============================================================
# DEVELOPMENT SERVER
# ============================================================

if __name__ == '__main__':
       app.run(
        host="0.0.0.0",
        port=PORT,
        debug=DEBUG
    )
    