from typing import TypeVar, Union
from .base import Message, RID_VERSION


T = TypeVar("T")


def get_key_by_value(data: dict[str, T], val: T) -> Union[str, T]:
    keys = [k for k, v in data.items() if v == val]
    if keys:
        return keys[0]
    return val


def pack(message: Message) -> bytes:
    type_nibble = (message.rid << 4) & 0xF0
    version_nibble = RID_VERSION & 0x0F
    header = (type_nibble | version_nibble).to_bytes(1, "little")
    return header + message.pack()
