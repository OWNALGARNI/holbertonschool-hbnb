from app.repositories.sqlalchemy_repository import SQLAlchemyRepository
from app.models.review import Review


class ReviewRepository(BaseRepository):
    def __init__(self):
        super().__init__(Review)
