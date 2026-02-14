"""
Initialize database with sample data
"""
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review

def init_database():
    app = create_app()
    
    with app.app_context():
        # Drop all tables and recreate
        db.drop_all()
        db.create_all()
        
        # Create admin user
        admin = User(
            email="admin@test.com",
            first_name="Admin",
            last_name="User",
            is_admin=True
        )
        admin.hash_password("admin123")
        db.session.add(admin)
        db.session.commit()
        print(f"✅ Admin user created: {admin.email}")
        
        # Create regular user
        regular_user = User(
            email="user@test.com",
            first_name="John",
            last_name="Doe",
            is_admin=False
        )
        regular_user.hash_password("user123")
        db.session.add(regular_user)
        db.session.commit()
        print(f"✅ Regular user created: {regular_user.email}")
        
        # Create amenities
        amenities_data = [
            "WiFi",
            "Air conditioning",
            "Parking",
            "Swimming pool",
            "Gym",
            "Kitchen",
            "TV",
            "Heating"
        ]
        
        amenities = []
        for amenity_name in amenities_data:
            amenity = Amenity(name=amenity_name)
            db.session.add(amenity)
            amenities.append(amenity)
        
        db.session.commit()
        print(f"✅ {len(amenities)} amenities created")
        
        # Create places
        places_data = [
            {
                "title": "Cozy Beach House",
                "description": "Beautiful beach house with ocean view",
                "price": 150.0,
                "latitude": 34.0522,
                "longitude": -118.2437,
                "owner_id": admin.id,
                "amenities": [amenities[0], amenities[1], amenities[2]]
            },
            {
                "title": "Modern City Apartment",
                "description": "Stylish apartment in the heart of the city",
                "price": 120.0,
                "latitude": 40.7128,
                "longitude": -74.0060,
                "owner_id": admin.id,
                "amenities": [amenities[0], amenities[1], amenities[6]]
            },
            {
                "title": "Mountain Cabin Retreat",
                "description": "Peaceful cabin surrounded by nature",
                "price": 100.0,
                "latitude": 39.7392,
                "longitude": -104.9903,
                "owner_id": regular_user.id,
                "amenities": [amenities[0], amenities[5], amenities[7]]
            },
            {
                "title": "Luxury Villa",
                "description": "Spacious villa with private pool",
                "price": 300.0,
                "latitude": 25.7617,
                "longitude": -80.1918,
                "owner_id": admin.id,
                "amenities": [amenities[0], amenities[1], amenities[3], amenities[4]]
            }
        ]
        
        places = []
        for place_data in places_data:
            place = Place(
                title=place_data["title"],
                description=place_data["description"],
                price=place_data["price"],
                latitude=place_data["latitude"],
                longitude=place_data["longitude"],
                owner_id=place_data["owner_id"]
            )
            place.amenities = place_data["amenities"]
            db.session.add(place)
            places.append(place)
        
        db.session.commit()
        print(f"✅ {len(places)} places created")
        
        # Create reviews
        reviews_data = [
            {
                "text": "Amazing place! Highly recommend.",
                "rating": 5,
                "place": places[0],
                "user": regular_user
            },
            {
                "text": "Great location but could be cleaner.",
                "rating": 4,
                "place": places[0],
                "user": regular_user
            },
            {
                "text": "Perfect for a weekend getaway!",
                "rating": 5,
                "place": places[1],
                "user": regular_user
            },
            {
                "text": "Loved the mountain views!",
                "rating": 5,
                "place": places[2],
                "user": admin
            },
            {
                "text": "Luxury at its finest. Worth every penny.",
                "rating": 5,
                "place": places[3],
                "user": regular_user
            }
        ]
        
        for review_data in reviews_data:
            review = Review(
                text=review_data["text"],
                rating=review_data["rating"],
                place_id=review_data["place"].id,
                user_id=review_data["user"].id
            )
            db.session.add(review)
        
        db.session.commit()
        print(f"✅ {len(reviews_data)} reviews created")
        
        print("\n" + "="*50)
        print("🎉 Database initialized successfully!")
        print("="*50)
        print("\n📋 Test Credentials:")
        print(f"   Admin: admin@test.com / admin123")
        print(f"   User:  user@test.com / user123")
        print("="*50)

if __name__ == '__main__':
    init_database()
