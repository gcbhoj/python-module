import re

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

from utils.file_system_reader import FileSystemReader
from utils.generate_time_greetings import GenerateTimeGreetings

from repository.resume_reader import ResumeReader

from profile_assistant.greetings_manager import GreetingsManager
from profile_assistant.profile_assistant_manager import ProfileAssistantManager


# Ensure necessary NLTK datasets are downloaded
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("wordnet", quiet=True)


class ProfileAssistant:

    def __init__(self):

        self.name = "Bahire"
        self.final_query = "q"
        self.is_final_query = False
        self.location = None

        # Initializing resume class
        self.resume_reader = ResumeReader()
        # Initialize Greetings Manager Class
        self.greeting_manager = GreetingsManager()
        # Initializing Profile Assistant Manager
        self.myAssistant = ProfileAssistantManager()

        # Build NLTK WordNet vocabulary dynamically
        self.intent_vocab = {
            "greeting": (
                self._build_synonym_set(
                    ["hello", "greeting"]
                )
                | {
                    "hi",
                    "hey",
                    "good morning",
                    "good afternoon",
                    "good evening",
                    "good night"
                }
            ),

            "education": self._build_synonym_set(
                ["education", "school", "degree"]
            ),

            "experience": self._build_synonym_set(
                ["experience", "work", "job"]
            ),

            "projects": self._build_synonym_set(
                ["project", "code", "software"]
            ),

            "contact": self._build_synonym_set(
                ["contact", "email", "phone"]
            )
        }

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

            # Exit check
            if user_input.lower() == self.final_query.lower():

                self.is_final_query = True

                print(f"{self.name}: Goodbye! Have a great day.")

                break

            # Check for greeting
            if self.myAssistant.is_greeting_user_input(user_input):
                reply_greeting = self.greeting_manager.generate_greeting_reply(user_input)
                print(reply_greeting)
                continue


            # Process normal query
            response = self.process_query(user_input)

            print(f"{self.name}: {response}\n")




    def process_query(self, query):
        """Determine intent and format response from resume JSON."""

        intent = self._match_intent(query)

        if intent == "education":

            edu_list = self.resume.get(
                "education",
                []
            )

            res = "**Education History:**\n"

            for edu in edu_list:

                res += (
                    f"• {edu.get('type')} in "
                    f"{edu.get('faculty')} - "
                    f"{edu.get('institution')} "
                    f"({edu.get('year')})\n"
                )

            return res

        elif intent == "experience":

            work_list = self.resume.get(
                "workExperience",
                []
            )

            res = "**Work Experience:**\n"

            for work in work_list:

                res += (
                    f"• {work.get('title')} at "
                    f"{work.get('organization')}\n"
                )

            return res

        elif intent == "projects":

            demos = self.resume.get(
                "demos",
                [{}]
            )[0].get(
                "categories",
                []
            )

            res = "**Featured Projects:**\n"

            for category in demos:

                for project in category.get(
                    "projects",
                    []
                ):

                    res += (
                        f"• {project.get('title')} "
                        f"({project.get('year')})\n"
                    )

            return res

        elif intent == "contact":

            return (
                f"**Email:** "
                f"{self.resume.get('primaryEmail')}\n"
                f"**Contact:** "
                f"{self.resume.get('contact')}\n"
                f"**GitHub:** "
                f"{self.resume.get('github')}"
            )

        return (
            "I'm not sure about that. "
            "Try asking about Bhoj's education, "
            "experience, projects, or contact info!"
        )


if __name__ == "__main__":

    assistant = ProfileAssistant()

    assistant.start()