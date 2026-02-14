"""
This module defines the RESTful routes for user-related operations such as:
- Creating a new user
- Listing all users
- Retrieving a user by ID
- Updating a user

The endpoints are exposed under the '/users/' namespace using Flask-RESTx.
"""

from flask import request
from flask_restx import Namespace, Resource, fields

# ✅ import نسبي صحيح
from ...services import facade

# ✅ لازم هذا الاسم يكون موجود عشان __init__.py يستورده
users_ns = Namespace("users", description="User operations")

# ✅ نخلي api كاسم بديل عشان ما نكسر بقية الكود في الملف
api = users_ns


# --- Swagger model (input) -------------------------------------------------
user_model = api.model(
    "User",
    {
        "first_name": fields.String(required=True, description="First name of the user"),
        "last_name": fields.String(required=True, description="Last name of the user"),
        "email": fields.String(required=True, description="Email of the user"),
        "password": fields.String(required=True, description="Password of the user"),
    },
)


def _get_all_users():
    """
    Compatibility helper: some projects name it get_all_users, others get_all_user.
    """
    if hasattr(facade, "get_all_users"):
        return facade.get_all_users()
    if hasattr(facade, "get_all_user"):
        return facade.get_all_user()
    # fallback: common naming
    if hasattr(facade, "list_users"):
        return facade.list_users()
    raise AttributeError("Facade is missing a method to list users.")


@api.route("/")
class UserList(Resource):
    """Handles operations related to the collection of users."""

    @api.expect(user_model, validate=True)
    @api.response(201, "User successfully created")
    @api.response(400, "Email already registered")
    @api.response(400, "Invalid input data")
    def post(self):
        """Register a new user."""
        user_data = api.payload or {}

        required_fields = ["first_name", "last_name", "email", "password"]
        for field in required_fields:
            if field not in user_data or user_data[field] in (None, ""):
                return {"error": f"Missing required field: {field}"}, 400

        # تحقق من وجود الإيميل
        if hasattr(facade, "get_user_by_email"):
            existing_user = facade.get_user_by_email(user_data["email"])
            if existing_user:
                return {"error": "Email already registered"}, 400

        try:
            new_user = facade.create_user(user_data)
        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception:
            return {"error": "Internal server error"}, 500

        return (
            {
                "id": new_user.id,
                "first_name": new_user.first_name,
                "last_name": new_user.last_name,
                "email": new_user.email,
            },
            201,
        )

    @api.response(200, "Users retrieved successfully")
    def get(self):
        """Retrieve a list of all registered users."""
        users = _get_all_users()
        return (
            [
                {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                }
                for user in users
            ],
            200,
        )


@api.route("/<string:user_id>")
class UserResource(Resource):
    """Handles operations related to a specific user identified by user ID."""

    @api.response(200, "User details retrieved successfully")
    @api.response(404, "User not found")
    def get(self, user_id):
        """Get user details by ID."""
        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404

        return (
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            },
            200,
        )

    @api.expect(user_model, validate=True)
    @api.response(200, "Successfully updated")
    @api.response(400, "Invalid input data")
    @api.response(404, "User not found")
    def put(self, user_id):
        """Update user information."""
        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404

        data = request.get_json(silent=True) or {}

        # بعض المشاريع تسميها update_user بدل put_user
        if hasattr(facade, "put_user"):
            updated_user = facade.put_user(user_id, data)
        elif hasattr(facade, "update_user"):
            updated_user = facade.update_user(user_id, data)
        else:
            return {"error": "Update method not implemented in facade"}, 500

        if not updated_user:
            return {"error": "Update failed"}, 400

        return (
            {
                "id": updated_user.id,
                "first_name": updated_user.first_name,
                "last_name": updated_user.last_name,
                "email": updated_user.email,
            },
            200,
        )