class ConflictError(Exception):
    def __init__(self, entity="Record"):
        self.message = f"{entity} already exists"
        super().__init__(self.message)
