import os

from cryptography.fernet import (
    Fernet,
    InvalidToken,
)

from config.logger_config import configure_logging

from app_constants.logging_enums import (
    ApplicationLayerLogging,
    LogEvent,
    LoggingComponent,
)


logger = configure_logging()


class FernetEncoder:
    """
    Provides text encryption and decryption using
    Fernet symmetric encryption.
    """

    def __init__(self):
        """
        Initialize the Fernet encoder using the
        FERNET_KEY environment variable.
        """

        logger.info(
            "[%s] [%s] initializing Fernet encoder [%s]",
            ApplicationLayerLogging.SECURITY.value,
            LoggingComponent.FERNET_ENCODER.value,
            LogEvent.STARTED.value,
        )

        self.fernet_key = os.getenv("FERNET_KEY")

        if not self.fernet_key:
            logger.error(
                "[%s] [%s] Fernet key is not configured [%s]",
                ApplicationLayerLogging.SECURITY.value,
                LoggingComponent.FERNET_ENCODER.value,
                LogEvent.FAILED.value,
            )

            raise ValueError(
                "FERNET_KEY is required for encryption."
            )

        try:
            self.fernet = Fernet(
                self.fernet_key.encode("utf-8")
            )

        except (ValueError, TypeError) as error:

            logger.error(
                "[%s] [%s] invalid Fernet key configuration [%s]",
                ApplicationLayerLogging.SECURITY.value,
                LoggingComponent.FERNET_ENCODER.value,
                LogEvent.FAILED.value,
            )

            raise ValueError(
                "FERNET_KEY is not a valid Fernet key."
            ) from error

        logger.info(
            "[%s] [%s] Fernet encoder initialized successfully [%s]",
            ApplicationLayerLogging.SECURITY.value,
            LoggingComponent.FERNET_ENCODER.value,
            LogEvent.COMPLETED.value,
        )

    def encode_text(self, text: str) -> str:
        """
        Encrypt plaintext and return a Fernet token.

        Args:
            text: Plaintext to encrypt.

        Returns:
            Encrypted Fernet token as a string.

        Raises:
            ValueError: If the plaintext is empty.
        """

        logger.info(
            "[%s] [%s] Fernet encoding requested [%s]",
            ApplicationLayerLogging.SECURITY.value,
            LoggingComponent.FERNET_ENCODER.value,
            LogEvent.STARTED.value,
        )

        if not text or not text.strip():

            logger.warning(
                "[%s] [%s] encryption failed: empty text [%s]",
                ApplicationLayerLogging.SECURITY.value,
                LoggingComponent.FERNET_ENCODER.value,
                LogEvent.FAILED.value,
            )

            raise ValueError(
                "Text is required for encryption."
            )

        encrypted_text = self.fernet.encrypt(
            text.encode("utf-8")
        )

        logger.info(
            "[%s] [%s] Fernet encoding completed successfully [%s]",
            ApplicationLayerLogging.SECURITY.value,
            LoggingComponent.FERNET_ENCODER.value,
            LogEvent.COMPLETED.value,
        )

        return encrypted_text.decode("utf-8")

    def decode_text(self, encrypted_text: str) -> str:
        """
        Decrypt a Fernet token and return plaintext.

        Args:
            encrypted_text: Fernet token to decrypt.

        Returns:
            Decrypted plaintext.

        Raises:
            ValueError: If the encrypted text is empty or
                        the token is invalid.
        """

        logger.info(
            "[%s] [%s] Fernet decoding requested [%s]",
            ApplicationLayerLogging.SECURITY.value,
            LoggingComponent.FERNET_ENCODER.value,
            LogEvent.STARTED.value,
        )

        if not encrypted_text or not encrypted_text.strip():

            logger.warning(
                "[%s] [%s] decryption failed: empty encrypted text [%s]",
                ApplicationLayerLogging.SECURITY.value,
                LoggingComponent.FERNET_ENCODER.value,
                LogEvent.FAILED.value,
            )

            raise ValueError(
                "Encrypted text is required for decryption."
            )

        try:
            decrypted_text = self.fernet.decrypt(
                encrypted_text.encode("utf-8")
            )

        except InvalidToken as error:

            logger.error(
                "[%s] [%s] Fernet decoding failed: invalid token [%s]",
                ApplicationLayerLogging.SECURITY.value,
                LoggingComponent.FERNET_ENCODER.value,
                LogEvent.FAILED.value,
            )

            raise ValueError(
                "Unable to decrypt the provided text."
            ) from error

        logger.info(
            "[%s] [%s] Fernet decoding completed successfully [%s]",
            ApplicationLayerLogging.SECURITY.value,
            LoggingComponent.FERNET_ENCODER.value,
            LogEvent.COMPLETED.value,
        )

        return decrypted_text.decode("utf-8")