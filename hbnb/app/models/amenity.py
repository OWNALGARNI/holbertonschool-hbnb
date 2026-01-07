from typing import Any, Dict

from app.models.base_model import BaseModel


class Amenity(BaseModel):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = self._validate_name(name)

    def _validate_name(self, name: str) -> str:
        if not name or not isinstance(name, str):
            raise ValueError("Amenity name is required")
        return name.strip()

    def update(self, data: Dict[str, Any]) -> None:
        if "name" in data:
            data["name"] = self._validate_name(data["name"])
        super().update(data)
