#!/usr/bin/python
##-------------------------------------------------------------------
## @copyright 2017 DennyZhang.com
## Licensed under MIT
##   https://www.dennyzhang.com/wp-content/mit_license.txt
##
## File : slack_cmd_process.py
## Author : Vivek Grover <vivek271091@gmail.com>, Denny Zhang <contact@dennyzhang.com>
## Description :
## --
## Created : <2017-08-27>
## Updated: Time-stamp: <2017-09-25 17:14:34>
##-------------------------------------------------------------------
import os
import python_mysql
import re
import subprocess
import jenkins
import time
import slackbot
import slack_message

BOT_NAME = os.environ.get('CHATBOT_NAME')

help = """Use below commands to use the bot\n\n@{0} command list jobs\n
@{0} command list running jobs\n
@{0} command describe job <job_name>\n
@{0} command execute job <job name> \n
""".format(BOT_NAME)

list_cmd = """List of the Commands:\n
1) deploy code from abc repository on example1.com server .
2) deploy code from xyz repository on example2.com server .
3) restart service on abc server.
"""


def cmd_process(command, username, chann_id):
    """
      Decide the command which is to be run based on user message directed
      at bot.
    """
    lis = command.split(" ")

    if lis[0].startswith("hi"):
        return "I am doing good, How about you?", "approved", "good"
    if len(lis) == 1 and lis[0] == "help":
        return help, "approved", "good"
    if lis[0] == "command" and len(lis) >= 3:
        if len(lis) == 3 and lis[1] == "list" and lis[2] == "jobs":
            return list_jobs_jenkins(), "approved", "good"
        if len(lis) == 4 and lis[1] == "list" and lis[2] == "running" and lis[3] == "jobs":
            return list_running_jenkins_job(), "approved", "good"
        if len(lis) == 4 and lis[1] == "describe" and lis[2] == "job" and len(lis[3]) > 0:
            output = jenkins_describe(lis[3].strip())
            if output == "Sorry, I can't find the job. Typo maybe?":
                return output, "approved", "danger"
            return output, "approved", "good"
        if len(lis) == 4 and lis[1] == "execute" and lis[2] == "job" and len(lis[3]) > 0:
            response, status, color = cmd_execute(username, lis[3], chann_id)
            return response, status, color

    return "Not sure what you mean, please use help.", "approved", "danger"


def cmd_execute(username, job_name, chann_id):
    value = python_mysql.get_status(username)
    if value != "Approved":
        return ":slightly_frowning_face: You don't have Approval to execute the job.\nWould you like to get the " \
               "approval from Admin to execute this command?", "notapproved", "danger"
    elif value == "Approved":
        output = cmd_exec(username, job_name, chann_id)
        if output == "Sorry, I can't find the job. Typo maybe?":
            return output, "approved", "danger"
        return output, "approved", "good"


def cmd_exec(username, job_name, chann_id):
    """
      execute the jenkins job based on provided job id and return the console output

    """
    try:
        url = get_job_url(job_name)
        if url != "not found":
            slack_message.send_message_without_button(username,
                                                      'Please wait job is being executed, use below url to check the '
                                                      'progress.\n{0}'.format( 
                                                          url), chann_id)
        output = execute_jenkins_job(job_name)
        return output
    except:
        return "Exception"


def execute_jenkins_job(job_name):
    try:
        jenkins_url = os.environ.get('JENKINS_URL')
        user_name = os.environ.get('JENKINS_USER')
        user_pass = os.environ.get('JENKINS_PASS')
        server = jenkins.Jenkins('{0}'.format(jenkins_url), username='{0}'.format(user_name),
                                 password='{0}'.format(user_pass))
        last_build_number = server.get_job_info('{0}'.format(job_name))['lastCompletedBuild']['number']
        new_build_number = server.get_job_info('{0}'.format(job_name))['lastCompletedBuild']['number']
        server.build_job('{0}'.format(job_name))
        while new_build_number == last_build_number:
            time.sleep(2)
            new_build_number = server.get_job_info('{0}'.format(job_name))['lastCompletedBuild']['number']
        return server.get_build_console_output('{0}'.format(job_name), new_build_number)
    except jenkins.NotFoundException:
        return "Sorry, I can't find the job. Typo maybe?"


def list_jobs_jenkins():
    jenkins_url = os.environ.get('JENKINS_URL')
    user_name = os.environ.get('JENKINS_USER')
    user_pass = os.environ.get('JENKINS_PASS')
    server = jenkins.Jenkins('{0}'.format(jenkins_url), username='{0}'.format(user_name),
                             password='{0}'.format(user_pass))
    jobs = server.get_jobs()
    max_length = max([len(job['name']) for job in jobs])
    return ('\n'.join(
        ['{2})  <{1}|{0}> '.format(job['name'].ljust(max_length), job['url'], (counter + 1)) for counter, job in
         enumerate(jobs)]).strip())


def get_job_url(job_name):
    jenkins_url = os.environ.get('JENKINS_URL')
    user_name = os.environ.get('JENKINS_USER')
    user_pass = os.environ.get('JENKINS_PASS')
    server = jenkins.Jenkins('{0}'.format(jenkins_url), username='{0}'.format(user_name),
                             password='{0}'.format(user_pass))
    jobs = server.get_jobs()
    for job in jobs:
        if job['name'] == job_name:
            return (job['url'])
    return "not found"


def list_running_jenkins_job():
    jenkins_url = os.environ.get('JENKINS_URL')
    user_name = os.environ.get('JENKINS_USER')
    user_pass = os.environ.get('JENKINS_PASS')
    server = jenkins.Jenkins('{0}'.format(jenkins_url), username='{0}'.format(user_name),
                             password='{0}'.format(user_pass))
    jobs = [job for job in server.get_jobs() if 'anime' in job['color']]
    jobs_info = [server.get_job_info(job['name']) for job in jobs]
    if not jobs_info:
        return "no jobs found"
    else:
        return '\n\n'.join(
            ['<{1}|{0}>\n{2}'.format(job['name'], job['lastBuild']['url'], job['healthReport'][0]['description']) for
             job in jobs_info]).strip()


def jenkins_describe(job_name):
    """Describe the job specified by jobName."""
    jenkins_url = os.environ.get('JENKINS_URL')
    user_name = os.environ.get('JENKINS_USER')
    user_pass = os.environ.get('JENKINS_PASS')
    server = jenkins.Jenkins('{0}'.format(jenkins_url), username='{0}'.format(user_name),
                             password='{0}'.format(user_pass))

    try:
        job = server.get_job_info(job_name.strip())
    except jenkins.NotFoundException:
        return "Sorry, I can't find the job. Typo maybe?"

    return ''.join([
        'Name: ', job['name'], '\n',
        'URL: ', job['url'], '\n',
        'Description: ', 'None' if job['description'] is None else job['description'], '\n',
        'Next Build Number: ',
        str('None' if job['nextBuildNumber'] is None else job['nextBuildNumber']), '\n',
        'Last Successful Build Number: ',
        str('None' if job['lastBuild'] is None else job['lastBuild']['number']), '\n',
        'Last Successful Build URL: ',
        'None' if job['lastBuild'] is None else job['lastBuild']['url'], '\n'
    ])

## File : slack_cmd_process.py ends
