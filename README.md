# OpenDroneID parser

Library for encoding and decoding Open Drone ID messages, as the format is defined in the ASTM F3411 Remote ID and the ASD-STAN prEN 4709-002 Direct Remote ID specifications.

## Installation
```sh
pip install firmware-pyodid
```

## Usage

```python
import dtpyodid
import json

message = dtpyodid.parse(data)
print(json.dumps(message))
```

## Development