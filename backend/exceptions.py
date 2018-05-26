class InvalidRequestError(Exception):
    def __init__(self, description):
        message = "Invalid Request." 
        if description is None:
            description = "No further information."
        super(InvalidRequestError, self).__init__(message + description)
        self.status_code = 400

class ServerError(Exception):
    def __init__(self):
        super(ServerError, self).__init__("Server not available, try later.")
        self.status_code = 500

