# Set the base image to vivek77/jenkinsbot
FROM vivek77/jenkinsbot

# File Author / Maintainer
MAINTAINER Vivek/Denny

# Update the repository sources list
RUN apt-get -yqq update

WORKDIR /root/bot

COPY python_mysql.py slack_cmd_process.py slack_message.py slackbot.py start_app.py /root/bot/

COPY init.sql /docker-entrypoint-initdb.d/

RUN chmod 775 /docker-entrypoint-initdb.d/init.sql && chmod -R 775 /root

RUN rm -rf /var/lib/apt/lists/* && \
rm -rf /var/cache/apk/*

ENV SLACK_BOT_TOKEN="BOT_TOKEN" CHATBOT_NAME="BOT_NAME" \
APPROVER_SLACK_NAME="APPROVER_SLACK_ID" JENKINS_URL="JENKINS_URL" \
JENKINS_USER="JENKINS_USER_NAME" JENKINS_PASS="JENKINS_USER_PASS"
