from flask import request, abort
from dataclasses import fields

def parse_dataclass(cls):
    data = request.get_json()

    if data is None:
        abort(400, "Invalid or missing JSON body")

    try:
        field_names = {f.name for f in fields(cls)}
        filtered = {k: v for k, v in data.items() if k in field_names}
        return cls(**filtered)
    except TypeError as e:
        abort(400, f"Invalid request body: {e}")