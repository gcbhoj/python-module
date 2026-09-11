import io

from gtts import gTTS

from config.logger_config import configure_logging
from app_constants.logging_enums import ApplicationLayerLogging, LogEvent, LoggingComponent

logger = configure_logging()
class Speaker:
    """Generates MP3 speech from text using Google Text-to-Speech."""
    def __init__(self, lang: str = "en"):
        """Initializes the speaker with the configured language."""        
        self.lang = lang
        logger.info(
            "[%s] [%s] speaker initialized with language [%s]",
            ApplicationLayerLogging.PROFILE_ASSISTANT.value,
            LoggingComponent.SPEAKER.value,
            self.lang,
        )
    def speak(self, text) -> bytes | None:
        """
        Converts the supplied text into MP3 audio bytes.

        Returns:
            bytes | None: Generated MP3 audio bytes, or None when
            no valid text is provided.
        """
        logger.info(
            "[%s] [%s] speech generation [%s]",
            ApplicationLayerLogging.PROFILE_ASSISTANT.value,
            LoggingComponent.SPEAKER.value,
            LogEvent.STARTED.value,
        )
        if not text:
            logger.warning(
                "[%s] [%s] speech generation skipped: "
                "text is empty [%s]",
                ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                LoggingComponent.SPEAKER.value,
                LogEvent.FAILED.value,
            )
            return None

        if isinstance(text, (list, tuple)):
            text_str = ". ".join(
                str(item)
                for item in text
            )
        else:
            text_str = str(text).strip()
        # Validate normalized text.
        if not text_str:
            logger.warning(
                "[%s] [%s] speech generation skipped: "
                "normalized text is empty [%s]",
                ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                LoggingComponent.SPEAKER.value,
                LogEvent.FAILED.value,
            )
            return None
        logger.debug(
            "[%s] [%s] preparing speech generation "
            "for language [%s], text length [%s]",
            ApplicationLayerLogging.PROFILE_ASSISTANT.value,
            LoggingComponent.SPEAKER.value,
            self.lang,
            len(text_str),
        )
        try:
            # Create an in-memory buffer so the MP3 does not
            # need to be written to disk.
            audio_buffer = io.BytesIO()

            tts = gTTS(
                text=text_str,
                lang=self.lang
            )
            # Write generated MP3 data into the memory buffer.
            tts.write_to_fp(audio_buffer)
            # Move the cursor back to the beginning of the buffer.
            audio_buffer.seek(0)
            # Retrieve the MP3 bytes.
            audio_bytes = audio_buffer.getvalue()
            logger.info(
                "[%s] [%s] speech generation completed "
                "with audio size [%s] bytes [%s]",
                ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                LoggingComponent.SPEAKER.value,
                len(audio_bytes),
                LogEvent.COMPLETED.value,
            )

            return audio_bytes

        except Exception as error:
            logger.exception(
                "[%s] [%s] speech generation failed: %s [%s]",
                ApplicationLayerLogging.PROFILE_ASSISTANT.value,
                LoggingComponent.SPEAKER.value,
                error,
                LogEvent.FAILED.value,
            )
            raise RuntimeError(
                f"Failed to generate speech: {error}"
            ) from error