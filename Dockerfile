# Set the base image to vivek77/jenkinsbot
FROM vivek77/jenkinsbot

# File Author / Maintainer
MAINTAINER Vivek/Denny

# Update the repository sources list
RUN apt-get -yqq update

WORKDIR /root/bot

RUN wget -Nq https://raw.githubusercontent.com/USDevOps/jenkins_slack_bot/tag_v1/python_mysql.py && \
 wget -Nq https://raw.githubusercontent.com/USDevOps/jenkins_slack_bot/tag_v1/slack_cmd_process.py && \
 wget -Nq https://raw.githubusercontent.com/USDevOps/jenkins_slack_bot/tag_v1/slack_message.py && \
 wget -Nq https://raw.githubusercontent.com/USDevOps/jenkins_slack_bot/tag_v1/slackbot.py && \
 wget -Nq https://raw.githubusercontent.com/USDevOps/jenkins_slack_bot/tag_v1/start_app.py


RUN cd /docker-entrypoint-initdb.d;wget -Nq https://raw.githubusercontent.com/USDevOps/jenkins_slack_bot/tag_v1/init.sql

RUN rm -rf /var/lib/apt/lists/* && \
rm -rf /var/cache/apk/*

ENV SLACK_BOT_TOKEN="BOT_TOKEN" CHATBOT_NAME="BOT_NAME" \
APPROVER_SLACK_NAME="APPROVER_SLACK_ID"
