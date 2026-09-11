
from datetime import datetime
from zoneinfo import ZoneInfo


from config.logger_config import configure_logging

from app_constants.logging_enums import ApplicationLayerLogging, LogEvent, LoggingComponent

logger = configure_logging()


class DateTimeManager:
    '''  Manages date and time operations for the Profile Assistant.

    The manager uses America/Toronto as the default timezone.
    The timezone can be overridden when the class is initialized.

    TODO:
        Use the user's actual timezone instead of a fixed timezone.
    """
    '''

    def __init__(self, timezone_name="America/Toronto"):
        """
        Initialize the date and time manager.

        Args:
            timezone_name: IANA timezone name used for date and time
                calculations. Defaults to America/Toronto.
        """
        self.tz = ZoneInfo(timezone_name)

    def get_current_datetime(self) -> datetime:
        """
        Retrieve the current date and time for the configured timezone.

        Returns:
            A timezone-aware datetime object representing the current
            date and time.
        """
        
        logger.info("[%s] [%s] request for current datetime [%s]",
                    ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                    LoggingComponent.DATE_TIME_MANAGER.value,
                    LogEvent.STARTED.value)
        result =  datetime.now(self.tz)
        logger.debug("[%s] [%s] result for current datetime: [%s] [%s]",
                    ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                    LoggingComponent.DATE_TIME_MANAGER.value,
                    result,
                    LogEvent.COMPLETED.value)
        return result

    def get_current_time(self) -> str:
        """
        Retrieve the current time for the configured timezone.

        Returns:
            The current time formatted as a 12-hour clock with
            the timezone abbreviation.
            Example: '3:45 PM EDT'.
        """
        logger.info("[%s] [%s] request for current time [%s]",
                    ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                    LoggingComponent.DATE_TIME_MANAGER.value,
                    LogEvent.STARTED.value)
        result =  self.get_current_datetime().strftime(
            "%I:%M %p %Z"
        ).lstrip("0")
        
        logger.debug("[%s] [%s] result for current datetime: [%s] [%s]",
                    ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                    LoggingComponent.DATE_TIME_MANAGER.value,
                    result,
                    LogEvent.COMPLETED.value)
        return result

    def get_current_date(self) -> str:
        """
        Retrieve the current calendar date for the configured timezone.

        Returns:
            The current date formatted as 'Month DD, YYYY'.
            Example: 'August 20, 2026'.
        """
        logger.info("[%s] [%s] request for current date [%s]",
                    ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                    LoggingComponent.DATE_TIME_MANAGER.value,
                    LogEvent.STARTED.value)
        result =  self.get_current_datetime().strftime(
            "%B %d, %Y"
        )
        logger.debug("[%s] [%s] result for current date: [%s] [%s]",
                    ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                    LoggingComponent.DATE_TIME_MANAGER.value,
                    result,
                    LogEvent.COMPLETED.value)
        return result

    def get_current_day(self) -> str:
        """
        Retrieve the current day of the week for the configured timezone.

        Returns:
            The current day of the week.
            Example: 'Thursday'.
        """
        
        logger.info("[%s] [%s] request for current day [%s]",
                    ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                    LoggingComponent.DATE_TIME_MANAGER.value,
                    LogEvent.STARTED.value)
        result =  self.get_current_datetime().strftime(
            "%A"
        )
        logger.debug("[%s] [%s] result for current date: [%s] [%s]",
                    ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                    LoggingComponent.DATE_TIME_MANAGER.value,
                    result,
                    LogEvent.COMPLETED.value)
        return result

    def get_day_part(self) -> str:
        """
        Determine the current part of the day based on the configured timezone.

        The day is divided into four periods:

        - Morning: 5:00 AM to 11:59 AM
        - Afternoon: 12:00 PM to 4:59 PM
        - Evening: 5:00 PM to 9:59 PM
        - Night: 10:00 PM to 4:59 AM

        Returns:
            A string identifying the current part of the day:
            'morning', 'afternoon', 'evening', or 'night'.
        """
        logger.info("[%s] [%s] request for day part [%s]",
                    ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                    LoggingComponent.DATE_TIME_MANAGER.value,
                    LogEvent.STARTED.value)
        hour = self.get_current_datetime().hour

        if 5 <= hour < 12:
            result = "morning"
        elif 12 <= hour < 17:
            result =  "afternoon"
        elif 17 <= hour < 22:
            result =  "evening"
        else:
            result =  "night"
            
        logger.debug("[%s] [%s] result for day part: [%s] [%s]",
                    ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                    LoggingComponent.DATE_TIME_MANAGER.value,
                    result,
                    LogEvent.COMPLETED.value)
        return result