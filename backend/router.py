import database

from flask_restful import (Resource, reqparse)
from database import (User, Transaction, DeadTransaction)

session = database.db_connect('heymoney.db')


class Stats(Resource):
    def get(self):
        return {'status': True}


class GetUser(Resource):
    def get(self):
        try:
            req_parser = reqparse.RequestParser()
            req_parser.add_argument('uid', type=str)
            req_args = req_parser.parse_args()

            uid = req_args['uid']

            if uid is None:
                all_users = session.query(User).all()
                return [user.as_dict() for user in all_users]
            else:
                user = session.query(User).filter_by(uid=uid).first()
                return user.as_dict()
        except Exception as e:
            return {'error': str(e)}


class GetTransaction(Resource):
    NotImplemented


class GetStats(Resource):
    NotImplemented
