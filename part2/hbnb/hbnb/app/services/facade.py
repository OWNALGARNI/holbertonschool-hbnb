#!/usr/bin/env python3
from ..persistence.repository import InMemoryRepository
from ..models.review import Review
from ..models.place import Place
from ..models.user import User


class HBnBFacade:
    def __init__(self) -> None:
        # Repository منفصل لكل كيان
        self.users_repo = InMemoryRepository()
        self.places_repo = InMemoryRepository()
        self.reviews_repo = InMemoryRepository()
        self.amenities_repo = InMemoryRepository()

    # ---------- Users ----------
    def create_user(self, data: dict) -> User:
        user = User(**data)
        self.users_repo.add(user)
        return user

    def get_user(self, user_id: str) -> User | None:
        return self.users_repo.get(user_id)

    def get_user_by_email(self, email: str) -> User | None:
        """Get user by email address"""
        for user in self.users_repo.get_all():
            if user.email == email.lower().strip():
                return user
        return None

    def get_all_users(self):
        return self.users_repo.get_all()

    def update_user(self, user_id: str, data: dict) -> User | None:
        """Update user data"""
        return self.users_repo.update(user_id, data)

    def delete_user(self, user_id: str) -> bool:
        """Delete user by ID"""
        return self.users_repo.delete(user_id)

    # ---------- Places ----------
    def create_place(self, data: dict) -> Place:
        place = Place(**data)
        self.places_repo.add(place)
        return place

    def get_place(self, place_id: str) -> Place | None:
        return self.places_repo.get(place_id)

    def get_all_places(self):
        return self.places_repo.get_all()

    def update_place(self, place_id: str, data: dict) -> Place | None:
        """Update place data"""
        return self.places_repo.update(place_id, data)

    def delete_place(self, place_id: str) -> bool:
        """Delete place by ID"""
        return self.places_repo.delete(place_id)

    # ---------- Reviews ----------
    def create_review(self, data: dict) -> Review:
        review = Review(**data)
        self.reviews_repo.add(review)
        return review

    def get_review(self, review_id: str) -> Review | None:
        return self.reviews_repo.get(review_id)

    def get_all_reviews(self):
        return self.reviews_repo.get_all()

    def update_review(self, review_id: str, data: dict) -> Review | None:
        # لازم يكون عندك update داخل InMemoryRepository
        return self.reviews_repo.update(review_id, data)

    def delete_review(self, review_id: str) -> bool:
        return self.reviews_repo.delete(review_id)

    def get_reviews_by_place(self, place_id: str):
        return [
            r for r in self.get_all_reviews()
            if getattr(r, "place_id", None) == place_id
        ]

    # ---------- Amenities ----------
    def create_amenity(self, data: dict):
        """Create a new amenity"""
        from ..models.amenity import Amenity
        amenity = Amenity(**data)
        self.amenities_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id: str):
        """Get amenity by ID"""
        return self.amenities_repo.get(amenity_id)

    def get_all_amenities(self):
        """Get all amenities"""
        return self.amenities_repo.get_all()

    def update_amenity(self, amenity_id: str, data: dict):
        """Update amenity data"""
        return self.amenities_repo.update(amenity_id, data)

    def delete_amenity(self, amenity_id: str) -> bool:
        """Delete amenity by ID"""
        return self.amenities_repo.delete(amenity_id)


# ✅ هذا أهم سطر لحل مشكلة ImportError
# لأن الـ API يستورد: HbnbFacade
HbnbFacade = HBnBFacade
