import http


class AppError(Exception):

    def __init__(self, message, status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR, payload=None):
        super().__init__()
        self.message = message
        self.payload = payload
        self.status_code = status_code

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class InvalidAPIUsage(AppError):
    _DEFAULT_STATUS_CODE = http.HTTPStatus.BAD_REQUEST

    def __init__(self, message, status_code=None, payload=None):
        status_code = status_code or self._DEFAULT_STATUS_CODE
        super().__init__(message, status_code=status_code, payload=payload)
