import json
import re

import dateutil.parser
from cerberus import Validator


class MyNormalizer(Validator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _normalize_coerce_isotime(self, value):
        # return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
        return dateutil.parser.parse(value, ignoretz=True)

    def _normalize_coerce_nullable_isotime(self, value):
        if value is not None:
            # return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
            return dateutil.parser.parse(value, ignoretz=True)
        return value


def object_id(field, value, error):
    if not isinstance(value, str):
        return error(field, "must be string")
    if not re.match('[a-f0-9]{24}', value):
        error(field, "must be an object_id")


def uid_validator(field, value, error):
    if not re.match('^[a-z0-9]+$', value):
        error(field, "must be an uid format")


def json_data_validator(field, value, error):
    try:
        json.loads(value)
    except Exception:
        error(field, "must be an json format")


table_schema = {
    "start_ts": {"coerce": "isotime"},
    "end_ts": {"coerce": "isotime"}
}

filter_schema = {
    "fields": {
        "type": "list",
        "schema": {
            "type": "string",
            "allowed": ["app_name", "process", "room", "short_message", "full_message", "version", "time"],
            "nullable": False,
            "empty": False
        }
    },
    "start_ts": {"coerce": "isotime"},
    "end_ts": {"coerce": "isotime"}
}
