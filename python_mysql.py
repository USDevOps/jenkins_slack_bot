#!/usr/bin/python
##-------------------------------------------------------------------
## @copyright 2017 DennyZhang.com
## Licensed under MIT
##   https://www.dennyzhang.com/wp-content/mit_license.txt
##
## File : python_mysql.py
## Author : Vivek Grover <vivek271091@gmail.com>, Denny Zhang <contact@dennyzhang.com>
## Description :
## --
## Created : <2017-08-27>
## Updated: Time-stamp: <2017-09-25 17:14:35>
##-------------------------------------------------------------------

import pymysql

def get_status(job_id,user):
  # Open database connection
  db = pymysql.connect("localhost","testuser","password","testdb" )
  # prepare a cursor object using cursor() method
  cursor = db.cursor()
  # Prepare SQL query to INSERT a record into the database.
  sql = "select {0} from access_command where username='{1}'".format(job_id,user)
  try:
    # Execute the SQL command
    cursor.execute(sql)
    # Fetch all the rows in a list of lists.
    results = cursor.fetchall()
    #return results
    for row in results:
      return(row[0])
  except:
    return "Error: unable to fetch data"

  # disconnect from server
  db.close()

def update_status(job_id,user):
  db = pymysql.connect("localhost","testuser","password","testdb" )
  cursor = db.cursor()
  sql = "update access_command set {0}='Approved' where username='{1}'".format(job_id,user)
  try:
    cursor.execute(sql)
    db.commit()
  except:
    db.rollback()

    db.close()

def add_user(user):
   db = pymysql.connect("localhost","testuser","password","testdb" )
   cursor = db.cursor()
   sql = "insert into access_command values ('%s','Not Approved','Not Approved','Not Approved')" %user
   try:
     cursor.execute(sql)
     db.commit()
   except:
     db.rollback()
   db.close()
## File : python_mysql.py ends
