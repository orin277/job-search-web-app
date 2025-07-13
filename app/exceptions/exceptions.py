

class UniqueConstraintException(Exception):
    def __init__(self, field: str, message: str | None = None):
        self.field = field
        self.message = message or f"Unique constraint failed for field '{field}'"
        super().__init__(self.message)