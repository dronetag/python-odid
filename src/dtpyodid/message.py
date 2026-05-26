import logging
import struct
from abc import ABC
from typing import ClassVar, Optional, Self

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

logger = logging.getLogger("odid")

class Message(ABC):
    rid: ClassVar[int]

    @classmethod
    def parse(cls, data: bytes) -> Optional[Self]:
        # sanity check that the message type (half)byte agrees with `self.rid`
        parsed_type = (data[0] & 0xF0) >> 4
        if parsed_type != cls.rid:
            return None

        # rid_version = data[0] & 0x0F  # RID version (does anyone use that?)
        # if rid_version != RID_VERSION:
        #     logger.warning(
        #         f"RID version {rid_version} arrived! We support only version {RID_VERSION}"
        #     )

        return cls._parse(data[1:])

    def _parse(self, data: bytes) -> Self:
        """Parse bytes into message fields and returns any remaining (unused) bytes"""
        raise NotImplementedError()

    def pack(self) -> bytes:
        """Encode itself into a byte stream"""
        return struct.pack("B", (self.rid << 4) | RID_VERSION) + self._pack()

    def _pack(self) -> bytes:
        """Encode itself into a byte stream"""
        raise NotImplementedError()
