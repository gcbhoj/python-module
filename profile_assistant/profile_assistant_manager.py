import re

from datetime import datetime,date

from profile_assistant.const_enums import BotsInformation, BotsInformationResponse,DateTimeInformation ,DateTimeInformationResponse

from profile_assistant.date_time_manager import DateTimeManager

from api_calls.open_weather_map import GetCurrentWeatherData
from profile_assistant.question_analyzer import SentenceAnalyzer



class ProfileAssistantManager:
    def __init__(self):
        self.date_time_manager  = DateTimeManager()
        self.question_analyzer = SentenceAnalyzer()
        
    def generate_date_time_reply(self,intent):
        
        match intent:
            case DateTimeInformation.CURRENT_TIME.name:
                return DateTimeInformationResponse.CURRENT_TIME.value + self.date_time_manager.get_current_time()
            
            case DateTimeInformation.CURRENT_DATE.name:
                return DateTimeInformationResponse.CURRENT_DATE.value + self.date_time_manager.get_current_date()
            
            case DateTimeInformation.CURRENT_DAY.name:
                return DateTimeInformationResponse.CURRENT_DAY.value + self.date_time_manager.get_current_day()
            
            case DateTimeInformation.DAY_PART.name:
                return DateTimeInformationResponse.DAY_PART.value + self.date_time_manager.get_current_time()
            
            case _:
                return self.date_time_manager.get_current_time()
        
        
        
        
    def generate_bot_info_reply(self, intent, bots_name, date_of_birth):
        
        match intent:
            case BotsInformation.BOTS_NAME.name:
                return BotsInformationResponse.BOTS_NAME.value + bots_name
            
            case BotsInformation.BOTS_PURPOSE.name:
                return BotsInformationResponse.BOTS_PURPOSE.value
            
            case BotsInformation.BOTS_CAPABILITIES.name:
                return BotsInformationResponse.BOTS_CAPABILITIES.value
            
            case BotsInformation.BOTS_HEALTH.name:
                return BotsInformationResponse.BOTS_HEALTH.value

            
            case BotsInformation.BOTS_DATE_OF_BIRTH.name:
                return BotsInformationResponse.BOTS_DATE_OF_BIRTH.value + date_of_birth
            
            case BotsInformation.BOTS_AGE.name:
                return BotsInformationResponse.BOTS_AGE.value + self._calculate_age(date_of_birth)
            
            case _:
                return "Much more to follow "
        
        
    
    
    def is_normal_greeting_user_input(self, user_input):
        
        analyzer = self.question_analyzer.analyse_user_input(user_input)

        intent = analyzer["category"]

        if intent == "NormalGreetings":
            return True
        
        return False
    
    def is_timed_greeting_user_input(self, user_input):
        analyzer = self.question_analyzer.analyse_user_input(user_input)

        intent = analyzer["category"]

        if intent == "NormalGreetings":
            return False
        
        return True
    
    def _retrieve_current_weather_data(self):
        forecaster = GetCurrentWeatherData()
        return forecaster.get_weather_report()
    
    def _calculate_age(self, date_of_birth) -> str:
        # 1. Parse string to date object if needed
        if isinstance(date_of_birth, str):
            try:
                date_of_birth = datetime.strptime(
                    date_of_birth, "%Y-%m-%d"
                ).date()
            except ValueError:
                return "recently created"

        today = date.today()

        # 2. Check for future creation date (e.g. today is before DOB)
        if date_of_birth > today:
            days_until = (date_of_birth - today).days
            if days_until == 1:
                return "1 day away from launch"
            return f"{days_until} days away from launch"

        # 3. Calculate age in years
        age_years = today.year - date_of_birth.year
        if (today.month, today.day) < (date_of_birth.month, date_of_birth.day):
            age_years -= 1

        # 4. If under 1 year old, return age in days or months
        if age_years < 1:
            days = (today - date_of_birth).days
            if days < 30:
                return f"{days} day{'s' if days != 1 else ''} old"

            months = (today.year - date_of_birth.year) * 12 + (
                today.month - date_of_birth.month
            )
            return f"{months} month{'s' if months != 1 else ''} old"

        return f"{age_years} year{'s' if age_years != 1 else ''} old"
        