from app.repositories.sqlalchemy_repository import SQLAlchemyRepository
from app.models.place import Place


class PlaceRepository(BaseRepository):
    def __init__(self):
        super().__init__(Place)
