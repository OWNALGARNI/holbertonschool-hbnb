from app.extensions import db
from app.models.base_model import BaseModel
from sqlalchemy.orm import relationship
import bcrypt


class User(BaseModel):
    __tablename__ = "users"

    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    is_admin = db.Column(db.Boolean, default=False)

    places = relationship(
        "Place",
        backref="owner",
        cascade="all, delete-orphan"
    )

    reviews = relationship(
        "Review",
        backref="author",
        cascade="all, delete-orphan"
    )

    def hash_password(self, password: str) -> None:
        """Hash the user's password"""
        self.password = bcrypt.hashpw(
            password.encode('utf-8'), 
            bcrypt.gensalt()
        ).decode('utf-8')

    def verify_password(self, password: str) -> bool:
        """Verify a password against the hash"""
        return bcrypt.checkpw(
            password.encode('utf-8'), 
            self.password.encode('utf-8')
        )
