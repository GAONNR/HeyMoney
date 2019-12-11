# TODO: https://blog.wky.kr/16
import slack
import database

from logzero import logger
from config import TOKEN
from database import (User, Transaction, DeadTransaction)

session = database.db_connect('heymoney.db')


def update_user_info(web_client):
    users = web_client.users_list()['members']
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


def add_new_transaction():
    NotImplemented


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


def __main():
    rtm_client = slack.RTMClient(token=TOKEN)
    logger.info('Starting Slack RTM Client')
    rtm_client.start()


if __name__ == '__main__':
    __main()
