import argparse
import database

from logzero import logger
from flask import (Flask, render_template)
from flask_restful import Api

from router import (Status,
                    GetUser,
                    GetTransaction,
                    GetStats)

parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int, default=12345)
parser.add_argument('--debug', action='store_true')
args = parser.parse_args()

app = Flask(__name__, template_folder='./', static_folder='dist/static')
api = Api(app)

api.add_resource(Status, '/api')
api.add_resource(GetUser, '/api/user')
api.add_resource(GetTransaction, '/api/transaction')
api.add_resource(GetStats, '/api/stats')


def __main():
    app.run('0.0.0.0', debug=args.debug, port=args.port, threaded=True)


if __name__ == '__main__':
    __main()
