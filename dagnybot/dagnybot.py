import redis
import time
from slackclient import SlackClient


# starterbot's ID as an environment variable
BOT_ID = 'U8416DAUS'

# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

# instantiate Slack & Twilio clients
slack_client = SlackClient('xoxp-276076583748-276906476150-275523992465-8b479a68064fea8841ff60d64df755bb')


def analysis_request(r):
    response = 'Hi! Can I help with some analysis?'

    r.set('status', '1')
    return response


def select_analysis(r):
    response = 'What scan are we analyzing?'

    r.set('status', '2')
    return response


def handle_command(command, channel, r):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    # response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
    #           "* command with numbers, delimited by spaces."
    # if command.startswith(EXAMPLE_COMMAND):
    #   response = "Sure...write some more code then I can do that!"

    status = r.get('status')

    print('status is', status)

    if status is b'0':
        response = analysis_request(r)
    elif status is b'1':
        response = select_analysis(r)
    else:
        response = 'zzzz'

    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=False)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            print(output)
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":

    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    r.set('status', '0')

    READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from firehose

    if slack_client.rtm_connect():
        print("DagnyBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel, r)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")