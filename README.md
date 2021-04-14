# UA-EDS-API

Provides easy interface for making REST requests to University of Arizona Box file storage.

## Motivation

To make a python API that could generically interact with the REST architecture of Box.

## Code Example

```python
from ua_box_api import ua_box_api

box_api = ua_eds_api.BoxApi(config)

items = box_api.get_all_items(10)
```

## Installation

pip install --user ua-box-api

## Credits

[RyanJohannesBland](https://github.com/RyanJohannesBland)
[EtienneThompson](https://github.com/EtienneThompson)

## License

MIT
