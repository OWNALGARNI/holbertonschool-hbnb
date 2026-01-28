from app.api.v1.users import users_ns

namespaces = [users_ns]

from .amenities import api as amenities_ns
from .places import api as places_ns
from .reviews import api as reviews_ns 

api.add_namespace(amenities_ns, path='/api/v1/amenities')
api.add_namespace(places_ns, path='/api/v1/places')


api.add_namespace(reviews_ns, path='/api/v1')
