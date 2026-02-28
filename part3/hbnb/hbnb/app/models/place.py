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
    country = db.Column(db.String(100))

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

    def to_dict(self):
        """Override to_dict to include amenities, reviews, and owner info"""
        data = super().to_dict()
        
        # Add owner information
        if hasattr(self, 'owner') and self.owner:
            data['owner'] = {
                'id': self.owner.id,
                'first_name': self.owner.first_name,
                'last_name': self.owner.last_name,
                'email': self.owner.email
            }
        
        # Add amenities (just id and name)
        data['amenities'] = [
            {'id': amenity.id, 'name': amenity.name}
            for amenity in self.amenities
        ]
        
        # Add reviews (with user info)
        data['reviews'] = []
        for review in self.reviews:
            review_data = review.to_dict()
            # Add user info if available
            if review.user:
                review_data['user'] = {
                    'id': review.user.id,
                    'first_name': review.user.first_name,
                    'last_name': review.user.last_name,
                    'email': review.user.email
                }
            data['reviews'].append(review_data)
        
        return data
