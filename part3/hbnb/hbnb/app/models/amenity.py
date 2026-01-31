from part3 import db
from part3.models.base_model import BaseModel
from sqlalchemy.orm import relationship

# Association table (Place <-> Amenity)
place_amenity = db.Table(
    "place_amenity",
    db.Column(
        "place_id",
        db.String(60),
        db.ForeignKey("places.id"),
        primary_key=True
    ),
    db.Column(
        "amenity_id",
        db.String(60),
        db.ForeignKey("amenities.id"),
        primary_key=True
    )
)


class Amenity(BaseModel):
    __tablename__ = "amenities"

    name = db.Column(db.String(128), nullable=False, unique=True)

    places = relationship(
        "Place",
        secondary=place_amenity,
        back_populates="amenities"
    )
