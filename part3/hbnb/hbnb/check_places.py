"""Check places in the database"""
from app import create_app
from app.models.place import Place

app = create_app()

with app.app_context():
    places = Place.query.all()
    print(f"\n{'='*60}")
    print(f"Total places in database: {len(places)}")
    print(f"{'='*60}\n")
    
    if not places:
        print("⚠️ No places found in database!")
        print("You need to add some places first.")
    else:
        for place in places:
            print(f"Place ID: {place.id}")
            print(f"Title: {place.title}")
            print(f"Price: ${place.price}/night")
            print(f"Owner ID: {place.owner_id}")
            print(f"Description: {place.description[:50]}..." if place.description and len(place.description) > 50 else f"Description: {place.description}")
            print("-" * 60)
