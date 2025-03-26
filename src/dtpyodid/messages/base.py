from abc import ABC
from typing import ClassVar

LAT_LONG_MULTIPLIER = 1e-7
SPEED_VERTICAL_MULTIPLIER = 0.5

MAX_AUTH_DATA_PAGES = 16
MAX_AUTH_PAGE_ZERO_SIZE = 17
MAX_AUTH_PAGE_NON_ZERO_SIZE = 23
MAX_AUTH_DATA = (
    MAX_AUTH_PAGE_ZERO_SIZE + (MAX_AUTH_DATA_PAGES - 1) * MAX_AUTH_PAGE_NON_ZERO_SIZE
)

MAX_MESSAGE_SIZE = 25
MAX_MESSAGES_IN_PACK = 9

MAX_ID_BYTE_SIZE = 20
MAX_STRING_BYTE_SIZE = 23

RID_VERSION: int = 2


class Message(ABC):
    rid: ClassVar[int]

    def parse(self, data: bytes) -> bytes:
        """Parse bytes into message fields and returns any remaining (unused) bytes"""
        raise NotImplementedError()

    def pack(self) -> bytes:
        """Encode itself into a byte stream"""
        raise NotImplementedError()
