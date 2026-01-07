from typing import Any, Dict, List

from app.models.base_model import BaseModel


class Place(BaseModel):
    def __init__(
        self,
        name: str,
        owner_id: str,
        price: float,
        latitude: float,
        longitude: float,
        description: str = "",
        amenity_ids: List[str] | None = None,
    ) -> None:
        super().__init__()

        self.name = self._validate_name(name)
        self.owner_id = self._validate_owner(owner_id)
        self.price = self._validate_price(price)
        self.latitude = self._validate_latitude(latitude)
        self.longitude = self._validate_longitude(longitude)

        self.description = description or ""
        self.amenity_ids = amenity_ids or []

    # -------- validations --------

    def _validate_name(self, name: str) -> str:
        if not name or not isinstance(name, str):
            raise ValueError("Place name is required")
        return name.strip()

    def _validate_owner(self, owner_id: str) -> str:
        if not owner_id or not isinstance(owner_id, str):
            raise ValueError("Owner id is required")
        return owner_id

    def _validate_price(self, price: float) -> float:
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Price must be a positive number")
        return float(price)

    def _validate_latitude(self, latitude: float) -> float:
        if not isinstance(latitude, (int, float)):
            raise ValueError("Latitude must be a number")
        if latitude < -90 or latitude > 90:
            raise ValueError("Latitude must be between -90 and 90")
        return float(latitude)

    def _validate_longitude(self, longitude: float) -> float:
        if not isinstance(longitude, (int, float)):
            raise ValueError("Longitude must be a number")
        if longitude < -180 or longitude > 180:
            raise ValueError("Longitude must be between -180 and 180")
        return float(longitude)

    # -------- update --------

    def update(self, data: Dict[str, Any]) -> None:
        if "name" in data:
            data["name"] = self._validate_name(data["name"])
        if "price" in data:
            data["price"] = self._validate_price(data["price"])
        if "latitude" in data:
            data["latitude"] = self._validate_latitude(data["latitude"])
        if "longitude" in data:
            data["longitude"] = self._validate_longitude(data["longitude"])

        super().update(data)
