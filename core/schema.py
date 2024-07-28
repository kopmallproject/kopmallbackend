from ninja import Schema

class SUCCESS_200OUTSCHEMA(Schema):
    message: str


class SUCCESS_201OUTSCHEMA(Schema):
    message: str


class ERROR_403OUTSCHEMA(Schema):
    error: str


class NOTFOUND_404OUTSCHEMA(Schema):
    message: str
