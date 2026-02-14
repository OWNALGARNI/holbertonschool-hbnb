from app.extensions import db
from app.models.base_model import BaseModel
from sqlalchemy import ForeignKey


class Review(BaseModel):
    __tablename__ = "reviews"

    text = db.Column(db.String(1024), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    place_id = db.Column(
        db.String(60),
        ForeignKey("places.id"),
        nullable=False
    )

    user_id = db.Column(
        db.String(60),
        ForeignKey("users.id"),
        nullable=False
    )
