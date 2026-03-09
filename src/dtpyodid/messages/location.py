import enum
import struct
from dataclasses import dataclass
from typing import ClassVar

from dtpyodid.message import LAT_LONG_MULTIPLIER, SPEED_VERTICAL_MULTIPLIER, Message


class Location_Status(enum.IntEnum):
    NONE = 0
    ON_GROUND = 1
    IN_AIR = 2
    EMERGENCY = 3


class Location_Height_Type(enum.IntEnum):
    ABOVE_START = 0
    AGL = 1


def is_full_timestamp(ts: float) -> bool:
    return ts > 2**16


@dataclass
class Location(Message):
    rid: ClassVar[int] = 0x1

    # See DIN EN 4709-002 for specific values i.e. for the accuracy
    latitude: float
    longitude: float
    height: float

    status: Location_Status = Location_Status.NONE
    height_type: Location_Height_Type = Location_Height_Type.AGL
    ew_direction: int = 0
    speed_mult: int = 0
    direction: int = 0
    speed_horizontal: int = 0
    speed_vertical: int = 0
    altitude_baro: float = -1000
    altitude_geo: float = -1000
    timestamp: int = 0
    accuracy_time: int = 0
    accuracy_horizontal: int = 0
    accuracy_vertical: int = 0
    accuracy_baro: int = 0
    accuracy_speed: int = 0

    @classmethod
    def _parse(cls, data: bytes) -> "Location":
        b = data[0]
        status = (b & 0xF0) >> 4
        height_type = (b & 0x04) >> 2
        ew_direction = (b & 0x02) >> 1
        speed_mult = b & 0x01

        direction = data[1]
        speed_hori = data[2]
        speed_vert = data[3]

        data = data[4:]

        next_format = "<iihhh"
        next_size = struct.calcsize(next_format)
        lat, lng, altPres, altGeo, height = struct.unpack(next_format, data[:next_size])
        data = data[next_size:]

        height = height

        next_format = "<BBHB"
        next_size = struct.calcsize(next_format)
        hori_vert_acc, speed_baro_acc, ts, time_acc = struct.unpack(
            next_format, data[:next_size]
        )
        data = data[next_size:]

        return cls(
            status = status,
            height_type = height_type,
            ew_direction = ew_direction,
            speed_mult = speed_mult,
            speed_hori = calc_speed(speed_hori, speed_mult),
            speed_vert = SPEED_VERTICAL_MULTIPLIER * speed_vert,
            direction = calc_direction(direction, ew_direction),

            latitude=LAT_LONG_MULTIPLIER * lat,
            longitude=LAT_LONG_MULTIPLIER * lng,
            altitude_baro=calc_altitude(altPres),
            altitude_geo=calc_altitude(altGeo),
            height=calc_altitude(height),

            accuracy_horizontal=hori_vert_acc & 0x0F,
            accuracy_vertical=(hori_vert_acc & 0xF0) >> 4,
            accuracy_baro=(speed_baro_acc & 0xF0) >> 4,
            accuracy_speed=speed_baro_acc & 0x0F,
            timestamp=ts,
            accuracy_time = time_acc * 0.1,
        )

    def _pack(self):
        if self.direction > 179:
            self.ew_direction = 1
        else:
            self.ew_direction = 0

        if self.speed_horizontal <= 255 * 0.25:
            self.speed_mult = 0
        else:
            self.speed_mult = 1

        raw_speed_vert = int(self.speed_vertical / SPEED_VERTICAL_MULTIPLIER)
        raw_latitude = int(self.latitude / LAT_LONG_MULTIPLIER)
        raw_longitude = int(self.longitude / LAT_LONG_MULTIPLIER)
        raw_accuracy_time = int(self.accuracy_time / 0.1)
        raw_direction = calc_direction_raw(self.direction, self.ew_direction)
        raw_speed_hori = calc_speed_raw(self.speed_horizontal, self.speed_mult)
        raw_altitude_baro = calc_altitude_raw(self.altitude_baro)
        raw_altitude_geo = calc_altitude_raw(self.altitude_geo)
        raw_height = calc_altitude_raw(self.height)

        a = (self.status << 4) & 0xF0
        b = (self.height_type << 2) & 0x04
        c = (self.ew_direction << 1) & 0x02
        d = self.speed_mult & 0x01
        first = ((a | b | c | d) & 0xFF).to_bytes(1, "little")

        pack1 = ( # 4 bytes
            first
            + (raw_direction & 0xFF).to_bytes(1, "little")
            + (raw_speed_hori & 0xFF).to_bytes(1, "little")
            + (raw_speed_vert & 0xFF).to_bytes(1, "little")
        )
        pack2 = struct.pack(  # 2*4 + 3*2 = 14 bytes
            "<iihhh",
            raw_latitude,
            raw_longitude,
            raw_altitude_baro,
            raw_altitude_geo,
            raw_height,
        )

        accuracy_vertical = (self.accuracy_vertical << 4) & 0xF0
        accuracy_horizontal = self.accuracy_horizontal & 0x0F
        e = accuracy_vertical | accuracy_horizontal
        accuracy_baro = (self.accuracy_baro << 4) & 0xF0
        accuracy_speed = self.accuracy_speed & 0x0F
        f = accuracy_baro | accuracy_speed
        ts = self.timestamp
        if is_full_timestamp(self.timestamp):
            ts = int(self.timestamp * 10) % 36000
        elif isinstance(self.timestamp, float):
            ts = int(self.timestamp * 10)
        pack3 = struct.pack(  # 2+2+1 = 5 bytes
            "<BBHB", e, f, ts, raw_accuracy_time & 0x07)

        return pack1 + pack2 + pack3 + (b"\0" * 1)


def calc_speed(value, mult) -> float:
    if mult == 0:
        return value * 0.25
    return (value * 0.75) + (255 * 0.25)

def calc_speed_raw(value, mult) -> float:
    if mult == 0:
        return int(value / 0.25)
    return int((value - (255 * 0.25)) / 0.75)

def calc_direction(value, ew) -> float:
    if ew == 0:
        return value
    return value + 180

def calc_direction_raw(value, ew) -> int:
    if ew == 0:
        return value
    return value - 180

def calc_altitude(value) -> float:
    return value / 2 - 1000

def calc_altitude_raw(value) -> float:
    return int((value + 1000) * 2)
