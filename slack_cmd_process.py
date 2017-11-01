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

help = """Use below commands to use the bot.\n\n!list jobs\n
!list running jobs\n
!list failed jobs\n
!describe job <job_name>\n
!execute job <job name> \n
"""


def cmd_process(command, username, chann_id):
    """
      Decide the command which is to be run based on user message directed
      at bot.
    """
    lis = command.split()

    if command.strip() == "None":
        return help, "approved", "good"
    if command.strip().startswith("hi"):
        return "I am doing good, How about you?", "approved", "good"
    if re.search(r'help|--help|-- help|--\s.*help', command):
        return help, "approved", "good"
    if re.search(r'list jobs|jobslist|listjobs|jobs list|list job|job list', command):
        return list_jobs_jenkins(username, chann_id), "approved", "good"
    if re.search(
            r'list running jobs|jobsrunninglist|listrunningjobs|jobs running list|running job|job running list|running',
            command):
        return list_running_jenkins_job(username, chann_id), "approved", "good"
    if re.search(r'list failed jobs|jobsfailedlist|listfailedjobs|jobs failed list|failed job|job failed list|failed',
                 command):
        return list_failed_jenkins_job(username, chann_id), "approved", "good"
    if len(lis) == 3 and lis[0] == "describe" and lis[1] == "job" and len(lis[2]) > 0:
        output = jenkins_describe(lis[2].strip())
        if output == "Sorry, I can't find the job. Typo maybe?":
            return output, "approved", "danger"
        return output, "approved", "good"
    if len(lis) == 3 and lis[0] == "execute" and lis[1] == "job" and len(lis[2]) > 0:
        response, status, color = cmd_execute(username, lis[2], chann_id)
        return response, status, color

    return "Not sure what you mean, please use help.\n\n{0}".format(help), "approved", "danger"


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


def list_jobs_jenkins(username, chann_id):
    jenkins_url = os.environ.get('JENKINS_URL')
    user_name = os.environ.get('JENKINS_USER')
    user_pass = os.environ.get('JENKINS_PASS')
    server = jenkins.Jenkins('{0}'.format(jenkins_url), username='{0}'.format(user_name),
                             password='{0}'.format(user_pass))
    jobs = server.get_jobs()
    slack_message.send_message_without_button(username, "I'm getting the jobs list from Jenkins...", chann_id)
    time.sleep(2)
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
            return job['url']
    return "not found"


def list_running_jenkins_job(username, chann_id):
    jenkins_url = os.environ.get('JENKINS_URL')
    user_name = os.environ.get('JENKINS_USER')
    user_pass = os.environ.get('JENKINS_PASS')
    server = jenkins.Jenkins('{0}'.format(jenkins_url), username='{0}'.format(user_name),
                             password='{0}'.format(user_pass))
    jobs = [job for job in server.get_jobs() if 'anime' in job['color']]
    jobs_info = [server.get_job_info(job['name']) for job in jobs]
    slack_message.send_message_without_button(username, "I will ask for the current running builds list!", chann_id)
    time.sleep(2)
    if not jobs_info:
        return "There is no running jobs!"
    else:
        return '\n\n'.join(
            ['<{1}|{0}>\n{2}'.format(job['name'], job['lastBuild']['url'], job['healthReport'][0]['description']) for
             job in jobs_info]).strip()


def list_failed_jenkins_job(username, chann_id):
    jenkins_url = os.environ.get('JENKINS_URL')
    user_name = os.environ.get('JENKINS_USER')
    user_pass = os.environ.get('JENKINS_PASS')
    server = jenkins.Jenkins('{0}'.format(jenkins_url), username='{0}'.format(user_name),
                             password='{0}'.format(user_pass))
    jobs = [job for job in server.get_jobs() if 'red' in job['color']]
    jobs_info = [server.get_job_info(job['name']) for job in jobs]
    slack_message.send_message_without_button(username, "I will get the failed jenkins job!", chann_id)
    time.sleep(2)
    if not jobs_info:
        return "There is no failed jobs!"
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
