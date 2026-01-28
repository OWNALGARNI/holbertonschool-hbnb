"""
Module reviews.py - RESTful API endpoints for reviews
"""
from app.services import facade
from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})


@api.route('/')
class ReviewList(Resource):
    """Handles HTTP requests for creating and retrieving reviews."""
    
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    def post(self):
        """Create a new review
        
        Requires JWT token. Users cannot review their own places or review the same place twice.
        """
        current_user_id = get_jwt_identity()
        review_data = api.payload
        
        # Set user_id to current user
        review_data['user_id'] = current_user_id
        
        place_id = review_data.get('place_id')
        if not place_id:
            return {'error': 'place_id is required'}, 400
        
        # Check if place exists
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        # Check if user is trying to review their own place
        if place.owner_id == current_user_id:
            return {'error': 'You cannot review your own place'}, 403
        
        # Check if user has already reviewed this place
        existing_reviews = facade.get_reviews_by_place(place_id)
        for review in existing_reviews:
            if review.user_id == current_user_id:
                return {'error': 'You have already reviewed this place'}, 400
        
        try:
            new_review = facade.create_review(review_data)
            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': new_review.user_id,
                'place_id': new_review.place_id,
                'created_at': new_review.created_at.isoformat(),
                'updated_at': new_review.updated_at.isoformat()
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve all reviews
        
        Public endpoint - no authentication required.
        """
        reviews = facade.get_all_reviews()
        return [{
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id,
            'place_id': review.place_id,
            'created_at': review.created_at.isoformat(),
            'updated_at': review.updated_at.isoformat()
        } for review in reviews], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    """Handles operations on a single review resource by ID."""
    
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get a review by its ID
        
        Public endpoint - no authentication required.
        """
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id,
            'place_id': review.place_id,
            'created_at': review.created_at.isoformat(),
            'updated_at': review.updated_at.isoformat()
        }, 200

    @jwt_required()
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    def put(self, review_id):
        """Update an existing review
        
        Requires JWT token. Only the review author can update their review.
        """
        current_user_id = get_jwt_identity()
        
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        
        # Check ownership
        if review.user_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403
        
        data = request.get_json()
        # Prevent changing user_id and place_id
        data.pop('user_id', None)
        data.pop('place_id', None)
        
        try:
            updated_review = facade.update_review(review_id, data)
            if not updated_review:
                return {'error': 'Update failed'}, 400
            
            return {
                'id': updated_review.id,
                'text': updated_review.text,
                'rating': updated_review.rating,
                'user_id': updated_review.user_id,
                'place_id': updated_review.place_id,
                'created_at': updated_review.created_at.isoformat(),
                'updated_at': updated_review.updated_at.isoformat()
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    def delete(self, review_id):
        """Delete a review by its ID
        
        Requires JWT token. Only the review author can delete their review.
        """
        current_user_id = get_jwt_identity()
        
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        
        # Check ownership
        if review.user_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403
        
        success = facade.delete_review(review_id)
        if success:
            return {'message': 'Review deleted successfully'}, 200
        return {'error': 'Failed to delete review'}, 400


@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    """Handles retrieval of reviews related to a specific place."""
    
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place
        
        Public endpoint - no authentication required.
        """
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        reviews = facade.get_reviews_by_place(place_id)
        return [{
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id,
            'place_id': review.place_id,
            "created_at": review.created_at.isoformat(),
            "updated_at": review.updated_at.isoformat()
        } for review in reviews], 200