# OpenDroneID parser

Library for encoding and decoding Open Drone ID messages, as the format is defined in the ASTM F3411 Remote ID and the ASD-STAN prEN 4709-002 Direct Remote ID specifications.

## Installation
```sh
pip install git+https://github.com/dronetag/python-odid@dronetag
```

## Usage

```python
import dtpyodid.parser as dtparser

message = dtparser.parse(data)
print(message)
```