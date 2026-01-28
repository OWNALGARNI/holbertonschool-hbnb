"""
places.py - API namespace for managing Place resources in the HBnB application.
"""
from app.services import facade
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})


@api.route('/')
class PlaceList(Resource):
    """Resource class for handling the list of places."""
    
    @jwt_required()
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    def post(self):
        """Register a new place
        
        Requires JWT token. The owner_id will be set to the current user.
        """
        current_user_id = get_jwt_identity()
        data = api.payload
        
        # Set owner_id to current user (ignore any provided owner_id)
        data['owner_id'] = current_user_id
        
        required_fields = ['title', 'price', 'latitude', 'longitude']
        for field in required_fields:
            if field not in data or not data[field]:
                return {"message": f"{field} is required"}, 400
        
        try:
            place = facade.create_place(data)
            return place.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places
        
        Public endpoint - no authentication required.
        """
        places = facade.get_all_places()
        result = [place.to_dict() for place in places]
        return result, 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    """Resource class for handling a single place by ID."""
    
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID
        
        Public endpoint - no authentication required.
        """
        place = facade.get_place(place_id)
        if place is None:
            return {'message': 'Place not found'}, 404
        return place.to_dict(), 200

    @jwt_required()
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    def put(self, place_id):
        """Update a place's information
        
        Requires JWT token. Only the owner can update their place.
        """
        current_user_id = get_jwt_identity()
        
        place = facade.get_place(place_id)
        if not place:
            return {'message': 'Place not found'}, 404
        
        # Check ownership
        if place.owner_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403
        
        data = api.payload
        # Prevent changing owner_id
        data.pop('owner_id', None)
        
        try:
            updated_place = facade.update_place(place_id, data)
            if not updated_place:
                return {'message': 'Place not found'}, 404
            return {
                "message": "Place updated successfully",
                "place": updated_place.to_dict()
            }, 200
        except ValueError as e:
            return {'message': str(e)}, 400
    
    @jwt_required()
    @api.response(200, 'Place deleted successfully')
    @api.response(404, 'Place not found')
    @api.response(403, 'Unauthorized action')
    def delete(self, place_id):
        """Delete a place
        
        Requires JWT token. Only the owner can delete their place.
        """
        current_user_id = get_jwt_identity()
        
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        # Check ownership
        if place.owner_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403
        
        success = facade.delete_place(place_id)
        if success:
            return {'message': 'Place deleted successfully'}, 200
        return {'error': 'Failed to delete place'}, 400