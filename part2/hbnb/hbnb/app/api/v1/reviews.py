# app/api/v1/reviews.py
from flask import request
from flask_restx import Namespace, Resource, fields

from app.facade.hbnb_facade import HBnBFacade

facade = HBnBFacade()

api = Namespace("api/v1", description="HBnB API v1 - Reviews")

# نموذج (Schema) للـ Review في RESTx (للتوثيق)
review_model = api.model("Review", {
    "id": fields.String(readOnly=True),
    "text": fields.String(required=True),
    "user_id": fields.String(required=True),
    "place_id": fields.String(required=True),
    "created_at": fields.String(readOnly=True),
    "updated_at": fields.String(readOnly=True),
})

review_create_model = api.model("ReviewCreate", {
    "text": fields.String(required=True),
    "user_id": fields.String(required=True),
})


def _not_json():
    api.abort(400, "Not a JSON")


def _missing(field):
    api.abort(400, f"Missing {field}")


@api.route("/places/<string:place_id>/reviews")
class PlaceReviews(Resource):
    def get(self, place_id):
        # تحقق أن المكان موجود
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")

        reviews = facade.get_reviews_by_place(place_id)
        return [r.to_dict() for r in reviews], 200

    @api.expect(review_create_model, validate=False)
    def post(self, place_id):
        # تحقق أن المكان موجود
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, "Place not found")

        data = request.get_json(silent=True)
        if data is None:
            _not_json()

        # تحقق من user_id و text
        user_id = data.get("user_id")
        text = data.get("text")

        if not user_id:
            _missing("user_id")
        if text is None or (isinstance(text, str) and text.strip() == ""):
            _missing("text")

        # تحقق أن المستخدم موجود
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")

        # أنشئ review واربطه بالمكان
        created = facade.create_review({
            "user_id": user_id,
            "place_id": place_id,
            "text": text,
        })
        return created.to_dict(), 201


@api.route("/reviews/<string:review_id>")
class ReviewById(Resource):
    def get(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")
        return review.to_dict(), 200

    def delete(self, review_id):
        ok = facade.delete_review(review_id)
        if not ok:
            api.abort(404, "Review not found")
        return {}, 200

    def put(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")

        data = request.get_json(silent=True)
        if data is None:
            _not_json()

        # ممنوع تعديل هذه
        forbidden = {"id", "user_id", "place_id", "created_at", "updated_at"}
        clean = {k: v for k, v in data.items() if k not in forbidden}

        # لو حاول يفرغ text
        if "text" in clean and (clean["text"] is None or str(clean["text"]).strip() == ""):
            _missing("text")

        updated = facade.update_review(review_id, clean)
        return updated.to_dict(), 200
