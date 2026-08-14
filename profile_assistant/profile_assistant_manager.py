import re

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

from profile_assistant.const_enums import TimedGreeting,NormalGreetings,EducationConst,ProjectsConst,ContactConst

# Ensure necessary NLTK datasets are downloaded
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("wordnet", quiet=True)

class ProfileAssistantManager:
    def __init__(self):
        pass
    
    
    def is_greeting_user_input(self, user_input):

        intent = self._match_intent(
            user_input
        )

        return intent == "greeting"
    
    def _match_intent(self, user_input):
        """Tokenize user input and match against intent vocabularies."""

        cleaned = re.sub(
            r"[^a-zA-Z\s]",
            "",
            user_input.lower()
        )

        tokens = set(
            word_tokenize(cleaned)
        )

        for intent, vocab in self.intent_vocab.items():

            if tokens.intersection(vocab):

                return intent

        return None
    
    
    def _build_synonym_set(self, seed_words):
        """Use NLTK WordNet to extract synonyms for seed terms."""

        synonyms = set(seed_words)

        for word in seed_words:

            for syn in wordnet.synsets(word):

                for lemma in syn.lemmas():

                    clean_lemma = (
                        lemma.name()
                        .lower()
                        .replace("_", " ")
                    )

                    synonyms.add(clean_lemma)

        return synonyms