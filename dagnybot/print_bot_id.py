import os
from slackclient import SlackClient


BOT_NAME = 'dagny'

slack_client = SlackClient('xoxp-276076583748-276906476150-275523992465-8b479a68064fea8841ff60d64df755bb')


if __name__ == "__main__":
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
    else:
        print("could not find bot user with the name " + BOT_NAME)