from enum import Enum


class ExitInformation(Enum):
    Q ="q"
    EXIT = "exit"
    BYE = "bye"
class TimedGreeting(Enum):

    GOOD_MORNING = "good morning"
    GOOD_AFTERNOON = "good afternoon"
    GOOD_EVENING = "good evening"
    GOOD_NIGHT = "good night"
    
class NormalGreetings(Enum):
    HI = "hi"
    HELLO = "hello"
    HEY = "hey"
    GREETING = "greeting"
    
class EducationConst(Enum):
    EDUCATION = "education"
    SCHOOL = "school"
    DEGREE = "degree"
    
class ExperienceConst(Enum):
    EXPERIENCE ="experience"
    WORK ="work"
    JOB = "job"
    WEB_DEVELOPMENT = "web development"
    
    
class ProjectsConst(Enum):
    PROJECT="project"
    CODE ="code"
    SOFTWARE = "software"
    
class ContactConst(Enum):
    CONTACT="contact"
    EMAIL ="email"
    PHONE ="phone"
    
class ExitResponses(Enum):
    MORNING = "Have a wonderful day !"
    AFTERNOON = "Have a Nice day !"
    EVENING = "ENJOY rest of the day !"
    NIGHT = "Good Night"
    
class BotsInformation(Enum):    
        # Assistant
    BOTS_NAME =["what is your name", "who are you", "your name"]
    BOTS_PURPOSE = [
        "what is your purpose",
        "purpose",
        "what do you do",
        "why were you built",
    ]
    BOTS_CAPABILITIES = [
        "what can you do",
        "capabilities",
        "what are your features",
        "why were you built",
    ]
    BOTS_DATE_OF_BIRTH = "what is your date of birth"
    BOTS_AGE = "how old are you"
    
class BotsInformationResponse(Enum):
        # Assistant

    BOTS_NAME = "My name is "
    BOTS_PURPOSE = [
        "I'm currently in my early version, so my capabilities are focused and growing.",
        "My purpose is to showcase my developer's work and answer questions about his background.",
        "I can walk you through my developer's resume and help you navigate their portfolio website.",
        "I can provide you with current date and time",
        "I can provide you with weather statement for a specific location"
    ]
    BOTS_CAPABILITIES = ["I can describe my developer's resume and help you navigate through my developer's website."]
    BOTS_DATE_OF_BIRTH = "I Was Conceived on May 2026 and was deployed on "
    BOTS_AGE = "I am "
    
class DeveloperInformation(Enum):
    DEVELOPERS_NAME = "what is your developer's name who created you who built you who developed you"
    PROFILE_NAME = "whose profile is this who does this profile belong to"
    PROFILE_ALIAS = "what is the profile owner's name who owns this profile"
    
class DeveloperInformationResponse(Enum):
        # Developer / Profile Owner
    DEVELOPERS_NAME = "My developer's name is "
    PROFILE_NAME = "This profile belongs to "
    PROFILE_ALIAS = "The owner of this profile is "
    
class DateTimeInformation(Enum):
        # Time / Date
    CURRENT_TIME = "what is the current time"
    CURRENT_DATE = "what is the current date"
    CURRENT_DAY = "what day is it"
    
class DateTimeInformationResponse(Enum):
        # Time / Date
    CURRENT_TIME = "The current time is "
    CURRENT_DATE = "Today's date is "
    CURRENT_DAY = "Today is "
    
class GeographicInformation(Enum):
        # Location
    CURRENT_LOCATION = "where are you located"
    # Weather
    CURRENT_WEATHER = "what is current weather"
    
class GeographicInformationResponse(Enum):
        # Location
    CURRENT_LOCATION = "The current location is "    
        # Weather
    CURRENT_WEATHER = "The weather looks like following in Brampton Ontario"
    
class ProfileInformation(Enum):
        # Application
    WEBSITE = "what is this website"
    CONTACT = "wow can i contact you"
    GITHUB = "what is your github"
    LINKEDIN = "what is your linkedin"

    # Conversation
    HELP = "help"
    
class ProfileInformationResponse(Enum):
    # Application / Website

    WEBSITE = (
        "This is a demo website created to showcase "
        "my developer's skills, experience, and projects."
    )

    CONTACT = "You can contact my developer through "

    GITHUB = "My developer's GitHub profile is "

    LINKEDIN = "My developer's LinkedIn profile is "

    # Conversation

    HELP = (
        "How can I help you?\n"
        "You can ask me about my developer's "
        "education, experience, projects, or contact information."
    )
    