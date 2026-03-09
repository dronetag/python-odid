from pyopendroneid import helper, opendroneid

import dtpyodid


def test_location_encode():
    ts = 2345.4
    og_location = opendroneid.ODID_Location_data(
        Status = opendroneid.ODID_STATUS_GROUND,
        Direction = 359,
        SpeedHorizontal = 1,
        SpeedVertical = 2,
        Latitude = 50.0740381,
        Longitude = 14.4666297,
        AltitudeBaro = 111,
        AltitudeGeo = 112,
        HeightType = opendroneid.ODID_HEIGHT_REF_OVER_TAKEOFF,
        Height = 108.5,
        # HorizAccuracy", ODID_Horizontal_accuracy_t),
        # VertAccuracy", ODID_Vertical_accuracy_t),
        # BaroAccuracy", ODID_Vertical_accuracy_t),
        # SpeedAccuracy", ODID_Speed_accuracy_t),
        # TSAccuracy", ODID_Timestamp_accuracy_t),
        TimeStamp = ts,
        )
    og_location_encoded = opendroneid.ODID_Location_encoded()
    opendroneid.encodeLocationMessage(og_location_encoded, og_location)
    og_location_bytes = bytes(og_location_encoded)

    new_location_bytes = dtpyodid.Location(
        status = opendroneid.ODID_STATUS_GROUND,
        direction = 359,
        speed_horizontal = 1,
        speed_vertical = 2,
        latitude = 50.0740381,
        longitude = 14.4666297,
        altitude_baro = 111,
        altitude_geo = 112,
        height_type = opendroneid.ODID_HEIGHT_REF_OVER_TAKEOFF,
        height = 108.5,
        # HorizAccuracy", ODID_Horizontal_accuracy_t),
        # VertAccuracy", ODID_Vertical_accuracy_t),
        # BaroAccuracy", ODID_Vertical_accuracy_t),
        # SpeedAccuracy", ODID_Speed_accuracy_t),
        # TSAccuracy", ODID_Timestamp_accuracy_t),
        timestamp = ts,
    ).pack()

    print(og_location_bytes.hex())
    print(new_location_bytes.hex())
    assert og_location_bytes == (new_location_bytes + b'\00\00\00')  # WTF WHY?!

def test_location_decode():
    ts = 2345.4

    og_location = opendroneid.ODID_Location_data()
    opendroneid.odid_initLocationData(og_location)
    
    location_bytes = dtpyodid.Location(
        status = opendroneid.ODID_STATUS_GROUND,
        direction = 359,
        speed_horizontal = 1,
        speed_vertical = 2,
        latitude = 50.0740381,
        longitude = 14.4666297,
        altitude_baro = 111,
        altitude_geo = 112,
        height_type = opendroneid.ODID_HEIGHT_REF_OVER_TAKEOFF,
        height = 108.5,
        # HorizAccuracy", ODID_Horizontal_accuracy_t),
        # VertAccuracy", ODID_Vertical_accuracy_t),
        # BaroAccuracy", ODID_Vertical_accuracy_t),
        accuracy_speed = 3,
        # TSAccuracy", ODID_Timestamp_accuracy_t),
        timestamp = ts,
    ).pack()
    assert len(location_bytes) == 25

    # Convert bytes to ODID_Location_encoded structure
    location_encoded = opendroneid.ODID_Location_encoded.from_buffer_copy(
        location_bytes + b'\00\00\00')  # WTF WHY?! Should be 25 bytes!
    opendroneid.decodeLocationMessage(og_location, location_encoded)

    assert og_location.Status == opendroneid.ODID_STATUS_GROUND
    assert og_location.Direction == 359
    assert og_location.SpeedHorizontal == 1
    assert og_location.SpeedVertical == 2
    assert og_location.Latitude == 50.0740381
    assert og_location.Longitude == 14.4666297
    assert og_location.AltitudeBaro == 111
    assert og_location.AltitudeGeo == 112
    assert og_location.HeightType == opendroneid.ODID_HEIGHT_REF_OVER_TAKEOFF
    assert og_location.Height == 108.5  # can do only halves
    # assert og_location.HorizAccuracy == HorizAccuracy", ODID_Horizontal_accuracy_t),
    # assert og_location.VertAccuracy == VertAccuracy", ODID_Vertical_accuracy_t),
    # assert og_location.BaroAccuracy == BaroAccuracy", ODID_Vertical_accuracy_t),
    # assert og_location.SpeedAccuracy == SpeedAccuracy", ODID_Speed_accuracy_t),
    # assert og_location.TSAccuracy == TSAccuracy", ODID_Timestamp_accuracy_t),
    assert int(og_location.TimeStamp) == int(ts)  # e.g. 2309.2


def test_location_decode_generic():
    ts = 2345.4

    location_bytes = dtpyodid.Location(
        status = opendroneid.ODID_STATUS_GROUND,
        direction = 359,
        speed_horizontal = 1,
        speed_vertical = 2,
        latitude = 50.0740381,
        longitude = 14.4666297,
        altitude_baro = 111,
        altitude_geo = 112,
        height_type = opendroneid.ODID_HEIGHT_REF_OVER_TAKEOFF,
        height = 108.5,
        # HorizAccuracy", ODID_Horizontal_accuracy_t),
        # VertAccuracy", ODID_Vertical_accuracy_t),
        # BaroAccuracy", ODID_Vertical_accuracy_t),
        accuracy_speed = 3,
        # TSAccuracy", ODID_Timestamp_accuracy_t),
        timestamp = ts,
    ).pack()
    assert len(location_bytes) == 25

    # Convert bytes to ODID_Location_encoded structure
    msg_type, decoded = helper.parseOpenDroneID(location_bytes)
    assert msg_type == opendroneid.ODID_MESSAGETYPE_LOCATION
    assert "Location" in decoded

    assert decoded["Location"]["Status"] == opendroneid.ODID_STATUS_GROUND
    assert decoded["Location"]["Direction"] == 359
    assert decoded["Location"]["SpeedHorizontal"] == 1
    assert decoded["Location"]["SpeedVertical"] == 2
    assert decoded["Location"]["Latitude"] == 50.0740381
    assert decoded["Location"]["Longitude"] == 14.4666297
    assert decoded["Location"]["AltitudeBaro"] == 111
    assert decoded["Location"]["AltitudeGeo"] == 112
    assert decoded["Location"]["HeightType"] == opendroneid.ODID_HEIGHT_REF_OVER_TAKEOFF
    assert decoded["Location"]["Height"] == 108.5
    # assert decoded["Location"]["HorizAccuracy"] == HorizAccuracy", ODID_Horizontal_accuracy_t),
    # assert decoded["Location"]["VertAccuracy"] == VertAccuracy", ODID_Vertical_accuracy_t),
    # assert decoded["Location"]["BaroAccuracy"] == BaroAccuracy", ODID_Vertical_accuracy_t),
    # assert decoded["Location"]["SpeedAccuracy"] == SpeedAccuracy", ODID_Speed_accuracy_t),
    # assert decoded["Location"]["TSAccuracy"] == TSAccuracy", ODID_Timestamp_accuracy_t),
    assert int(decoded["Location"]["Timestamp"]) == int(ts)  # e.g. 2309.2
