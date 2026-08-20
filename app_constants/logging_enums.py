from enum import Enum


class ApplicationLayerLogging(Enum):
    CONTROLLER = "controller"
    SERVICE = "service"
    REPOSITORY = "repository"
    MIDDLEWARE = "middleware"
    PROFILE_ASSISTANT = "profile_assistant"


class LoggingComponent(Enum):
    PROFILE_ASSISTANT = "profile_assistant"
    SPEAKER = "speaker"
    RESUME_READER = "resume_reader"
    GLOBAL_EXCEPTION = "global_exception"
    DATE_TIME_MANAGER = "date_time_manager"
    GREETINGS_MANAGER = "greetings_manager"
    PROFILE_ASSISTANT_MANAGER = "profile_assistant_manager"


class LogEvent(Enum):
    STARTED = "started"
    COMPLETED = "completed"
    FAILED = "failed"
    CALLED = "called"
    INITIALIZED = "initialized"
    RECEIVED = "received"
    ERROR = "error"