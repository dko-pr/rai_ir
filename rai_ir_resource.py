from flask_restful import Resource, reqparse
import rai_ir_request
class Tracking(Resource):
    def get(self, carNumber):
        if (carNumber == 0):
            return "Please input car number.", 404
        else:
            return rai_ir_request.getTrackingDetails(carNumber), 200
    def post(self):
        return "Not supported. Use GET method.", 404
    def put(self):
        return "Not supported. Use GET method.", 404
    def delete(self):
        return "Not supported. Use GET method.", 404
