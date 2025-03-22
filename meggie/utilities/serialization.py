"""Contains helpers to serialize and deserialize action params without losing types."""

import numpy as np


def serialize_leaf(value):
    """Serialize a leaf node in the dictionary."""

    if isinstance(value, np.ndarray):
        return {
            "is_value": True,
            "value": value.tolist(),
            "type": "numpy.ndarray",
            "dtype": str(value.dtype),
            "shape": value.shape,
        }
    elif isinstance(value, (int, float, bool, str, list)):
        return {"is_value": True, "value": value, "type": type(value).__name__}
    else:
        # Handle additional types as needed
        return {"is_value": True, "value": value, "type": type(value).__name__}


def serialize_dict(dct):
    """Recursively serialize a dictionary, converting non-dict leaves to structured dicts."""

    if isinstance(dct, dict):
        return {k: serialize_dict(v) for k, v in dct.items()}
    else:
        return serialize_leaf(dct)


def deserialize_leaf(leaf):
    """Deserialize a serialized leaf node back to its original type."""

    if "is_value" in leaf and leaf["is_value"]:
        value_type = leaf["type"]
        if value_type == "numpy.ndarray":
            return np.array(leaf["value"], dtype=leaf["dtype"]).reshape(leaf["shape"])
        elif value_type == "int":
            return int(leaf["value"])
        elif value_type == "float":
            return float(leaf["value"])
        elif value_type == "bool":
            return bool(leaf["value"])
        elif value_type == "str":
            return str(leaf["value"])
        elif value_type == "list":
            return list(leaf["value"])
        else:
            # Handle additional types as needed
            return leaf["value"]
    return leaf


def deserialize_dict(dct):
    """Recursively deserialize a dictionary, converting structured dicts back to original types."""

    if isinstance(dct, dict):
        if "is_value" in dct and dct["is_value"]:
            return deserialize_leaf(dct)
        else:
            return {k: deserialize_dict(v) for k, v in dct.items()}
    else:
        # Be brave and return the value as-is for backwards compatibility
        return dct
