from flask import request
from flask_restx import Namespace, Resource, fields

from app.facade import facade
from app.models.user import User

users_ns = Namespace("users", description="User operations")

# ---------- Swagger Models ----------

# For POST (create): email/password required
user_input = users_ns.model(
    "UserInput",
    {
        "email": fields.String(required=True, description="User email"),
        "password": fields.String(required=True, description="User password"),
        "first_name": fields.String(required=False, description="First name"),
        "last_name": fields.String(required=False, description="Last name"),
    },
)

# For PUT (update): all optional (partial update)
user_update = users_ns.model(
    "UserUpdate",
    {
        "email": fields.String(required=False, description="User email"),
        "password": fields.String(required=False, description="User password"),
        "first_name": fields.String(required=False, description="First name"),
        "last_name": fields.String(required=False, description="Last name"),
    },
)

# Output model (NO password)
user_output = users_ns.model(
    "UserOutput",
    {
        "id": fields.String(description="User id"),
        "email": fields.String(description="User email"),
        "first_name": fields.String(description="First name"),
        "last_name": fields.String(description="Last name"),
        "created_at": fields.String(description="Created at"),
        "updated_at": fields.String(description="Updated at"),
    },
)

# ---------- Routes ----------


@users_ns.route("/ping")
class UsersPing(Resource):
    def get(self):
        return {"message": "users namespace works"}, 200


@users_ns.route("/")
class UsersCollection(Resource):
    @users_ns.expect(user_input)
    @users_ns.marshal_with(user_output, code=201)
    def post(self):
        payload = request.get_json() or {}

        try:
            user = User(
                email=payload.get("email"),
                password=payload.get("password"),
                first_name=payload.get("first_name"),
                last_name=payload.get("last_name"),
            )
            facade.repo.add(user)
            return user.to_dict(), 201
        except ValueError as e:
            return {"error": str(e)}, 400

    @users_ns.marshal_list_with(user_output, code=200)
    def get(self):
        users = facade.repo.list(User)
        return [u.to_dict() for u in users], 200


@users_ns.route("/<string:user_id>")
class UserItem(Resource):
    @users_ns.marshal_with(user_output, code=200)
    def get(self, user_id):
        user = facade.repo.get(User, user_id)
        if not user:
            return {"error": "User not found"}, 404
        return user.to_dict(), 200

    @users_ns.expect(user_update)
    @users_ns.marshal_with(user_output, code=200)
    def put(self, user_id):
        user = facade.repo.get(User, user_id)
        if not user:
            return {"error": "User not found"}, 404

        payload = request.get_json() or {}

        try:
            user.update(payload)      # validates email/password if provided
            facade.repo.add(user)     # re-save
            return user.to_dict(), 200
        except ValueError as e:
            return {"error": str(e)}, 400
