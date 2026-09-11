from flask import jsonify

from config.logger_config import configure_logging
from app_constants.logging_enums import ApplicationLayerLogging, LogEvent, LoggingComponent

logger = configure_logging()

def register_error_handlers(app):

    @app.errorhandler(ValueError)
    def handle_value_error(error):
        logger.error("[%s] [%s] value error occurred: [%s] [%s]",
                     ApplicationLayerLogging.MIDDLEWARE.value,
                     LoggingComponent.GLOBAL_EXCEPTION.value,
                     str(error),
                     LogEvent.ERROR.value)
        return jsonify({
            "success": False,
            "message": str(error)
        }), 400


    @app.errorhandler(FileNotFoundError)
    def handle_file_error(error):
        logger.error("[%s] [%s] file not found error occurred: [%s] [%s]",
                     ApplicationLayerLogging.MIDDLEWARE.value,
                     LoggingComponent.GLOBAL_EXCEPTION.value,
                     str(error),
                     LogEvent.ERROR.value)
        return jsonify({
            "success": False,
            "message": str(error)
        }), 404


    @app.errorhandler(IOError)
    def handle_io_error(error):
        logger.error("[%s] [%s] input output error occurred: [%s] [%s]",
                     ApplicationLayerLogging.MIDDLEWARE.value,
                     LoggingComponent.GLOBAL_EXCEPTION.value,
                     str(error),
                     LogEvent.ERROR.value)
        return jsonify({
            "success": False,
            "message": str(error)
        }), 500


    @app.errorhandler(Exception)
    def handle_exception(error):
        logger.error("[%s] [%s] unknown exception occurred: [%s] [%s]",
                     ApplicationLayerLogging.MIDDLEWARE.value,
                     LoggingComponent.GLOBAL_EXCEPTION.value,
                     str(error),
                     LogEvent.ERROR.value)
        return jsonify({
            "success": False,
            "message": str(error)
        }), 500