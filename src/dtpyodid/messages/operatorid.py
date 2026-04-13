import enum

from dtpyodid.message import MAX_ID_BYTE_SIZE, Message


class OperatorID_Type(enum.IntEnum):
    CAA = 0


class OperatorID(Message):
    rid: int = 0x5

    def __init__(self) -> None:
        self.operator_type = 0xFF
        self.operator_id = ""

    @staticmethod
    def _parse(data) -> "OperatorID":
        pack = OperatorID()
        pack.operator_type = OperatorID_Type(data[0])
        pack.operator_id = str(data[1:], "ascii")
        return pack

    def _pack(self):
        op_type = (self.operator_type & 0xFF).to_bytes(1, "little")

        op_id = bytes(self.operator_id, "ascii")
        op_id += b"\0" * (MAX_ID_BYTE_SIZE - len(op_id))

        return op_type + op_id + (b"\0" * 3)

    def __repr__(self) -> str:
        return f'RemoteID_OperatorID(operator_type={self.operator_type.name}, ' \
               f'operator_id="{self.operator_id}")'
