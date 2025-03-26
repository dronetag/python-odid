from .base import Message, MAX_STRING_BYTE_SIZE
from . import utils

SelfID_Description_Type = {"TEXT": 0, "EMERGENCY": 1, "EXTENDED_STATUS": 2}


class SelfID(Message):
    rid: int = 0x3

    description_type: int
    operation_description: str

    def __init__(self) -> None:
        self.description_type = 0xFF
        self.operation_description = ""

    def parse(self, data: bytes) -> bytes:
        data = super().parse(data)
        self.description_type = data[0]
        self.operation_description = str(data[1:25], "ascii")
        return data[25:]

    def pack(self):
        desc_type = (self.description_type & 0xFF).to_bytes(1, "little")

        desc = bytes(self.operation_description, "ascii")
        desc += b"\0" * (MAX_STRING_BYTE_SIZE - len(desc))

        return desc_type + desc

    def __str__(self) -> str:
        return f'RemoteID_SelfID: description_type={utils.get_key_by_value(SelfID_Description_Type, self.description_type)} operation_description="{self.operation_description}"'
