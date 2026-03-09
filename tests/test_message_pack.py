from pyopendroneid import helper, opendroneid

import dtpyodid


def test_message_pack():
    ts = 2345.4

    basic_id = dtpyodid.BasicID(
        ua_type=opendroneid.ODID_UATYPE_GROUND_OBSTACLE,
        id_type=opendroneid.ODID_IDTYPE_NONE,
        uas_id="SCOUT01"
    )
    basic_id_1 = dtpyodid.SelfID(
        desc="D1TEST1",
        desc_type=opendroneid.ODID_DESC_TYPE_TEXT,
    )

    location = dtpyodid.Location(
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
    )

    message_pack = dtpyodid.MessagePack(messages=[
        basic_id,
        basic_id_1,
        location,
    ])

    msg_type, messages = helper.parseOpenDroneID(message_pack.pack())
    assert msg_type == opendroneid.ODID_MESSAGETYPE_PACKED

    print(f"{messages=}")

    assert messages['BasicID'][0]['UAType'] == opendroneid.ODID_UATYPE_GROUND_OBSTACLE
    assert messages['BasicID'][0]['IDType'] == 0
    assert messages['BasicID'][0]['UASID'] == "SCOUT01"

    assert messages['SelfID']['DescType'] == opendroneid.ODID_DESC_TYPE_TEXT
    assert messages['SelfID']['Desc'] == "D1TEST1"

    assert messages['Location']['Status'] == opendroneid.ODID_STATUS_GROUND
    assert messages['Location']['Direction'] == 359.0
    assert messages['Location']['SpeedHorizontal'] == 1.0
    assert messages['Location']['SpeedVertical'] == 2.0
    assert messages['Location']['Latitude'] == 50.0740381
    assert messages['Location']['Longitude'] == 14.4666297
    assert messages['Location']['AltitudeBaro'] == 111.0
    assert messages['Location']['AltitudeGeo'] == 112.0
    assert messages['Location']['HeightType'] == 0
    assert messages['Location']['Height'] == 108.5
    assert messages['Location']['HorizAccuracy'] == 0
    assert messages['Location']['VertAccuracy'] == 0
    assert messages['Location']['BaroAccuracy'] == 0
    assert messages['Location']['SpeedAccuracy'] == 0
    assert messages['Location']['TSAccuracy'] == 0
    assert int(messages['Location']['Timestamp']) == int(ts)
    
    assert messages['System'] is None
    assert messages['OperatorID'] is None