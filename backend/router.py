import database

from flask_restful import (Resource, reqparse)
from database import (User, Transaction, DeadTransaction)

SESSION = database.db_connect('heymoney.db')


class Status(Resource):
    def get(self):
        return {'status': True}


class GetUser(Resource):
    def get(self):
        try:
            req_parser = reqparse.RequestParser()
            req_parser.add_argument('uid', type=str)
            req_args = req_parser.parse_args()

            uid = req_args['uid']

            session = SESSION()

            if uid is None:
                all_users = session.query(User).all()
                return [user.as_dict() for user in all_users]
            else:
                user = session.query(User).filter_by(uid=uid).first()
                return user.as_dict()
        except Exception as e:
            return {'error': str(e)}


class GetTransaction(Resource):
    def get(self):
        try:
            req_parser = reqparse.RequestParser()
            req_parser.add_argument('tid', type=str)
            req_parser.add_argument('debtor', type=str)
            req_parser.add_argument('creditor', type=str)
            req_args = req_parser.parse_args()

            tid = req_args['tid']
            debtor = req_args['debtor']
            creditor = req_args['creditor']

            session = SESSION()

            if tid:
                trade = session.query(Transaction).filter_by(tid=tid).first()
                return trade.as_dict()
            elif debtor:
                trades = session.query(Transaction).filter_by(debtor_id=debtor)
                return [trade.as_dict() for trade in trades]
            elif creditor:
                trades = session.query(Transaction).filter_by(
                    creditor_id=creditor)
                return [trade.as_dict() for trade in trades]
            else:
                all_trades = session.query(Transaction).all()
                return [trade.as_dict() for trade in all_trades]
        except Exception as e:
            return {'error': str(e)}


class GetDeadTransaction(Resource):
    def get(self):
        try:
            req_parser = reqparse.RequestParser()
            req_parser.add_argument('tid', type=str)
            req_parser.add_argument('debtor', type=str)
            req_parser.add_argument('creditor', type=str)
            req_args = req_parser.parse_args()

            tid = req_args['tid']
            debtor = req_args['debtor']
            creditor = req_args['creditor']

            session = SESSION()

            if tid:
                trade = session.query(
                    DeadTransaction).filter_by(tid=tid).first()
                return trade.as_dict()
            elif debtor:
                trades = session.query(
                    DeadTransaction).filter_by(debtor_id=debtor)
                return [trade.as_dict() for trade in trades]
            elif creditor:
                trades = session.query(DeadTransaction).filter_by(
                    creditor_id=creditor)
                return [trade.as_dict() for trade in trades]
            else:
                all_trades = session.query(DeadTransaction).all()
                return [trade.as_dict() for trade in all_trades]
        except Exception as e:
            return {'error': str(e)}


class GetStats(Resource):
    NotImplemented
