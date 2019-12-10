# TODO: https://blog.wky.kr/16
import slack

from config import TOKEN


@slack.RTMClient.run_on(event='message')
def msg_handler(**payload):
    data = payload['data']
    web_client = payload['web_client']

    if 'Hello' in data.get('text', []):
        channel_id = data['channel']
        thread_ts = data['ts']

        user = data['user']
        web_client.chat_postMessage(channel=channel_id,
                                    text=f'Hi <@{user}>!', thread_ts=thread_ts)


def __main():
    rtm_client = slack.RTMClient(token=TOKEN)
    rtm_client.start()


if __name__ == '__main__':
    __main()
