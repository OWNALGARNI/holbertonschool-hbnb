from app.extensions import db
from app.models.base_model import BaseModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


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

    # Relationship to access user data
    user = relationship("User", backref="user_reviews", foreign_keys=[user_id])

    def to_dict(self):
        """Override to_dict to include user information"""
        data = super().to_dict()
        
        # Add user information
        if hasattr(self, 'user') and self.user:
            data['user'] = {
                'id': self.user.id,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
                'email': self.user.email
            }
        
        return data
