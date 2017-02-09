# This script reuses and adapts the code from 
# https://github.com/mattmakai/fullstackpython.com/blob/gh-pages/source/content/posts/160604-build-first-slack-bot-python.markdown
# https://github.com/mccreath/isitup-for-slack/blob/master/docs/TUTORIAL.md
# Both repos at the time of writing are covered by the MIT license

import os
import time
from slackclient import SlackClient
import requests
import re

# starterbot's ID as an environment variable

BOT_ID = os.environ.get('BOT_ID')

# constants

AT_BOT = '<@' + BOT_ID + '>'
EXAMPLE_COMMAND = 'ping'

# instantiate Slack & Twilio clients

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


def post_message(msg):
    """
        Wrapper for message posting
    """

    slack_client.api_call('chat.postMessage', channel=channel,
                          text=msg, as_user=True)


def get_status_description(status_code):
    """
        Return textual description of website status
    """

    if status_code == 1:
        status_text = '*up*'
    elif status_code == 2:
        status_text = '*down*'
    elif status_code == 3:
        status_text = '*not valid*'
    else:
        status_text = '*intractable*. Status code ' + str(status_code) \
            + ' is unknown'
    return status_text


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """

    response = 'Not sure what you mean. Use the *' + EXAMPLE_COMMAND \
        + '* domain, delimited by space.'
    if command.startswith(EXAMPLE_COMMAND):

        # This code block is hacked together, no proper error handling -- very fragile

        print "Parsed command is '" + command + "'"

        # Slack converts 'ping ryerson.ca' to 'ping <http://ryerson.ca|ryerson.ca>'
        # Need to extract the domain name resideing between | and >

        domain_names = re.findall(r'\|(.*)\>', command)
        status = ''
        if domain_names:
            domain_name = domain_names[0]  # grab the 1st value
            print 'Domain name is ' + domain_name
            r = requests.get('https://isitup.org/' + domain_name
                             + '.json')
            status = r.json()
            response = 'Web site ' + domain_name + ' is ' \
                + get_status_description(status['status_code'])

            post_message(response)
            post_message('Raw response from isitup.org is')
            post_message(status)
        else:
            post_message("I got the following command '" + command
                         + "' but could not extract the domain name")


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """

    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:

                # return text after the @ mention, whitespace removed

                return (output['text'
                        ].split(AT_BOT)[1].strip().lower(),
                        output['channel'])
    return (None, None)


if __name__ == '__main__':
    READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print 'StarterBot connected and running!'
        while True:
            (command, channel) = \
                parse_slack_output(slack_client.rtm_read())
            if command and channel:
                print 'Cleaned up message: comand = ', command, \
                    'channel = ', channel
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print 'Connection failed. Invalid Slack token or bot ID?'


			