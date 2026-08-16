import re

from datetime import datetime,date

from profile_assistant.const_enums import BotsInformation, BotsInformationResponse

from profile_assistant.date_time_manager import DateTimeManager

from api_calls.open_weather_map import GetCurrentWeatherData
from profile_assistant.question_analyzer import SentenceAnalyzer



class ProfileAssistantManager:
    def __init__(self):
        self.date_time_manager  = DateTimeManager()
        self.question_analyzer = SentenceAnalyzer()
        
        
        
    def generate_bot_info_reply(self, intent, bots_name, date_of_birth):
        
        print(intent)
        
        match intent:
            case BotsInformation.BOTS_NAME.name:
                return BotsInformationResponse.BOTS_NAME.value + bots_name
            
            case BotsInformation.BOTS_PURPOSE.name:
                return BotsInformationResponse.BOTS_PURPOSE.value
            
            case BotsInformation.BOTS_CAPABILITIES.name:
                return BotsInformationResponse.BOTS_CAPABILITIES.value
            
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
    
    def _calculate_age(self, date_of_birth):
        if isinstance(date_of_birth, str):
            date_of_birth = datetime.strptime(
                date_of_birth,
                "%Y-%m-%d"
            ).date()

        today = date.today()

        age = today.year - date_of_birth.year

        if (
            (today.month, today.day)
            < (date_of_birth.month, date_of_birth.day)
        ):
            age -= 1

        return age
        