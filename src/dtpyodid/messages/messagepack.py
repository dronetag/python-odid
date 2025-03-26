from typing import ClassVar
from .base import Message, MAX_MESSAGE_SIZE, MAX_MESSAGES_IN_PACK
from .. import parser


class MessagePack(Message):
    rid: ClassVar[int] = 0xF

    message_size: int
    messages: list[Message]

    def __init__(self, message_size: int = 25) -> None:
        self.message_size = message_size
        self.messages = []

    def parse(self, data: bytes) -> bytes:
        self.message_size = data[0]
        messages_in_pack = data[1]

        if self.message_size > MAX_MESSAGE_SIZE:
            raise ValueError(
                f"Invalid declared message size in MessagePack {self.message_size}"
            )
        if messages_in_pack <= 0 or messages_in_pack > MAX_MESSAGES_IN_PACK:
            raise ValueError("")

        data = data[2:]
        for _ in range(messages_in_pack):
            self.messages.append(parser.parse(data[: self.message_size]))
            data = data[self.message_size :]
        return data

    def pack(self) -> bytes:
        return b""

    def __repr__(self) -> str:
        return f"MessagePack(message_size={self.message_size} messages_in_pack={len(self.messages)})"
