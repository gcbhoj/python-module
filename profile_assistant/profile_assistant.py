import re
import os

from utils.file_system_reader import FileSystemReader

from profile_assistant.const_enums import ExitInformation
from repository.resume_reader import ResumeReader
from repository.profile_assistant_repo import ProfileAssistantRepo

from profile_assistant.const_enums import NormalGreetings, TimedGreeting, BotsInformation, DateTimeInformation, SpeakerCommand

from profile_assistant.greetings_manager import GreetingsManager
from profile_assistant.profile_assistant_manager import ProfileAssistantManager
from profile_assistant.question_analyzer import SentenceAnalyzer
from profile_assistant.speaker import Speaker


class ProfileAssistant:

    def __init__(self):
        self.name = "Bahire"
        self.date_of_birth = "2026-08-19"
        self.final_query = [e.value for e in ExitInformation]
        self.is_final_query = False

        # Toggle flag
        self.is_speak_enabled = os.getenv("DEV_ENV") == "development"

        # Managers
        self.resume_reader = ResumeReader()
        self.greeting_manager = GreetingsManager()
        self.myAssistant = ProfileAssistantManager()
        self.question_analyzer = SentenceAnalyzer()
        self.speaker = Speaker()
        
        self.repo = ProfileAssistantRepo()

    def run(self):
        """Main entry point wrapping start mode inside a match/case switch."""
        match self.is_speak_enabled:
            case True:
                print("[System]: Starting ProfileAssistant in Voice Mode...")
                self._start_voice_mode()

            case False:
                print("[System]: Starting ProfileAssistant in Text Mode...")
                self._start_text_mode()

            case _:
                self._start_text_mode()

    def _format_reply(self, reply):
        """Normalizes reply strings/lists into speech and console safe strings."""
        if isinstance(reply, (list, tuple)):
            return ". ".join(str(item) for item in reply)
        return str(reply) if reply else ""

    def _start_voice_mode(self):
        """Mode 1: Text output + Audio output."""
        profile_alias = self.resume_reader.get_alias()
        timed = self.greeting_manager.generate_timed_greeting()
        startup = self.greeting_manager.generate_startup_greeting(
            self.name, profile_alias
        )

        print(f"{timed}\n{startup}")
        self.speaker.speak(f"{timed}. {startup}")

        while not self.is_final_query:
            user_input = input("You: ").strip()
            if not user_input:
                continue

            normalized_input = self._normalize_input(user_input)

            if normalized_input in self.final_query:
                self.is_final_query = True
                exit_msg = self.greeting_manager.generate_exit_greeting()
                print(f"{self.name}: Goodbye!\n{exit_msg}")
                self.speaker.speak(f"Goodbye! {exit_msg}")
                break

            reply = self._process_query(normalized_input)
            if reply:
                clean_reply = self._format_reply(reply)
                print(f"{self.name}: {clean_reply}")
                self.speaker.speak(clean_reply)

    def _start_text_mode(self):
        """Mode 2: Pure Text mode (No speaker calls)."""
        profile_alias = self.resume_reader.get_alias()
        timed = self.greeting_manager.generate_timed_greeting()
        startup = self.greeting_manager.generate_startup_greeting(
            self.name, profile_alias
        )

        print(f"{timed}\n{startup}")

        while not self.is_final_query:
            user_input = input("You: ").strip()
            if not user_input:
                continue

            normalized_input = self._normalize_input(user_input)

            if normalized_input in self.final_query:
                self.is_final_query = True
                print(
                    f"{self.name}: Goodbye!\n{self.greeting_manager.generate_exit_greeting()}"
                )
                break

            reply = self._process_query(normalized_input)
            if reply:
                clean_reply = self._format_reply(reply)
                print(f"{self.name}: {clean_reply}")

    def _process_query(self, normalized_input: str):
        """Core logic handler shared across both modes."""
        user_input_analysis = self.question_analyzer.analyse_user_input(
            normalized_input
        )
        enum_category = user_input_analysis.get("category")
        intent = user_input_analysis.get("intent")

        match enum_category:
            case NormalGreetings.__name__:
                return self.greeting_manager.generate_normal_greeting()

            case TimedGreeting.__name__:
                return self.greeting_manager.generate_timed_greeting()

            case BotsInformation.__name__:
                return self.myAssistant.generate_bot_info_reply(
                    intent, self.name, self.date_of_birth
                )

            case DateTimeInformation.__name__:
                return self.myAssistant.generate_date_time_reply(intent)

            case SpeakerCommand.__name__:
                if intent == "ENABLE_SPEAKER":
                    self.is_speak_enabled = True
                    return "Switching to voice mode."
                else:
                    self.is_speak_enabled = False
                    return "Switching to text mode."

            case _:
                return f"Unrecognized query: {user_input_analysis}"

    @staticmethod
    def _normalize_input(user_input: str) -> str:
        if not user_input:
            return ""
        normalized = user_input.strip().lower().replace("?", "")
        return re.sub(r"\s+", " ", normalized).strip()


if __name__ == "__main__":
    assistant = ProfileAssistant()
    assistant.run()  