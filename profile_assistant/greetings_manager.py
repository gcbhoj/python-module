from datetime import datetime

from config.logger_config import configure_logging

from app_constants.logging_enums import ApplicationLayerLogging, LogEvent, LoggingComponent

from profile_assistant.const_enums import  TimedGreeting,NormalGreetings, ExitResponses
from profile_assistant.date_time_manager import DateTimeManager

logger = configure_logging()

class GreetingsManager:

    def __init__(self):
        self.date_time_manager = DateTimeManager()
        self.time = datetime.now()

    def generate_startup_greeting(self,assist_name: str,profile_alias: str) -> str:
        logger.info("[%s] [%s] start up greeting [%s]", 
                    ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                    LoggingComponent.GREETINGS_MANAGER.value,
                    LogEvent.STARTED.value)
        result =  (
            f"I am {assist_name}.\n"
            f"I can assist you in navigating "
            f"{profile_alias}'s profile website and resume.\n"
            f"Type q to quit this conversation."
        )
        logger.debug("[%s] [%s] start up greeting result: [%s] [%s]", 
                    ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                    LoggingComponent.GREETINGS_MANAGER.value,
                    result,
                    LogEvent.STARTED.value)
        
        return result
        
    def generate_exit_greeting(self):
        """
    Generate an appropriate exit greeting based on the current
    time of day.

    Returns:
        A time-appropriate exit greeting.
    """
        logger.info("[%s] [%s] exit greeting [%s]", 
                    ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                    LoggingComponent.GREETINGS_MANAGER.value,
                    LogEvent.STARTED.value)
        hour = self.date_time_manager.get_current_datetime().hour
        
        match hour:
            case h if 5 <= h < 12:
                result =  ExitResponses.MORNING.value
                return result
            case h if 12 <= h < 17:
                result =  ExitResponses.AFTERNOON.value
                return result
            case h if 17 <= h < 22:
                result = ExitResponses.EVENING.value
                return result
            case _:
                result =  ExitResponses.NIGHT.value                
        
        logger.debug("[%s] [%s] exit greeting result: [%s] [%s]",
                     ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                     LoggingComponent.PROFILE_ASSISTANT.value,
                     result,
                     LogEvent.COMPLETED.value)
        return result
        
    def generate_timed_greeting(self):
        """
    Generate a greeting appropriate for the current time of day.

    Returns:
        A time-appropriate greeting such as 'Good Morning',
        'Good Afternoon', 'Good Evening', or 'Good Night'.
    """
        logger.info("[%s] [%s] timed greeting [%s]", 
                    ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                    LoggingComponent.GREETINGS_MANAGER.value,
                    LogEvent.STARTED.value)
        hour = self.date_time_manager.get_current_datetime().hour

        if 5 <= hour < 12:
            result = TimedGreeting.GOOD_MORNING.value

        elif 12 <= hour < 17:
            result = TimedGreeting.GOOD_AFTERNOON.value

        elif 17 <= hour < 22:
            result = TimedGreeting.GOOD_EVENING.value

        else:
            return TimedGreeting.GOOD_NIGHT.value
        
        logger.debug("[%s] [%s] timedgreeting result: [%s] [%s]",
                     ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                     LoggingComponent.PROFILE_ASSISTANT.value,
                     result,
                     LogEvent.COMPLETED.value)
        return result
        
    def generate_normal_greeting(self):
        """
    Generate a appropriate greeting.

    Returns:
        Normal greetings like hi hello.
        TODO
        use spacy to to generate normal greetings
    """
        logger.info("[%s] [%s] normal greeting [%s]", 
                    ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                    LoggingComponent.GREETINGS_MANAGER.value,
                    LogEvent.STARTED.value)
        result =  NormalGreetings.HELLO.value
        
        logger.debug("[%s] [%s] normal greeting result: [%s] [%s]",
                     ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                     LoggingComponent.PROFILE_ASSISTANT.value,
                     result,
                     LogEvent.COMPLETED.value)
        return result
    
    