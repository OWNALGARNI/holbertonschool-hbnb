import re
from typing import Any, Dict, Optional

from app.models.base_model import BaseModel


class User(BaseModel):
    def __init__(
        self,
        email: str,
        password: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
    ) -> None:
        super().__init__()

        self.email = self._validate_email(email)
        self.password = self._validate_password(password)
        self.first_name = first_name or ""
        self.last_name = last_name or ""

    def _validate_email(self, email: str) -> str:
        if not email or not isinstance(email, str):
            raise ValueError("Email is required")

        # simple email check (enough for this project)
        pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(pattern, email):
            raise ValueError("Invalid email format")

        return email.strip().lower()

    def _validate_password(self, password: str) -> str:
        if not password or not isinstance(password, str):
            raise ValueError("Password is required")
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters")
        return password

    def update(self, data: Dict[str, Any]) -> None:
        """
        Update user fields with validation where needed.
        """
        if "email" in data:
            data["email"] = self._validate_email(data["email"])
        if "password" in data:
            data["password"] = self._validate_password(data["password"])

        super().update(data)

    def to_dict(self) -> Dict[str, Any]:
        """
        Return user dict WITHOUT password.
        """
        result = super().to_dict()
        result.pop("password", None)
        return result
