# Set the base image to vivek77/jenkinsbot
FROM vivek77/jenkinsbot

# File Author / Maintainer
MAINTAINER Vivek/Denny

# Update the repository sources list
RUN apt-get -yqq update

WORKDIR /root/bot

ADD https://raw.githubusercontent.com/vivekgrover1/jenkinsbot/master/python_mysql.py \
 https://raw.githubusercontent.com/USDevOps/jenkins_slack_bot/tag_v1/slack_cmd_process.py  \
 https://raw.githubusercontent.com/USDevOps/jenkins_slack_bot/tag_v1/slack_message.py  \
 https://raw.githubusercontent.com/USDevOps/jenkins_slack_bot/tag_v1/slackbot.py  \
 https://raw.githubusercontent.com/USDevOps/jenkins_slack_bot/tag_v1/start_app.py /root/bot/

ADD https://raw.githubusercontent.com/vivekgrover1/jenkinsbot/master/init.sql /docker-entrypoint-initdb.d/

RUN chmod 775 /docker-entrypoint-initdb.d/init.sql && chmod -R 775 /root

RUN rm -rf /var/lib/apt/lists/* && \
rm -rf /var/cache/apk/*

ENV SLACK_BOT_TOKEN="BOT_TOKEN" CHATBOT_NAME="BOT_NAME" \
APPROVER_SLACK_NAME="APPROVER_SLACK_ID"
