from flask_restful import Resource


class IndexResource(Resource):
    def get(self):
        return {'versao': '0.1'}