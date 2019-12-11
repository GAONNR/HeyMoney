import re
import slack
import database

from subprocess import run, PIPE
from datetime import datetime
from logzero import logger
from config import TOKEN
from database import (User, Transaction, DeadTransaction)

SESSION = database.db_connect('heymoney.db')


def update_user_info(web_client):
    users = web_client.users_list()['members']

    session = SESSION()

    for user in users:
        db_user = session.query(User).filter_by(uid=user['id']).first()
        if db_user is None:
            new_user = User(uid=user['id'],
                            name=user['profile']['display_name'],
                            profile_photo=user['profile']['image_192'])
            session.add(new_user)
        else:
            db_user.name = user['profile']['display_name']
            db_user.profile_photo = user['profile']['image_192']
        session.commit()


def add_new_transaction(c_uid, d_uid, name, price, ts):
    session = SESSION()

    creditor = session.query(User).filter_by(uid=c_uid).first()
    debtor = session.query(User).filter_by(uid=d_uid).first()

    new_transaction = Transaction(name=name,
                                  creditor_id=c_uid,
                                  debtor_id=d_uid,
                                  price=price,
                                  timestamp=ts)
    session.add(new_transaction)

    creditor.credit = creditor.credit + price
    debtor.debt = debtor.debt + price

    session.commit()


def kill_transaction(c_uid, d_uid, price):
    session = SESSION()

    creditor = session.query(User).filter_by(uid=c_uid).first()
    debtor = session.query(User).filter_by(uid=d_uid).first()

    transactions = session.query(Transaction) \
        .filter_by(creditor_id=c_uid, debtor_id=d_uid) \
        .order_by(Transaction.timestamp)

    dead_transactions = list()
    remainings = price
    for transaction in transactions:
        if remainings < transaction.price:
            transaction.price = transaction.price - remainings
            remainings = 0
            break
        remainings -= transaction.price
        dead_transactions.append(transaction)

    for t in dead_transactions:
        dead_transaction = DeadTransaction(name=t.name,
                                           creditor_id=t.creditor_id,
                                           debtor_id=t.debtor_id,
                                           price=t.price,
                                           timestamp=t.timestamp)
        session.delete(t)
        session.add(dead_transaction)

    if remainings > 0:
        add_new_transaction(
            d_uid, c_uid, '[AUTO]Remainings', remainings,
            datetime.now().timestamp())

    creditor.credit = creditor.credit - price + remainings
    debtor.debt = debtor.debt - price + remainings

    # TODO: it is too hard to control the remainings
    # because of the race condition.... Should we remove?

    logger.debug('Remainings Occurred')
    logger.debug('Creditor\'s Debt: %d', creditor.debt)
    logger.debug('Debtor\'s Credit: %d', debtor.credit)
    logger.debug('Remainings: %d', remainings)

    creditor.debt = creditor.debt + remainings
    debtor.credit = debtor.credit + remainings

    session.commit()


def tokenize_text(text):
    return re.sub(r'\s+', ' ',
                  re.sub(r'[,|.|@|<|>|!|?|-|+|\"|\']', '', text)).strip().split(' ')


def queryfy_tokens(tokens):
    return '[%s]' % ', '.join(tokens)


def extractor(out):
    res = re.sub(r'\s+', '', out).strip().split(',')
    if res[0] == 'false.':
        return None
    else:
        return {x.split('=')[0]: x.split('=')[1] for x in res}


def test_new_transaction(tokens):
    p = run(['swipl', 'parse_new_trans.pl'], stdout=PIPE,
            input='s(User, Price, What, %s, []).\n\n' % queryfy_tokens(tokens),
            encoding='ascii')
    return extractor(p.stdout)


def test_kill_transaction(tokens):
    p = run(['swipl', 'parse_kill_trans.pl'], stdout=PIPE,
            input='s(User, Price, %s, []).\n\n' % queryfy_tokens(tokens),
            encoding='ascii')
    return extractor(p.stdout)


@slack.RTMClient.run_on(event='message')
def msg_handler(**payload):
    data = payload['data']
    web_client = payload['web_client']

    if not 'user' in data:
        return

    logger.debug('[CHAT] %s in %s: %s', data['user'],
                 data['channel'], data.get('text'))

    if data.get('text').strip() == '!update':
        logger.info('Updating User Info')
        update_user_info(web_client)
        logger.info('Done')
        web_client.chat_postMessage(channel=data['channel'],
                                    text='Hi <@%s>, I just have updated the user list!' % data['user'])

    if data.get('text').strip() == '!test_add_transaction':
        logger.info('Processing Test Scenario: add_transaction')
        add_new_transaction('U6HB7CTRT', 'U6MLYFJG3',
                            'dinner', 10000, int(float(data['ts'])))
        web_client.chat_postMessage(channel=data['channel'],
                                    text='http://lab.g40n.xyz:12345/api/transaction?creditor=U6HB7CTRT')

    if data.get('text').strip() == '!test_kill_transaction':
        logger.info('Processing Test Scenario: kill_transaction')
        kill_transaction('U6HB7CTRT', 'U6MLYFJG3', 3000)
        web_client.chat_postMessage(channel=data['channel'],
                                    text='http://lab.g40n.xyz:12345/api/transaction?creditor=U6HB7CTRT')

    tokenized_text = tokenize_text(data.get('text').lower())
    logger.debug(tokenized_text)

    parsed_new_trans = test_new_transaction(tokenized_text)
    if parsed_new_trans:
        add_new_transaction(data['user'], parsed_new_trans['User'].upper(),
                            parsed_new_trans['What'], int(parsed_new_trans['Price']), int(float(data['ts'])))
        web_client.chat_postMessage(channel=data['channel'],
                                    text='http://lab.g40n.xyz:8080/user-profile/%s' % data['user'])

    parsed_kill_trans = test_kill_transaction(tokenized_text)
    if parsed_kill_trans:
        kill_transaction(parsed_kill_trans['User'].upper(), data['user'],
                         int(parsed_kill_trans['Price']))
        web_client.chat_postMessage(channel=data['channel'],
                                    text='http://lab.g40n.xyz:8080/user-profile/%s' % data['user'])


def __main():
    rtm_client = slack.RTMClient(token=TOKEN)
    logger.info('Starting Slack RTM Client')
    rtm_client.start()


if __name__ == '__main__':
    __main()
