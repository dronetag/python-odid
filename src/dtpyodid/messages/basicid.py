import enum
from dataclasses import dataclass
from typing import ClassVar

from dtpyodid.message import MAX_ID_BYTE_SIZE, Message


class BasicID_ID_Type(enum.IntEnum):
    NONE = 0
    SERIAL_NUMBER = 1
    CAA_REGISTRATION_ID = 2
    UTM_ASSIGNED_UUID = 3
    SPECIFIC_SESSION_ID = 4
    ERROR = 0xf


class BasicID_UA_Type(enum.IntEnum):
    NONE = 0
    AEROPLANE = 1
    HELICOPTER_OR_MULTIROTOR = 2
    GYROPLANE = 3
    HYBRID_LIFT = 4
    ORNITHOPTER = 5
    GLIDER = 6
    KITE = 7
    FREE_BALLOON = 8
    CAPTIVE_BALLOON = 9
    AIRSHIP = 10
    FREE_FALL_PARACHUTE = 11
    ROCKET = 12
    TETHERED_POWERED_AIRCRAFT = 13
    GROUND_OBSTACLE = 14
    OTHER = 15


@dataclass
class BasicID(Message):
    rid: ClassVar[int] = 0x0
    id_type: BasicID_ID_Type = BasicID_ID_Type.NONE
    ua_type: BasicID_UA_Type = BasicID_UA_Type.OTHER
    uas_id: str = ""

    @classmethod
    def _parse(cls, data: bytes) -> "BasicID":
        basic_types = data[0]
        pack = cls()
        pack.id_type = BasicID_ID_Type((basic_types & 0xF0) >> 4)
        pack.ua_type = BasicID_UA_Type(basic_types & 0x0F)
        pack.uas_id = str(data[1:], "ascii").strip("\0")
        return pack

    def _pack(self):
        id_type_nibble = (self.id_type << 4) & 0xF0
        ua_type_nibble = self.ua_type & 0x0F
        basic_types = (id_type_nibble | ua_type_nibble).to_bytes(1, "little")

        uas_id = bytes(self.uas_id, "ascii")
        uas_id += b"\0" * (MAX_ID_BYTE_SIZE - len(uas_id))

        return basic_types + uas_id + (b"\0" * 3)

    # def __repr__(self) -> str:
    #     return f'RemoteID_BasicID(id_type={self.id_type.name}, ' \
    #            f'ua_type={self.ua_type.name}, uas_id="{self.uas_id}")'
