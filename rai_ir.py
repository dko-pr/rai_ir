from flask import Flask
from flask_restful import Api
import rai_ir_resource

app = Flask(__name__)
api = Api(app)
api.add_resource(rai_ir_resource.Tracking, "/rai.ir", "/rai.ir/", "/rai.ir/<int:carNumber>")
if __name__ == '__main__':
    app.run(host= '10.10.200.24', debug=True, port="21523")
