from datetime import datetime

from profile_assistant.const_enums import TimedGreeting,NormalGreetings


class GreetingsManager:

    def __init__(self):
        self.time = datetime.now()

    def generate_startup_greeting(self,
        assist_name: str,
        profile_alias: str
    ) -> str:

        return (
            f"Hi! I am {assist_name}.\n"
            f"I can assist you in navigating "
            f"{profile_alias}'s profile website and resume.\n"
            f"Type q to quit this conversation."
        )
        
        
    def generate_timed_greeting(self):
        hour = self.time.hour

        if 5 <= hour < 12:
            return TimedGreeting.GOOD_MORNING.value

        elif 12 <= hour < 17:
            return TimedGreeting.GOOD_AFTERNOON.value

        elif 17 <= hour < 21:
            return TimedGreeting.GOOD_EVENING.value

        else:
            return TimedGreeting.GOOD_NIGHT.value
        
    def generate_greeting_reply(self, greeting):

        if greeting in TimedGreeting:
            return self.generate_timed_greeting().value
        elif greeting in NormalGreetings:
            return greeting

        return None
        