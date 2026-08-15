from enum import Enum


class TimedGreeting(Enum):

    GOOD_MORNING = "good morning"
    GOOD_AFTERNOON = "good afternoon"
    GOOD_EVENING = "good evening"
    GOOD_NIGHT = "good night"
    
class NormalGreetings(Enum):
    HI = "hi",
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
    BOTS_NAME ="what is your name"
    BOTS_PURPOSE = "what can you do"
    BOTS_CAPABILITIES = "what can you help me with"
    BOTS_DATE_OF_BITRH = "what is your date of birth"
    BOTS_AGE = "how old are you"
    
class BotsInformationResponse(Enum):
        # Assistant

    BOTS_NAME = "My name is "
    BOTS_PURPOSE = ("I am currently in my first version, so my capabilities are "
        "limited. I can describe my developer's resume and help you "
        "navigate through my developer's website.")
    BOTS_CAPABILITIES = ("I can describe my developer's resume and help you "
        "navigate through my developer's website.")
    
class DeveloperInformation(Enum):
        # Developer / Profile Owner
    DEVELOPERS_NAME = "what is your developer's name"
    PROFILE_NAME = "whose profile is this"
    PROFILE_ALIAS = "what is the profile owner's name"
    
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
    