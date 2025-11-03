class NotFoundError(Exception):
    def __init__(self, entity="Record"):
        self.message = f"{entity} not found"
        super().__init__(self.message)
