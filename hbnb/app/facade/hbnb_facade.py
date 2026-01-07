from app.persistence.repository import InMemoryRepository


class HBnBFacade:
    def __init__(self) -> None:
        self.repo = InMemoryRepository
    