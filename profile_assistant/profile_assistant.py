import re

from utils.file_system_reader import FileSystemReader

from profile_assistant.const_enums import ExitInformation
from repository.resume_reader import ResumeReader

from profile_assistant.const_enums import NormalGreetings, TimedGreeting, BotsInformation

from profile_assistant.greetings_manager import GreetingsManager
from profile_assistant.profile_assistant_manager import ProfileAssistantManager
from profile_assistant.question_analyzer import SentenceAnalyzer


class ProfileAssistant:

    def __init__(self):

        self.name = "Bahire"
        self.date_of_birth = "2026-08-17"
        self.final_query = [e.value for e in ExitInformation]
        self.is_final_query = False
        self.location = None

        # Initializing resume class
        self.resume_reader = ResumeReader()
        # Initialize Greetings Manager Class
        self.greeting_manager = GreetingsManager()
        # Initializing Profile Assistant Manager
        self.myAssistant = ProfileAssistantManager()
        self.question_analyzer = SentenceAnalyzer()

    def start(self):
        
        profile_alias = self.resume_reader.get_alias()
        
        initial_greeting = self.greeting_manager.generate_startup_greeting(self.name,profile_alias)
        print(f"{self.greeting_manager.generate_timed_greeting()}\n"
            f"{initial_greeting}"
            )

        while not self.is_final_query:

            user_input = input("You: ").strip()
            
            # Ignore empty input
            if not user_input:
                continue
            
            normalized_user_input = self._normalize_input(user_input)

            # Exit check
            if normalized_user_input in self.final_query:
                self.is_final_query = True
                print(f"{self.name}: Goodbye!\n"
                      f"{self.greeting_manager.generate_exit_greeting()}")
                break
            
            user_input_analysis = self.question_analyzer.analyse_user_input(normalized_user_input)
            enum_category = user_input_analysis.get("category")
            intent = user_input_analysis.get("intent")
            
            match enum_category:
                case NormalGreetings.__name__:
                    reply = self.greeting_manager.generate_normal_greeting()
                    print(f"{self.name}: {reply}.")
                                        
                case TimedGreeting.__name__:
                    reply = self.greeting_manager.generate_timed_greeting()
                    print(f"{self.name}: {reply}.")
                    
                case BotsInformation.__name__:
                    reply = self.myAssistant.generate_bot_info_reply(intent, self.name, self.date_of_birth)
                    print(f"{self.name}: {reply}.")
                case _:
                    print(user_input_analysis)
                

    @staticmethod
    def _normalize_input(user_input: str) -> str:

            if not user_input:
                return ""

            # Remove leading/trailing whitespace
            normalized = user_input.strip().lower()

            # Remove question marks
            normalized = normalized.replace("?", "")

            # Normalize multiple spaces
            normalized = re.sub(r"\s+", " ", normalized)

            return normalized.strip()







if __name__ == "__main__":

    assistant = ProfileAssistant()

    assistant.start()