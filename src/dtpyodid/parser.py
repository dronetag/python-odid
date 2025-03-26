import logging
from typing import Type

from .messages.auth import Auth
from .messages.base import Message, RID_VERSION
from .messages.system import System
from .messages.selfid import SelfID
from .messages.basicid import BasicID
from .messages.location import Location
from .messages.messagepack import MessagePack
from .messages.operatorid import OperatorID


TYPES: dict[int, Type[Message]] = {
    BasicID.rid: BasicID,
    Location.rid: Location,
    Auth.rid: Auth,
    SelfID.rid: SelfID,
    System.rid: System,
    OperatorID.rid: OperatorID,
    MessagePack.rid: MessagePack,
}

logger = logging.getLogger("odid")


def parse(data: bytes) -> Message:
    # sanity check that the message type (half)byte agrees with `self.rid`
    parsed_type = (data[0] & 0xF0) >> 4
    if parsed_type not in TYPES:
        raise ValueError(f"Unknown message type {parsed_type}! Known {TYPES.keys()}")

    rid_version = data[0] & 0x0F  # RID version (does anyone use that?)
    if rid_version != RID_VERSION:
        logger.warning(
            f"RID version {rid_version} arrived! We support only version {RID_VERSION}"
        )

    message = TYPES[parsed_type]()
    message.parse(data[1:])
    return message
