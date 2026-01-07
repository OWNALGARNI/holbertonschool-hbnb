import uuid
from datetime import datetime
from typing import Any, Dict


class BaseModel:
    def __init__(self) -> None:
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def update(self, data: Dict[str, Any]) -> None:
        """
        Update allowed attributes from a dict and refresh updated_at.
        """
        for key, value in data.items():
            # prevent updating internal fields directly
            if key in {"id", "created_at", "updated_at"}:
                continue
            if hasattr(self, key):
                setattr(self, key, value)

        self.updated_at = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert object to dict for JSON responses.
        """
        result = self.__dict__.copy()
        result["created_at"] = self.created_at.isoformat()
        result["updated_at"] = self.updated_at.isoformat()
        return result
