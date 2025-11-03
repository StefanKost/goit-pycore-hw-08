class InvalidPhone(Exception):
    def __init__(self, message="Invalid phone number"):
        self.message = message
        super().__init__(self.message)
