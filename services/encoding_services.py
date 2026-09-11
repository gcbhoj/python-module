from config.logger_config import configure_logging

from security.fernet_encoder import FernetEncoder

from app_constants.logging_enums import ApplicationLayerLogging, LogEvent, LoggingComponent


logger = configure_logging()


class EncodingServices:
    """
    Service layer for encoding and decoding data using Fernet encryption.
    """

    def __init__(self):
        self.fernet = FernetEncoder()

    def fernet_encoding(self, text: str) -> str:
        """Encrypt text using Fernet."""
        
        logger.info("[%s] [%s] fernet encryption [$s]",
                    ApplicationLayerLogging.SERVICE.value,
                    LoggingComponent.ENCODING_SERVICES.value,
                    LogEvent.STARTED.value)

        if not text or not text.strip():
            logger.warning("[%s] [%s] text is empty for fernet encryption [$s]",
                    ApplicationLayerLogging.SERVICE.value,
                    LoggingComponent.ENCODING_SERVICES.value,
                    LogEvent.FAILED.value)
            raise ValueError(
                "Text is required for Fernet encoding."
            )

        logger.info("[%s] [%s] fernet encryption [$s]",
                    ApplicationLayerLogging.SERVICE.value,
                    LoggingComponent.FERNET_ENCODER.value,
                    LogEvent.CALLED.value)

        result = self.fernet.encode_text(text)

        logger.info("[%s] [%s] fernet encryption [$s]",
                    ApplicationLayerLogging.SERVICE.value,
                    LoggingComponent.FERNET_ENCODER.value,
                    LogEvent.COMPLETED.value)

        return result

    def fernet_decoding(self, encrypted_text: str) -> str:
        """Decrypt Fernet encrypted text."""
        
        logger.info("[%s] [%s] fernet decryption [$s]",
                    ApplicationLayerLogging.SERVICE.value,
                    LoggingComponent.ENCODING_SERVICES.value,
                    LogEvent.STARTED.value)

        if not encrypted_text or not encrypted_text.strip():
            logger.warning("[%s] [%s] text is empty for fernet decryption [$s]",
                    ApplicationLayerLogging.SERVICE.value,
                    LoggingComponent.ENCODING_SERVICES.value,
                    LogEvent.FAILED.value)
            raise ValueError(
                "Encrypted text is required for Fernet decoding."
            )

        logger.info("[%s] [%s] fernet decryption [$s]",
                    ApplicationLayerLogging.SERVICE.value,
                    LoggingComponent.FERNET_ENCODER.value,
                    LogEvent.CALLED.value)

        result = self.fernet.decode_text(
            encrypted_text
        )

        logger.info("[%s] [%s] fernet decryption [$s]",
                    ApplicationLayerLogging.SERVICE.value,
                    LoggingComponent.FERNET_ENCODER.value,
                    LogEvent.COMPLETED.value)

        return result