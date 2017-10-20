create database jenkinsbotdb;
create user 'jenkinsbot'@'localhost' identified by 'jenkinsbot';
grant all on jenkinsbotdb.* to 'jenkinsbot' identified by 'jenkinsbot';
use jenkinsbotdb;
create table jenkinsbot_job_status ( username varchar(30), approval_status varchar(20),PRIMARY KEY(username));
