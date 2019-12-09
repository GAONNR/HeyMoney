# TODO: https://blog.wky.kr/16
import slack

from token import TOKEN


def response(client):
    res = client.chat_postMessage(channel='#money', text='Hello world!')

    assert res["ok"]
    assert res["message"]["text"] == "Hello world!"
    return res


def __main():
    client = slack.WebClient(token=TOKEN)
    response(client)


if __name__ == '__main__':
    __main()
