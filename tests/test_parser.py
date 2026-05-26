import dtpyodid

def test_parse():
    data = b"B\004}I\306\035\340\016\207\010\001\000\031\000\000\000\000\020v\n\263\307\222\r\000"
    print(dtpyodid.parse(data))
    
def test_parse_encoding_error():
    data = b"\x02\x10\x12\xbc\xf3\xabW\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    print(dtpyodid.parse(data))