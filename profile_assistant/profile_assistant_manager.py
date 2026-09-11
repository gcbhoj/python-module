from datetime import date, datetime

from config.logger_config import configure_logging

from app_constants.logging_enums import (
    ApplicationLayerLogging,
    LogEvent,
    LoggingComponent,
)

from profile_assistant.const_enums import (
    BotsInformation,
    BotsInformationResponse,
    DateTimeInformation,
    DateTimeInformationResponse,
)

from profile_assistant.date_time_manager import DateTimeManager
from profile_assistant.question_analyzer import SentenceAnalyzer

from repository.profile_assistant_repo import ProfileAssistantRepo

from api_calls.open_weather_map import GetCurrentWeatherData


logger = configure_logging()


class ProfileAssistantManager:
    """
    Manages Profile Assistant operations including date/time responses,
    bot information, greeting classification, weather information,
    and assistant age calculation.
    """

    def __init__(self):
        """
        Initialize the Profile Assistant Manager and its dependencies.
        """

        logger.info(
            "[%s] [%s] profile assistant manager initialization [%s]",
            ApplicationLayerLogging.PROFILE_ASSISTANT.value,
            LoggingComponent.PROFILE_ASSISTANT.value,
            LogEvent.STARTED.value,
        )

        self.date_time_manager = DateTimeManager()
        self.question_analyzer = SentenceAnalyzer()
        self.repo = ProfileAssistantRepo()

        logger.debug(
            "[%s] [%s] profile assistant manager initialized [%s]",
            ApplicationLayerLogging.PROFILE_ASSISTANT.value,
            LoggingComponent.PROFILE_ASSISTANT.value,
            LogEvent.COMPLETED.value,
        )
    # ============================================================
    # RETRIEVE NAME AND DATE OF BIRTH
    # ============================================================
    
    def retrieve_name_dob(self):
        logger.info("[%s] [%s] retrieving assistant's name [%s]",
                    ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                    LoggingComponent.PROFILE_ASSISTANT_MANAGER.value,
                    LogEvent.STARTED.value )
        logger.info("[%s] [%s] retrieving assistant's name [%s]",
                    ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                    LoggingComponent.PROFILE_ASSISTANT_REPOSITORY.value,
                    LogEvent.CALLED.value )
        result = self.repo.retrieve_name();
        logger.info("[%s] [%s] retrieving assistant's name [%s]",
                    ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                    LoggingComponent.PROFILE_ASSISTANT_REPOSITORY.value,
                    LogEvent.COMPLETED.value )
        
        return result    

    # ============================================================
    # DATE / TIME
    # ============================================================

    def generate_date_time_reply(self, intent) -> str:
        """
        Generate a response for a date and time related user request.

        Args:
            intent: Date/time intent identified by the question analyzer.

        Returns:
            A formatted response containing the requested date/time
            information.
        """

        logger.info(
            "[%s] [%s] date/time reply generation started for intent [%s] [%s]",
            ApplicationLayerLogging.PROFILE_ASSISTANT.value,
            LoggingComponent.DATE_TIME_MANAGER.value,
            intent,
            LogEvent.STARTED.value,
        )

        match intent:

            case DateTimeInformation.CURRENT_TIME.name:
                result = (
                    DateTimeInformationResponse.CURRENT_TIME.value
                    + self.date_time_manager.get_current_time()
                )

            case DateTimeInformation.CURRENT_DATE.name:
                result = (
                    DateTimeInformationResponse.CURRENT_DATE.value
                    + self.date_time_manager.get_current_date()
                )

            case DateTimeInformation.CURRENT_DAY.name:
                result = (
                    DateTimeInformationResponse.CURRENT_DAY.value
                    + self.date_time_manager.get_current_day()
                )

            case DateTimeInformation.DAY_PART.name:
                result = (
                    DateTimeInformationResponse.DAY_PART.value
                    + self.date_time_manager.get_day_part()
                )

            case _:
                result = self.date_time_manager.get_current_time()

        logger.debug(
            "[%s] [%s] date/time reply generated: [%s] [%s]",
            ApplicationLayerLogging.PROFILE_ASSISTANT.value,
            LoggingComponent.DATE_TIME_MANAGER.value,
            result,
            LogEvent.COMPLETED.value,
        )

        return result

    # ============================================================
    # BOT INFORMATION
    # ============================================================

    def generate_bot_info_reply(
        self,
        intent,
        bots_name,
        date_of_birth,
    ) -> str:
        """
        Generate a response to a question about the Profile Assistant.

        Args:
            intent: Bot-information intent identified by the analyzer.
            bots_name: Name of the Profile Assistant.
            date_of_birth: Assistant creation date.

        Returns:
            A response appropriate for the requested bot information.
        """

        logger.info(
            "[%s] [%s] bot information reply generation started for intent [%s] [%s]",
            ApplicationLayerLogging.PROFILE_ASSISTANT.value,
            LoggingComponent.PROFILE_ASSISTANT.value,
            intent,
            LogEvent.STARTED.value,
        )

        match intent:

            case BotsInformation.BOTS_NAME.name:
                result = (
                    BotsInformationResponse.BOTS_NAME.value
                    + bots_name
                )

            case BotsInformation.BOTS_PURPOSE.name:
                result = (
                    BotsInformationResponse.BOTS_PURPOSE.value
                )

            case BotsInformation.BOTS_CAPABILITIES.name:
                result = (
                    BotsInformationResponse.BOTS_CAPABILITIES.value
                )

            case BotsInformation.BOTS_HEALTH.name:
                result = (
                    BotsInformationResponse.BOTS_HEALTH.value
                )

            case BotsInformation.BOTS_DATE_OF_BIRTH.name:
                result = (
                    BotsInformationResponse.BOTS_DATE_OF_BIRTH.value
                    + date_of_birth
                )

            case BotsInformation.BOTS_AGE.name:
                result = (
                    BotsInformationResponse.BOTS_AGE.value
                    + self._calculate_age(date_of_birth)
                )

            case _:
                result = "Much more to follow."

        logger.debug(
            "[%s] [%s] bot information reply generated: [%s] [%s]",
            ApplicationLayerLogging.PROFILE_ASSISTANT.value,
            LoggingComponent.PROFILE_ASSISTANT.value,
            result,
            LogEvent.COMPLETED.value,
        )

        return result

    # ============================================================
    # GREETING ANALYSIS
    # ============================================================

    def is_normal_greeting_user_input(self, user_input: str) -> bool:
        """
        Determine whether the supplied user input is a normal greeting.

        Args:
            user_input: User's input text.

        Returns:
            True when the input is classified as a normal greeting;
            otherwise False.
        """

        logger.info(
            "[%s] [%s] normal greeting analysis started [%s]",
            ApplicationLayerLogging.PROFILE_ASSISTANT.value,
            LoggingComponent.PROFILE_ASSISTANT.value,
            LogEvent.STARTED.value,
        )

        analyzer = self.question_analyzer.analyse_user_input(
            user_input
        )

        category = analyzer.get("category")

        result = category == "NormalGreetings"

        logger.debug(
            "[%s] [%s] normal greeting analysis result: [%s] [%s]",
            ApplicationLayerLogging.PROFILE_ASSISTANT.value,
            LoggingComponent.PROFILE_ASSISTANT.value,
            result,
            LogEvent.COMPLETED.value,
        )

        return result

    def is_timed_greeting_user_input(self, user_input: str) -> bool:
        """
        Determine whether the supplied user input is a timed greeting.

        Args:
            user_input: User's input text.

        Returns:
            True when the input is classified as a timed greeting;
            otherwise False.
        """

        logger.info(
            "[%s] [%s] timed greeting analysis started [%s]",
            ApplicationLayerLogging.PROFILE_ASSISTANT.value,
            LoggingComponent.PROFILE_ASSISTANT.value,
            LogEvent.STARTED.value,
        )

        analyzer = self.question_analyzer.analyse_user_input(
            user_input
        )

        category = analyzer.get("category")

        result = category == "TimedGreeting"

        logger.debug(
            "[%s] [%s] timed greeting analysis result: [%s] [%s]",
            ApplicationLayerLogging.PROFILE_ASSISTANT.value,
            LoggingComponent.PROFILE_ASSISTANT.value,
            result,
            LogEvent.COMPLETED.value,
        )

        return result

    # ============================================================
    # WEATHER
    # ============================================================

    def _retrieve_current_weather_data(self):
        """
        Retrieve the current weather report.

        Returns:
            The current weather report returned by the weather service.
        """

        logger.info(
            "[%s] [%s] current weather retrieval started [%s]",
            ApplicationLayerLogging.PROFILE_ASSISTANT.value,
            LoggingComponent.WEATHER.value,
            LogEvent.STARTED.value,
        )

        forecaster = GetCurrentWeatherData()

        result = forecaster.get_weather_report()

        logger.debug(
            "[%s] [%s] current weather retrieved: [%s] [%s]",
            ApplicationLayerLogging.PROFILE_ASSISTANT.value,
            LoggingComponent.WEATHER.value,
            result,
            LogEvent.COMPLETED.value,
        )

        return result

    # ============================================================
    # AGE CALCULATION
    # ============================================================

    def _calculate_age(self, date_of_birth) -> str:
        """
        Calculate the age of the Profile Assistant.

        The method supports both ISO date strings and Python date objects.
        If the date is in the future, the method reports the number of
        days remaining until the assistant's creation date.

        Args:
            date_of_birth: Assistant creation date as either a string
                in YYYY-MM-DD format or a date object.

        Returns:
            A human-readable age or time-until-launch description.
        """

        logger.info(
            "[%s] [%s] assistant age calculation started [%s]",
            ApplicationLayerLogging.PROFILE_ASSISTANT.value,
            LoggingComponent.PROFILE_ASSISTANT.value,
            LogEvent.STARTED.value,
        )

        # Convert string date to date object.
        if isinstance(date_of_birth, str):
            try:
                date_of_birth = datetime.strptime(
                    date_of_birth,
                    "%Y-%m-%d",
                ).date()

            except ValueError:
                logger.warning(
                    "[%s] [%s] invalid date of birth format: [%s]",
                    ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                    LoggingComponent.PROFILE_ASSISTANT.value,
                    date_of_birth,
                )

                return "recently created"

        today = date.today()

        # Future creation date.
        if date_of_birth > today:

            days_until = (
                date_of_birth - today
            ).days

            if days_until == 1:
                result = "1 day away from launch"
            else:
                result = f"{days_until} days away from launch"

            logger.debug(
                "[%s] [%s] assistant age result: [%s] [%s]",
                ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                LoggingComponent.PROFILE_ASSISTANT.value,
                result,
                LogEvent.COMPLETED.value,
            )

            return result

        # Calculate age in years.
        age_years = (
            today.year
            - date_of_birth.year
        )

        if (
            today.month,
            today.day
        ) < (
            date_of_birth.month,
            date_of_birth.day
        ):
            age_years -= 1

        # Less than one year old.
        if age_years < 1:

            days = (
                today - date_of_birth
            ).days

            if days < 30:

                result = (
                    f"{days} day"
                    f"{'s' if days != 1 else ''} old"
                )

                logger.debug(
                    "[%s] [%s] assistant age result: [%s] [%s]",
                    ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                    LoggingComponent.PROFILE_ASSISTANT.value,
                    result,
                    LogEvent.COMPLETED.value,
                )

                return result

            months = (
                (today.year - date_of_birth.year) * 12
                + (today.month - date_of_birth.month)
            )

            result = (
                f"{months} month"
                f"{'s' if months != 1 else ''} old"
            )

            logger.debug(
                "[%s] [%s] assistant age result: [%s] [%s]",
                ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                LoggingComponent.PROFILE_ASSISTANT.value,
                result,
                LogEvent.COMPLETED.value,
            )

            return result

        # One year or older.
        result = (
            f"{age_years} year"
            f"{'s' if age_years != 1 else ''} old"
        )

        logger.debug(
            "[%s] [%s] assistant age result: [%s] [%s]",
            ApplicationLayerLogging.PROFILE_ASSISTANT.value,
            LoggingComponent.PROFILE_ASSISTANT.value,
            result,
            LogEvent.COMPLETED.value,
        )

        return result