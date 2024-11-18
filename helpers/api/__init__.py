from flask_restful import Api

from resources.IndexResource import IndexResource

api = Api()

# Index
api.add_resource(IndexResource, '/')