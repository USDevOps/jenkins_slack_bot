#!/usr/bin/python
##-------------------------------------------------------------------
## @copyright 2017 DennyZhang.com
## Licensed under MIT
##   https://www.dennyzhang.com/wp-content/mit_license.txt
##
## File : start_app.py
## Author : Vivek Grover <vivek271091@gmail.com>, Denny Zhang <contact@dennyzhang.com>
## Description :
## --
## Created : <2017-08-27>
## Updated: Time-stamp: <2017-09-25 17:14:31>
##-------------------------------------------------------------------
from flask import Flask, request, make_response, Response
from slackclient import SlackClient
import json
import os
import slackbot
import python_mysql
import slack_message

# Flask webserver for incoming traffic from Slack
app = Flask(__name__)


@app.route('/')
def index():
    print('hi budy')
    return 'This is the homepage'


@app.route("/slack/message_actions", methods=["POST"])
def message_actions():
    # slack_event = json.loads(request.data)
    # return slack_event.get('challenge')
    # Parse the request payload
    form_json = json.loads(request.form["payload"])

    # Check to see what the user's selection was and update the message
    selection = form_json["actions"][0]["value"]
    chan_id = form_json["channel"]["id"]
    msg_ts = form_json["message_ts"]
    callback = form_json["callback_id"]
    username = form_json["user"]["name"]
    user_id = callback.split('_')[0]
    job_id = callback.split('_')[1]
    user_chan_id = callback.split('_')[2]

    if selection == "Yes":
        mesg = "Your request has been sent to the Admin for the Approval of job_id_{0}.".format(job_id)
        if user_id == username:
            slack_message.update_message(chan_id, msg_ts, mesg)
            slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
            SLACK_NAME = os.environ.get('APPROVER_SLACK_NAME')
            userid = slackbot.get_bot_id(SLACK_NAME, slack_client)
            im_id = slackbot.get_im_id(userid, slack_client)
            slack_message.send_interactive_message(username, job_id, im_id, user_chan_id)

    elif selection == "bad":
        mesg = "You choose not to send your request to Admin for Approval."
        if user_id == username:
            slack_message.update_message(chan_id, msg_ts, mesg)



    elif selection == "Not Approved":
        mesg = "Thanks, I will inform the user!"
        slack_message.update_message(chan_id, msg_ts, mesg)

        mesg2 = "Sorry! Your Request has been rejected by Admin."
        slack_message.send_message_without_button(user_id, mesg2, user_chan_id)

    elif selection == "Approve":
        mesg = "Thanks, I will inform the user!"
        slack_message.update_message(chan_id, msg_ts, mesg)
        job = "job_id_" + job_id
        python_mysql.update_status(job, user_id)
        mesg2 = "Your Request has been approved for {0} now you can execute the command".format(job)
        slack_message.send_message_without_button(user_id, mesg2, user_chan_id)

    return make_response("", 200)


if __name__ == "__main__":
    slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
    app.run(host='0.0.0.0', port='80')

## File : start_app.py ends
