from enum import Enum
from sentence_transformers import SentenceTransformer,util
from profile_assistant.const_enums import TimedGreeting,NormalGreetings,EducationConst,ProjectsConst,ContactConst,ExitResponses,ConstantQuestions,ConstantAnswers


class SentenceAnalyzer:
    
    def __int__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.bots_information = [q.value for q in ]
    
    def analyse_user_input(self, user_input):