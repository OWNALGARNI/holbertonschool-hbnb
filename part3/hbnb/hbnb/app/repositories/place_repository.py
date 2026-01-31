from part3.repositories.base_repository import BaseRepository
from part3.models.place import Place


class PlaceRepository(BaseRepository):
    def __init__(self):
        super().__init__(Place)
