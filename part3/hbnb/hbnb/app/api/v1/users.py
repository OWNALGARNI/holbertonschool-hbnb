"""
This module defines the RESTful routes for user-related operations such as:
- Creating a new user
- Listing all users
- Retrieving a user by ID
- Updating a user

The endpoints are exposed under the '/users/' namespace using Flask-RESTx.
"""

from app.services import facade
from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True,
                                description='First name of the user'),
    'last_name': fields.String(required=True,
                               description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})


@api.route('/')
class UserList(Resource):
    """Handles operations related to the collection of users."""
    
    @api.expect(user_model)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user.

        Returns:
            tuple: A dictionary with the user's information and a 201 status
            code if successful.
            If the email is already registered, returns an error dictionary
            and 400 status code.
        """
        user_data = api.payload or {}
        required_fields = ['first_name', 'last_name', 'email', 'password']
        for field in required_fields:
            if field not in user_data:
                return {'error': f'Missing required field: {field}'}, 400

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception:
            return {'error': 'Internal server error'}, 500

        return {'id': new_user.id, 'first_name': new_user.first_name,
                'last_name': new_user.last_name, 'email': new_user.email}, 201

    @jwt_required()
    def get(self):
        """Retrieve a list of all registered users.
        
        Requires JWT token for authentication.

        Returns:
            tuple: A list of dictionaries representing users, and a 200
            status code.
        """
        users = facade.get_all_users()
        return [{
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        } for user in users], 200


@api.route('/<user_id>')
class UserResource(Resource):
    """Handles operations related to a specific user identified by user ID."""

    @jwt_required()
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID.
        
        Requires JWT token for authentication.

        Args:
            user_id (str): The unique identifier of the user.

        Returns:
            tuple: A dictionary with user information and a 200 status code
            if found.
            If not found, returns an error dictionary and 404 status code.
        """
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name,
                'last_name': user.last_name, 'email': user.email}, 200

    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(200, 'Successfully update')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    def put(self, user_id):
        """Update user information.
        
        Requires JWT token for authentication.
        Users can only update their own information.
        Email and password cannot be updated through this endpoint.

        Args:
            user_id (str): The unique identifier of the user.

        Returns:
            tuple: A dictionary with updated user data and a 200 status code
            if successful.
            If the user is not found or update fails, returns an error
            dictionary.
        """
        current_user_id = get_jwt_identity()
        
        # Check if user is updating their own profile
        if current_user_id != user_id:
            return {'error': 'Unauthorized action'}, 403
        
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        data = request.get_json()
        
        # Prevent updating email and password
        data.pop('email', None)
        data.pop('password', None)
        
        updated_user = facade.update_user(user_id, data)

        if not updated_user:
            return {'error': 'Update failed'}, 400

        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email
        }, 200