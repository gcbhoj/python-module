import re

from datetime import datetime,date

from profile_assistant.const_enums import TimedGreeting,NormalGreetings,EducationConst,ProjectsConst,ContactConst,ExitResponses,ConstantQuestions,ConstantAnswers

from profile_assistant.date_time_manager import DateTimeManager

from api_calls.open_weather_map import GetCurrentWeatherData



class ProfileAssistantManager:
    def __init__(self):
        self.date_time_manager  = DateTimeManager()
    
    
    def is_greeting_user_input(self, user_input):

        intent = self._match_intent(user_input)

        return intent == "greeting"
    
    def is_constant_question(self,user_input):
        
        if user_input in ConstantQuestions:
            return True
        return False
    
    def generate_response_constant_question(self, question, bots_name,profile_owner, location,email_contact,github_link,linkedin_link):
        
        if question == ConstantQuestions.BOTS_NAME.value:
            return ConstantAnswers.BOTS_NAME.value + bots_name
        
        elif question == ConstantQuestions.BOTS_PURPOSE.value:
            return ConstantAnswers.BOTS_PURPOSE.value
        
        elif question == ConstantQuestions.BOTS_CAPABILITIES.value:
            return ConstantAnswers.BOTS_CAPABILITIES.value
        
        elif question ==  ConstantQuestions.DEVELOPERS_NAME.value:
            return ConstantAnswers.DEVELOPERS_NAME.value + profile_owner
        
        elif question == ConstantQuestions.PROFILE_NAME.value:
            return ConstantAnswers.PROFILE_NAME.value + profile_owner
        
        elif question == ConstantQuestions.PROFILE_ALIAS.value:
            return ConstantAnswers.PROFILE_ALIAS.value + profile_owner
        
        elif question == ConstantQuestions.CURRENT_TIME.value:
            return ConstantAnswers.CURRENT_TIME.value + self.date_time_manager.get_current_time()
        
        elif question == ConstantQuestions.CURRENT_DATE.value:
            return ConstantAnswers.CURRENT_DATE + self.date_time_manager.get_current_date()
        
        elif question == ConstantQuestions.CURRENT_LOCATION.value:
            return ConstantAnswers.CURRENT_LOCATION + location
        
        elif question == ConstantQuestions.CURRENT_WEATHER.value:
            return ConstantAnswers.CURRENT_WEATHER.value + self._retrieve_current_weather_data()
            
        
        elif question == ConstantQuestions.WEBSITE.value:
            return ConstantAnswers.WEBSITE.value
        
        elif question == ConstantQuestions.CONTACT.value:
            return ConstantAnswers.CONTACT.value + email_contact
        
        elif question ==  ConstantQuestions.GITHUB.value:
            return ConstantAnswers.GITHUB.value + github_link
        
        elif question == ConstantQuestions.LINKEDIN.value:
            return ConstantAnswers.LINKEDIN.value + linkedin_link
        
        return None
        
    
    
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
        