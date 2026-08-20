import os

from cryptography.fernet import Fernet, InvalidToken

from config.logger_config import configure_logging


logger = configure_logging()


class FernetEncoder:
    """
    Provides text encryption and decryption using Fernet symmetric encryption.
    """

    def __init__(self):
        self.fernet_key = os.getenv("FERNET_KEY")

        if not self.fernet_key:
            logger.error("Fernet key is not configured.")
            raise ValueError(
                "FERNET_KEY is required for encryption."
            )

        try:
            self.fernet = Fernet(
                self.fernet_key.encode("utf-8")
            )

        except (ValueError, TypeError) as error:
            logger.error(
                "Invalid Fernet key configuration."
            )
            raise ValueError(
                "FERNET_KEY is not a valid Fernet key."
            ) from error

        logger.info("Fernet encryption service initialized.")

    def encode_text(self, text: str) -> str:
        """
        Encrypt plaintext and return a Fernet token.
        """

        if not text or not text.strip():
            logger.warning(
                "Encryption failed: text is empty."
            )
            raise ValueError(
                "Text is required for encryption."
            )

        logger.info("Fernet encoding started.")

        encrypted_text = self.fernet.encrypt(
            text.encode("utf-8")
        )

        logger.info("Fernet encoding completed.")

        return encrypted_text.decode("utf-8")

    def decode_text(self, encrypted_text: str) -> str:
        """
        Decrypt a Fernet token and return plaintext.
        """

        if not encrypted_text or not encrypted_text.strip():
            logger.warning(
                "Decryption failed: encrypted text is empty."
            )
            raise ValueError(
                "Encrypted text is required for decryption."
            )

        logger.info("Fernet decoding started.")

        try:
            decrypted_text = self.fernet.decrypt(
                encrypted_text.encode("utf-8")
            )

        except InvalidToken as error:
            logger.error(
                "Fernet decoding failed: invalid token."
            )
            raise ValueError(
                "Unable to decrypt the provided text."
            ) from error

        logger.info("Fernet decoding completed.")

        return decrypted_text.decode("utf-8")