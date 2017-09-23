import os
import python_mysql
import re
import subprocess
import jenkins
import time
import slackbot
import slack_message

help="""Use below commands to use the bot\n\n@jenkinsbot command list jobs\n
@jenkinsbot command execute job <job id> \n
"""

list_cmd="""List of the Commands:\n
1) deploy code from abc repository on example1.com server .
2) deploy code from xyz repository on example2.com server .
3) restart service on abc server.
"""


def cmd_process(command,username):
    """
      Decide the command which is to be run based on user message directed
      at bot.
    """
    lis=command.split(" ")

    if lis[0].startswith("hi"):
        return "I am doing good, How about you?","approved","good",0
    if len(lis)==1 and lis[0]=="help":
        return help, "approved","good",0
    if lis[0]=="command" and len(lis)>=3:
        if len(lis)==3 and lis[1]=="list" and lis[2]=="jobs" :
           return list_cmd, "approved","good",0
        if len(lis)==4 and lis[1]=="execute" and lis[2]=="job" and (lis[3]=="1" or lis[3]=="2" or lis[3]=="3"):
           response,status,color=cmd_execute(username,lis[3])
           return response,status,color,lis[3]




    return "Not sure what you mean, please use help.","approved","danger",0

def cmd_execute(username,job_no):

    job_id="job_id_" + job_no
    value=python_mysql.get_status(job_id,username)
    if value!="Approved":
       return " :slightly_frowning_face: You don't have Approval to execute the {0}.\nWould you like to get the approval from Admin to execute this command?".format(job_id), "notapproved","danger"
    elif value=="Approved":
       output=cmd_exec(username,job_no)
       return output,"approved","good"


def cmd_exec(username,job_no):
    """
      execute the jenkins job based on provided job id and return the console output
    """
    try:

     if( job_no == "1"):
      slack_message.send_message_without_button(username,'Please wait job is being executed...')
      output=execute_jenkins_job('job_ansible_1')
      return output
     elif( job_no =="2"):
      slack_message.send_message_without_button(username,'Please wait job is being executed...')
      output=execute_jenkins_job('job_ansible_2')
      return output
     elif(job_no == "3"):
      slack_message.send_message_without_button(username,'Please wait job is being executed...')
      output=execute_jenkins_job('job_ansible_3')
      return output
    except:
      return "Exception"


def execute_jenkins_job(job_name):

  ec2_host=os.environ.get('EC2_HOST')
  user_pass=os.environ.get('USER_PASS')
  server = jenkins.Jenkins('http://{0}:8080'.format(ec2_host), username='vivek', password='{0}'.format(user_pass))
  server.build_job('{0}'.format(job_name))
  time.sleep(8)
  last_build_number = server.get_job_info('{0}'.format(job_name))['lastCompletedBuild']['number']
  return server.get_build_console_output('{0}'.format(job_name), last_build_number)
