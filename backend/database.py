import argparse
import sqlalchemy as db

from logzero import logger
from sqlalchemy import (Column, Integer, String, ForeignKey)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

parser = argparse.ArgumentParser()
parser.add_argument('db_path', default='heymoney.db')
parser.add_argument('--init_db', action='store_true')

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    uid = Column(String, primary_key=True)
    name = Column(String)
    profile_photo = Column(String)
    debt = Column(Integer, default=0)
    credit = Column(Integer, default=0)

    def __repr__(self):
        return '<User %s(%s), debt=%s, credit=%s, profile_photo=%s>' % (
            self.name, self.uid, self.debt, self.credit, self.profile_photo)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Transaction(Base):
    __tablename__ = 'transactions'

    tid = Column(Integer, primary_key=True)
    name = Column(String)
    creditor_id = Column(String, ForeignKey('users.uid'))
    debtor_id = Column(String, ForeignKey('users.uid'))
    price = Column(Integer)
    timestamp = Column(Integer)

    def __repr__(self):
        return '<Transaction %s: %s must give %s %s for %s at %s>' % (
            self.tid, self.debtor_id, self.creditor_id,
            self.price, self.name, self.time)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class DeadTransaction(Base):
    __tablename__ = 'dead_transactions'

    tid = Column(Integer, primary_key=True)
    name = Column(String)
    creditor_id = Column(String, ForeignKey('users.uid'))
    debtor_id = Column(String, ForeignKey('users.uid'))
    price = Column(Integer)
    timestamp = Column(Integer)

    def __repr__(self):
        return '<DeadTransaction %s: %s must give %s %s for %s at %s>' % (
            self.tid, self.debtor_id, self.creditor_id,
            self.price, self.name, self.time)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def get_engine(db_path):
    return db.create_engine('sqlite:///%s' % db_path)


def db_connect(db_path):
    Session = sessionmaker(bind=get_engine(db_path))
    logger.info('Connected to database')
    return Session


def __main():
    args = parser.parse_args()
    if args.init_db:
        engine = get_engine(args.db_path)
        Base.metadata.create_all(engine)
        logger.info('Created New Database and Tables')


if __name__ == '__main__':
    __main()
