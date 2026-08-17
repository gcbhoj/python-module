from datetime import datetime

from profile_assistant.const_enums import  TimedGreeting,NormalGreetings, ExitResponses
from profile_assistant.date_time_manager import DateTimeManager


class GreetingsManager:

    def __init__(self):
        self.date_time_manager = DateTimeManager()
        self.time = datetime.now()

    def generate_startup_greeting(self,
        assist_name: str,
        profile_alias: str
    ) -> str:

        return (
            f"I am {assist_name}.\n"
            f"I can assist you in navigating "
            f"{profile_alias}'s profile website and resume.\n"
            f"Type q to quit this conversation."
        )
        
    def generate_exit_greeting(self):
        hour = self.date_time_manager.get_current_datetime().hour
        
        match hour:
            case h if 5 <= h < 12:
                return ExitResponses.MORNING.value
            case h if 12 <= h < 17:
                return ExitResponses.AFTERNOON.value
            case h if 17 <= h < 22:
                return ExitResponses.EVENING.value
            case _:
                return ExitResponses.NIGHT.value
        
    def generate_timed_greeting(self):
        hour = self.date_time_manager.get_current_datetime().hour

        if 5 <= hour < 12:
            return TimedGreeting.GOOD_MORNING.value

        elif 12 <= hour < 17:
            return TimedGreeting.GOOD_AFTERNOON.value

        elif 17 <= hour < 22:
            return TimedGreeting.GOOD_EVENING.value

        else:
            return TimedGreeting.GOOD_NIGHT.value
        
    def generate_normal_greeting(self):
        return NormalGreetings.HELLO.value
    
    