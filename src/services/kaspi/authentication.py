import logging
import re

from pyrogram import Client
from pyrogram.types import Message

from settings import MTPROTO_API_HASH, MTPROTO_API_ID
from src.models.orm import ConfirmCode

logger = logging.getLogger(__name__)


def match_confirm_code(text):
    pattern = r"Код:([\d]+)"
    code = re.findall(pattern, text, re.I)
    return code[0] if len(code) else None


def get_confirmation_code():
    logger.info("Searching for confirmation code")

    with Client("client_session", MTPROTO_API_ID, MTPROTO_API_HASH) as app:
        message: Message
        messages = app.get_history("@HcksBOT", limit=10)
        result = None

        logger.info("Iterating over the messages")
        for message in messages:  # noqa
            code = match_confirm_code(message.text)
            if code is None:
                continue

            status = ConfirmCode.check(code)
            if not status:
                result = code
                ConfirmCode.register_code(code)

        logger.info("Correct code was found: {}".format(result))
        return result
