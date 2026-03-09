import enum
from dataclasses import dataclass
from typing import ClassVar

from dtpyodid.message import MAX_STRING_BYTE_SIZE, Message


class Type(enum.IntEnum):
    TEXT = 0
    EMERGENCY = 1
    EXTENDED_STATUS = 2
    INVALID = 0xFF


@dataclass
class SelfID(Message):
    rid: ClassVar[int] = 0x3

    desc: str
    desc_type: int = Type.INVALID

    @classmethod
    def _parse(data: bytes) -> "SelfID":
        return SelfID(
            desc_type=data[0],
            desc=str(data[1:25], "ascii"),
        )

    def _pack(self) -> bytes:
        desc_type = (self.desc_type & 0xFF).to_bytes(1, "little")

        desc = bytes(self.desc, "ascii")
        desc += b"\0" * (MAX_STRING_BYTE_SIZE - len(desc))

        return desc_type + desc
