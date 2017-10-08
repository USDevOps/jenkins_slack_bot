# Set the base image to vivek77/jenkinsbot
FROM vivek77/jenkinsbot

# File Author / Maintainer
MAINTAINER Vivek/Denny

# Update the repository sources list
RUN apt-get update

WORKDIR /root/bot

RUN wget -Nq https://raw.githubusercontent.com/USDevOps/jenkins_slack_bot/master/python_mysql.py && \
 wget -Nq https://raw.githubusercontent.com/USDevOps/jenkins_slack_bot/master/slack_cmd_process.py && \
 wget -Nq https://raw.githubusercontent.com/USDevOps/jenkins_slack_bot/master/slack_message.py && \
 wget -Nq https://raw.githubusercontent.com/USDevOps/jenkins_slack_bot/master/slackbot.py && \
 wget -Nq https://raw.githubusercontent.com/USDevOps/jenkins_slack_bot/master/start_app.py && \
 wget -Nq https://raw.githubusercontent.com/USDevOps/jenkins_slack_bot/master/start_bot.sh


ENV SLACK_BOT_TOKEN="BOT_TOKEN" CHATBOT_NAME="BOT_NAME" \
APPROVER_SLACK_NAME="APPROVER_SLACK_ID"

ENTRYPOINT /root/bot/start_bot.sh
