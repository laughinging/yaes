class InvalidRequestError(Exception):
    def __init__(self):
        message = "The email request is invalid."
        super(InvalidRequestError, self).__init__(message)
        self.status_code = 400

class ServerError(Exception):
    def __init__(self):
        message = "Service not available."
        super(ServerError, self).__init__(message)
        self.status_code = 500
