from pyopendroneid import opendroneid

import dtpyodid


def test_basic_id():
    og_basic_id = opendroneid.ODID_BasicID_data(
        UAType=opendroneid.ODID_UATYPE_GROUND_OBSTACLE,
        IDType=opendroneid.ODID_IDTYPE_NONE,
        UASID=b"SCOUT01")
    og_basic_id_encoded = opendroneid.ODID_BasicID_encoded()
    opendroneid.encodeBasicIDMessage(og_basic_id_encoded, og_basic_id)
    og_basic_id_bytes = bytes(og_basic_id_encoded)

    new_basic_id_bytes = dtpyodid.BasicID(ua_type=opendroneid.ODID_UATYPE_GROUND_OBSTACLE,
        id_type=opendroneid.ODID_IDTYPE_NONE,
        uas_id="SCOUT01"
    ).pack()

    assert og_basic_id_bytes == new_basic_id_bytes