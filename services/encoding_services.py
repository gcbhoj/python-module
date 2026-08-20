from config.logger_config import configure_logging

from security.fernet_encoder import FernetEncoder


logger = configure_logging()


class EncodingServices:
    """Helper service for encoding and decoding data."""

    def __init__(self):
        self.fernet = FernetEncoder()

        logger.info(
            "Encoding service initialized."
        )

    def fernet_encoding(self, text: str) -> str:
        """Encrypt text using Fernet."""

        if not text or not text.strip():
            raise ValueError(
                "Text is required for Fernet encoding."
            )

        logger.info(
            "Fernet encoding started in helper."
        )

        result = self.fernet.encode_text(text)

        logger.info(
            "Fernet encoding completed in helper."
        )

        return result

    def fernet_decoding(self, encrypted_text: str) -> str:
        """Decrypt Fernet encrypted text."""

        if not encrypted_text or not encrypted_text.strip():
            raise ValueError(
                "Encrypted text is required for Fernet decoding."
            )

        logger.info(
            "Fernet decoding started in helper."
        )

        result = self.fernet.decode_text(
            encrypted_text
        )

        logger.info(
            "Fernet decoding completed in helper."
        )

        return result