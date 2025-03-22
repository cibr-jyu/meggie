import numpy as np
import json
from meggie.utilities.serialization import serialize_dict, deserialize_dict


def test_serialization_deserialization():
    # A real-like test dict containing params with numpy arrays
    message_dict = {
        "params": {
            # np.array
            "freqs": np.array(
                [
                    5.0,
                    5.5,
                    6.0,
                    6.5,
                    7.0,
                    7.5,
                    8.0,
                    8.5,
                    9.0,
                    9.5,
                ]
            ),
            # int
            "decim": 1,
            # bool
            "subtract_evoked": False,
            # str
            "name": "TFR",
            # list
            "conditions": ["Somato"],
            # dict
            "dict_example": {"cats": "meow", "dogs": "woof"},
        }
    }

    # Serialize the dictionary
    serialized_message = serialize_dict(message_dict)
    serialized_json = json.dumps(serialized_message)

    # Simulate writing to and reading from a log file
    deserialized_json = json.loads(serialized_json)
    deserialized_message = deserialize_dict(deserialized_json)

    # Assertions to verify correctness
    for key in message_dict["params"]:
        original_value = message_dict["params"][key]
        deserialized_value = deserialized_message["params"][key]

        if isinstance(original_value, np.ndarray):
            assert isinstance(deserialized_value, np.ndarray)
            assert np.array_equal(original_value, deserialized_value)
            assert original_value.dtype == deserialized_value.dtype
            assert original_value.shape == deserialized_value.shape
        elif isinstance(original_value, list):
            assert isinstance(deserialized_value, list)
            assert original_value == deserialized_value
        else:
            assert type(original_value) is type(deserialized_value)
            assert original_value == deserialized_value
