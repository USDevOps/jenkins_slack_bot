# jenkins_slack_bot
Invoke Jenkins jobs from slack

[![Build Status](https://travis-ci.org/DennyZhang/jenkins_slack_bot.svg?branch=master)](https://travis-ci.org/DennyZhang/jenkins_slack_bot) [![Docker](https://www.dennyzhang.com/wp-content/uploads/sns/docker.png)](https://hub.docker.com/r/denny/jenkins_slack_bot/) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

## Deploying a JenkinsSlack bot using [Docker Container](https://github.com/USDevOps/jenkins_slack_bot/blob/master/docker-compose.yml) 
This bot is an implementation of CI/CD Process Integration with ChatOps and building a Slack App with Slack's Python SDK, [python-slackclient](http://python-slackclient.readthedocs.io/en/latest/).

We'll cover all the steps you'll need to configure and deploy JenkinsSlack Bot to your Slack Workspace.

JenkinsSlack Bot is designed to help DevOps engineers to execute the CI/CD Process from the chatroom. Additionally, In order to have control over unauthorized deployment of code to different application environment, there is authorization mechanism so that only approved commands can trigger the deployment. 

>![JenkinsSlackbot](https://s3.ap-south-1.amazonaws.com/jenkinsbot/ezgif.com-optimize.gif)

Let's start with the jenkinsSlack bot :sparkles:

## Section 1: Create a Slack App and Bot User

### Creating a new Slack App on [api.slack.com](https://api.slack.com/apps)

In your browser, on [api.slack.com/apps](https://api.slack.com/apps) you'll find a green button labeled [Create New App](https://api.slack.com/apps/new) on the top right of the page.

![create_new_slack_app](https://s3.ap-south-1.amazonaws.com/jenkinsbot/createapp0.PNG)

:point_right: :white_check_mark:

![create_slack_app_detail](https://s3.ap-south-1.amazonaws.com/jenkinsbot/newapp.PNG)


### Adding A Bot User

Let's create new **Bot User** so our app can communicate on Slack. On the left side navigation of your app's settings page you'll find the **Bot Users** tab where you can create a new bot user for your app.

![add_bot_user](https://s3.ap-south-1.amazonaws.com/jenkinsbot/createapp3.PNG)

## Section 2: Subscribe to Events and Enable Interactive Components

Once you have created the Slack App and Bot User, let's have it subscribe to some events in Slack!

On your app's settings page you'll find **Event Subscriptions** on the left navigation bar and turn on the Enable Events.

Near the bottom of the page under the **WorkSpace Events** section you'll be able to subscribe your bot to the events.

![add_WorkSpace_events](https://s3.ap-south-1.amazonaws.com/jenkinsbot/events_new.PNG)

This project uses the following events:

- [message.channels](https://api.slack.com/events/message.channels)
- [message.im](https://api.slack.com/events/message.im)

After you've subscribed to all the events your app will need, you need to enable the interactive components. Before Proceeding, make sure to save the changes.

On your app's settings page you'll find **Interactive Components** on the left navigation bar.

Click on button Enable Inteactive Components and Add the URL like below:

http://HOST:PORT_NO/slack/message_actions (Select the port of your machine which you want to expose)

![Enable Inteactive Components](https://s3.ap-south-1.amazonaws.com/jenkinsbot/events2.PNG)

When you are done, make sure to **Save Changes** and copy the URL you will need to have it while building the bot.

## Section 3: SLACK BOT Token and Install App

Once you have subscribed the bot events and interactive components, let's install the App to the Slack Workspace

On your app's settings page you'll find **OAuth & Permissions** on the left navigation bar and click on **Install App to Workspace** button.

After clicking on button, you will need to authorize the bot on next page.

![Install App](https://s3.ap-south-1.amazonaws.com/jenkinsbot/install2.PNG)

Now under the **Bot User OAuth Access Token** section you'll be able to find the Bot Token.

Please copy the bot token from the page and save it you will need to use it while building the bot.

![Bot User Access token](https://s3.ap-south-1.amazonaws.com/jenkinsbot/token.PNG

## How To Use

### Specify the Environment Variable  and Host Port no in docker compose file.

```
environment:
       MYSQL_ROOT_PASSWORD : "MYSQL_PASS"
       SLACK_BOT_TOKEN : "BOT_TOKEN"
       CHATBOT_NAME : "BOT_NAME"
       APPROVER_SLACK_NAME : "APPROVER_SLACK_ID"

 ports:
      - "HOST_PORT"

```
### Building the bot from docker compose file.

```
docker-compose.yml up 

```

# System Design
### High Level Design Diagram of Jenkins_Slack_Bot.

![High Level Design Diagram](https://s3.ap-south-1.amazonaws.com/jenkinsbot/HLD_jenkinsslackbot.jpg)

# Demo & Screenshot
![Jenkins Slackbot demo GIF](https://s3.ap-south-1.amazonaws.com/jenkinsbot/ezgif.com-optimize.gif)

# Maintainers
- Vivek Grover:[![LinkedIn](https://www.dennyzhang.com/wp-content/uploads/sns/linkedin.png)](https://www.linkedin.com/in/vivek-grover-69420743/) [![Github](https://www.dennyzhang.com/wp-content/uploads/sns/github.png)](https://github.com/vivekgrover1/)
- [Denny Zhang](https://www.dennyzhang.com): [![LinkedIn](https://www.dennyzhang.com/wp-content/uploads/sns/linkedin.png)](https://www.linkedin.com/in/dennyzhang001) [![Github](https://www.dennyzhang.com/wp-content/uploads/sns/github.png)](https://github.com/DennyZhang) [![Twitter](https://www.dennyzhang.com/wp-content/uploads/sns/twitter.png)](https://twitter.com/dennyzhang001) [![Slack](https://www.dennyzhang.com/wp-content/uploads/sns/slack.png)](https://goo.gl/ozDDyL)
