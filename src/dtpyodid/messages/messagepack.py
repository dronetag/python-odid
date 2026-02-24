import io
import struct
from typing import ClassVar

from .. import parser
from .base import MAX_MESSAGE_SIZE, MAX_MESSAGES_IN_PACK, Message


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
        buffer.write(struct.pack("BB", max_message_size, len(messages)))
        for message in messages:
            msg_size = buffer.write(message)
            if msg_size < max_message_size:
                buffer.write(b"\0" * max_message_size - msg_size)
        return buffer.getvalue()


    def __repr__(self) -> str:
        return f"MessagePack(message_size={self.message_size} messages_in_pack={len(self.messages)})"
