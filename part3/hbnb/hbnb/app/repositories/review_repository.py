from part3.repositories.base_repository import BaseRepository
from part3.models.review import Review


class ReviewRepository(BaseRepository):
    def __init__(self):
        super().__init__(Review)
