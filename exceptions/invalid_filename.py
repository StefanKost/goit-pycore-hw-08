class InvalidFilename(Exception):
    def __init__(self, message="Invalid filename"):
        self.message = message
        super().__init__(self.message)
