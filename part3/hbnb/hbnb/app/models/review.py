from part3 import db
from part3.models.base_model import BaseModel
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
