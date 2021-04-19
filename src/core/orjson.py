import orjson

from pydantic import BaseModel


def _orjson_dumps(val, *, default):
    # For repair error like this -> https://github.com/samuelcolvin/pydantic/issues/1150
    # File "pydantic/main.py", line 506, in pydantic.main.BaseModel.json TypeError: Expected unicode, got bytes
    return orjson.dumps(val, default=default).decode()


class BaseModelOrjson(BaseModel):
    class Config:
        # Change standart json to faster orjson
        json_loads = orjson.loads
        json_dumps = _orjson_dumps
