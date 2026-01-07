from typing import Any, Dict

from app.models.base_model import BaseModel


class Review(BaseModel):
    def __init__(self, text: str, user_id: str, place_id: str) -> None:
        super().__init__()

        self.text = self._validate_text(text)
        self.user_id = self._validate_id(user_id, "user_id")
        self.place_id = self._validate_id(place_id, "place_id")

    def _validate_text(self, text: str) -> str:
        if not text or not isinstance(text, str):
            raise ValueError("Review text is required")
        text = text.strip()
        if len(text) == 0:
            raise ValueError("Review text cannot be empty")
        return text

    def _validate_id(self, value: str, field_name: str) -> str:
        if not value or not isinstance(value, str):
            raise ValueError(f"{field_name} is required")
        return value

    def update(self, data: Dict[str, Any]) -> None:
        if "text" in data:
            data["text"] = self._validate_text(data["text"])

        # prevent changing relationships via update
        data.pop("user_id", None)
        data.pop("place_id", None)

        super().update(data)
