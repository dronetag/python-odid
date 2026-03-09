import logging
from typing import Optional, Type

from .message import Message
from .messages.auth import Auth
from .messages.basicid import BasicID
from .messages.location import Location
from .messages.messagepack import MessagePack
from .messages.operatorid import OperatorID
from .messages.selfid import SelfID
from .messages.system import System

MESSAGES: list[Type[Message]] = {
    BasicID,
    Location,
    Auth,
    SelfID,
    System,
    OperatorID,
    MessagePack,
}

logger = logging.getLogger("odid")


def parse(data: bytes) -> Optional[Message]:
    # sanity check that the message type (half)byte agrees with `self.rid`
    for MESSAGE in MESSAGES:
        if message := MESSAGE.parse(data):
            return message
    return None