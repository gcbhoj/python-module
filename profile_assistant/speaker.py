import io

from gtts import gTTS


class Speaker:

    def __init__(self, lang: str = "en"):
        self.lang = lang

    def speak(self, text) -> bytes | None:
        """
        Convert text to MP3 audio and return the MP3 bytes.
        """

        if not text:
            return None

        if isinstance(text, (list, tuple)):
            text_str = ". ".join(
                str(item)
                for item in text
            )
        else:
            text_str = str(text).strip()

        if not text_str:
            return None

        try:
            audio_buffer = io.BytesIO()

            tts = gTTS(
                text=text_str,
                lang=self.lang
            )

            tts.write_to_fp(audio_buffer)

            audio_buffer.seek(0)

            return audio_buffer.getvalue()

        except Exception as error:
            raise RuntimeError(
                f"Failed to generate speech: {error}"
            ) from error