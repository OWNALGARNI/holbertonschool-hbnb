from app.extensions import db
from app.models.base_model import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.models.amenity import place_amenity


class Place(BaseModel):
    __tablename__ = "places"

    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(1024))
    price = db.Column(db.Integer, nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    owner_id = db.Column(
        db.String(60),
        ForeignKey("users.id"),
        nullable=False
    )

    reviews = relationship(
        "Review",
        backref="place",
        cascade="all, delete-orphan"
    )

    amenities = relationship(
        "Amenity",
        secondary=place_amenity,
        back_populates="places"
    )
