class ClientError(Exception):
    def __init__(self, description=None):
        message = "An error occurred with client."
        if description is None:
            description = "No further information."
        super(ClientError, self).__init__(message + description)
        self.status_code = 400

class ProviderServerError(Exception):
    def __init__(self, description=None):
        message = "An error occurred with email server provider."
        if description is None:
            description = "No further information."
        super(ProviderServerError, self).__init__(message + description)
        self.status_code = status_code
        self.status_code = 500
