class InvalidBirthday(Exception):
    def __init__(self, message="Invalid birthday format"):
        self.message = message
        super().__init__(self.message)
