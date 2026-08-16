import io
from gtts import gTTS
from IPython.display import Audio, display


class Speaker:

    def __init__(self, lang: str = "en"):
        self.lang = lang

    def speak(self, text):
        """Generates speech and renders an in-browser audio player in Jupyter."""
        if not text:
            return

        # Convert list/tuple structures into a continuous string
        if isinstance(text, (list, tuple)):
            text_str = ". ".join(str(item) for item in text)
        else:
            text_str = str(text)

        try:
            # Generate speech in memory
            fp = io.BytesIO()
            tts = gTTS(text=text_str, lang=self.lang)
            tts.write_to_fp(fp)
            fp.seek(0)

            # Render inline Jupyter audio element and autoplay
            display(Audio(fp.read(), autoplay=True))
        except Exception as e:
            print(f"[Warning] Could not render audio: {e}")