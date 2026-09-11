from enum import Enum


class ApplicationLayerLogging(Enum):
    CONTROLLER = "controller"
    SERVICE = "service"
    REPOSITORY = "repository"
    MIDDLEWARE = "middleware"
    PROFILE_ASSISTANT = "profile_assistant"
    SECURITY ="security"


class LoggingComponent(Enum):
    PROFILE_ASSISTANT = "profile_assistant"
    SPEAKER = "speaker"
    RESUME_READER = "resume_reader"
    GLOBAL_EXCEPTION = "global_exception"
    DATE_TIME_MANAGER = "date_time_manager"
    GREETINGS_MANAGER = "greetings_manager"
    PROFILE_ASSISTANT_MANAGER = "profile_assistant_manager"
    QUESTION_ANALYZER = "question_analyzer"
    FERNET_ENCODER = "fernet_encoder"
    ENCODING_SERVICES = "encoding_services"
    PROFILE_ASSISTANT_SERVICE = "profile_assistant_service"
    PROFILE_ASSISTANT_REPOSITORY ="profile_assistant_repository"


class LogEvent(Enum):
    STARTED = "started"
    COMPLETED = "completed"
    FAILED = "failed"
    CALLED = "called"
    INITIALIZED = "initialized"
    RECEIVED = "received"
    ERROR = "error"