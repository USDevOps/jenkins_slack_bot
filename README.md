# jenkins_slack_bot
Invoke Jenkins jobs from slack

[![Build Status](https://travis-ci.org/DennyZhang/jenkins_slack_bot.svg?branch=master)](https://travis-ci.org/DennyZhang/jenkins_slack_bot) [![Docker](https://www.dennyzhang.com/wp-content/uploads/sns/docker.png)](https://hub.docker.com/r/denny/jenkins_slack_bot/) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

## Deploying a JenkinsSlack bot using [Docker Container](https://github.com/vivekgrover1/jenkinsbot/blob/master/Dockerfile) 
This bot is an implementation of CI/CD Process Integration with ChatOps and building a Slack App with Slack's Python SDK, [python-slackclient](http://python-slackclient.readthedocs.io/en/latest/).

We'll cover all the steps you'll need to configure and deploy JenkinsSlack Bot to your Slack Workspace.

JenkinsSlack Bot is designed to help DevOps engineers to execute the CI/CD Process from the chatroom. Additionally, In order to have control over unauthorized deployment of code to different application environment, there is authorization mechanism so that only approved commands can trigger the deployment. 

>![JenkinsSlackbot](https://s3.ap-south-1.amazonaws.com/jenkinsbot/ezgif.com-optimize.gif)

Let's start with the jenkinsSlack bot :sparkles:

* [Section 1: Create a Slack App and Bot User](docs/section1.md)  
* [Section 2: Subscribe to Events and Enable Interactive Components](docs/section2.md)  
* [Section 3: Install Slack App](docs/section3.md)

## How To Use

### Specify the Environment Variable in docker file.

```
ENV SLACK_BOT_TOKEN="slack-token" CHATBOT_NAME="your_bot_name" \
APPROVER_SLACK_NAME="SLACK_USER_ID" 

```
### Building the bot from docker file.

```
docker build -t jenkinsbot .

```
### Run the container with --publish option in run command.

```
 docker run -d -p 98:80 -it --name jenkinsbot jenkinsbot
 
 docker exec jenkinsbot sh /root/bot/start_bot.s
```

# System Design
### High Level Design Diagram of Jenkins_Slack_Bot.

![High Level Design Diagram](https://s3.ap-south-1.amazonaws.com/jenkinsbot/HLD_jenkinsslackbot.jpg)

# Demo & Screenshot
![Jenkins Slackbot demo GIF](https://s3.ap-south-1.amazonaws.com/jenkinsbot/ezgif.com-optimize.gif)

# Maintainers
- Vivek Grover:[![LinkedIn](https://www.dennyzhang.com/wp-content/uploads/sns/linkedin.png)](https://www.linkedin.com/in/vivek-grover-69420743/) [![Github](https://raw.githubusercontent.com/USDevOps/mywechat-slack-group/master/images/github.png)](https://github.com/vivekgrover1/)
- [Denny Zhang](https://www.dennyzhang.com): [![LinkedIn](https://www.dennyzhang.com/wp-content/uploads/sns/linkedin.png)](https://www.linkedin.com/in/dennyzhang001) [![Github](https://raw.githubusercontent.com/USDevOps/mywechat-slack-group/master/images/github.png)](https://github.com/DennyZhang) [![Twitter](https://raw.githubusercontent.com/USDevOps/mywechat-slack-group/master/images/twitter.png)](https://twitter.com/dennyzhang001) [![Slack](https://raw.githubusercontent.com/USDevOps/mywechat-slack-group/master/images/slack.png)](https://goo.gl/ozDDyL)
