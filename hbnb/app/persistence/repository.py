import uuid
from typing import Dict, List, TypeVar, Generic

T = TypeVar("T")


class InMemoryRepository(Generic[T]):
    def __init__(self):
        self._storage: Dict[str, T] = {}

    def add(self, obj: T) -> None:
        self._storage[obj.id] = obj

    def get(self, obj_id: str) -> T | None:
        return self._storage.get(obj_id)

    def get_all(self) -> List[T]:
        return list(self._storage.values())

    def update(self, obj_id: str, data: dict) -> T | None:
        obj = self.get(obj_id)
        if obj:
            obj.update(data)
        return obj

    def delete(self, obj_id: str) -> bool:
        return self._storage.pop(obj_id, None) is not None
