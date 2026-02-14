"""
Authentication endpoints for user login
"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade

api = Namespace('auth', description='Authentication operations')

# Login model for input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})


@api.route('/login')
class Login(Resource):
    """Handle user login and JWT token generation"""
    
    @api.expect(login_model)
    @api.response(200, 'Login successful')
    @api.response(401, 'Invalid credentials')
    def post(self):
        """Authenticate user and return JWT token
        
        Returns:
            dict: Contains access_token on success
            dict: Contains error message on failure
        """
        credentials = api.payload
        
        # Validate required fields
        if not credentials or 'email' not in credentials or 'password' not in credentials:
            return {'error': 'Email and password are required'}, 400
        
        email = credentials['email']
        password = credentials['password']
        
        # Debug logging
        print(f"🔍 Login attempt: email='{email}', password='{password}'")
        
        # Get user by email
        user = facade.get_user_by_email(email)
        
        print(f"🔍 User found: {user is not None}")
        if user:
            print(f"🔍 User email: '{user.email}'")
            print(f"🔍 Password verification: {user.verify_password(password)}")
        
        if not user:
            return {'error': 'Invalid credentials'}, 401
        
        # Verify password
        if not user.verify_password(password):
            return {'error': 'Invalid credentials'}, 401
        
        # Create JWT token with user claims
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={
                'email': user.email,
                'is_admin': user.is_admin
            }
        )
        
        return {
            'access_token': access_token
        }, 200