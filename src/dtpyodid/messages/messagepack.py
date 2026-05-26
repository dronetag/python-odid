import io
import struct
from dataclasses import dataclass, field
from typing import ClassVar, Type

from dtpyodid.message import MAX_MESSAGE_SIZE, MAX_MESSAGES_IN_PACK, Message

from .auth import Auth
from .basicid import BasicID
from .location import Location
from .operatorid import OperatorID
from .selfid import SelfID
from .system import System

MESSAGES: list[Type[Message]] = [
    Auth,
    BasicID,
    Location,
    OperatorID,
    SelfID,
    System,
]

@dataclass
class MessagePack(Message):
    rid: ClassVar[int] = 0xF

    messages: list[Message] = field(default_factory=list)

    @classmethod
    def _parse(cls, data: bytes) -> bytes:
        message_size = data[0]
        messages_in_pack = data[1]

        msg_pack = cls()

        if message_size > MAX_MESSAGE_SIZE:
            raise ValueError(
                f"Invalid declared message size in MessagePack {message_size}"
            )
        if messages_in_pack <= 0 or messages_in_pack > MAX_MESSAGES_IN_PACK:
            raise ValueError("")

        data = data[2:]
        for _ in range(messages_in_pack):
            for MESSAGE in MESSAGES:
                if message := MESSAGE.parse(data[: message_size]):
                    msg_pack.messages.append(message)
                    break
            data = data[message_size :]

        return msg_pack

    def _pack(self) -> bytes:
        buffer = io.BytesIO()
        messages = []
        max_message_size = 0
        for i, message in enumerate(self.messages):
            if i == MAX_MESSAGES_IN_PACK:
                break
            messages.append(message.pack())
            max_message_size = max(max_message_size, len(messages[-1]))
        if max_message_size > MAX_MESSAGE_SIZE:
            raise ValueError(
                f"One message in pack is longer ({max_message_size}) than {MAX_MESSAGE_SIZE}")
        buffer.write(struct.pack("BB", MAX_MESSAGE_SIZE, len(messages)))
        for message in messages:
            msg_size = buffer.write(message)
            if msg_size < MAX_MESSAGE_SIZE:
                buffer.write(b"\0" * (MAX_MESSAGE_SIZE - msg_size))
        return buffer.getvalue()
