# -*- coding: utf-8 -*-
"""
Email script for pizza lunch and w(h)ine time warnings
Modified by Trevor Dorn-Wallenstein to do birthdays
======================================================

In the same directory as this script, you should create
a `birthdays.txt` file. Each line will have a username+name
of a grad with their next birthday, like so: 

    tzdw Trevor MM DD 2019

Where you're careful to choose the right year because 
otherwise it'll break. At the end of the file, make an
entry like
    rerun Trevor MM DD YYYY
Where MM DD YYYY is the date you want to be reminded
to set up the script next year. This script will set up `at` jobs 
to email the grads on each birthday. The contents of the 
emails should be specified in this script. Note - we're
using HTML encoding to send out those files, so to render 
line breaks, use <br> tags, etc.

To add new assignments, first update the `birthdays.txt` 
file with new birthdays, years, grads, etc. Then run:

    $ python uwastromsg.py

which creates/updates the `scheduler.sh` file. Then, source the
`scheduler.sh` file to create the `at` jobs by running:

    $ source scheduler.sh

You can now check which `at` jobs are scheduled in the queue
by running:

    $ atq

For more help with `at` jobs, try:

    $ man at

The login information for the uwastrograd account should be 
saved in text files in this directory -- if you don't have 
that info, contact Brett at bmmorris@uw.edu, otherwise no
emails will be sent.

Last edit: December 5th, 2018. Created on Sep 27, 2014 by 
Brett Morris. Built upon the enduring work of "THE LEGENDARY 
YUSRA ALSAYYAD" who wrote the original version on 
"JULY 6, 2013, WHILE LONELY AT MRO."

Jave Note:

If you run into issues, try the following in an ipython console:

from uwastromsg import send_email

send_email(from_address, to_address, cc_address, from_address, subject, message)

to see if emails can be properly sent!

"""

import datetime  # For handling dates
import smtplib   # For sending emails with Simple Mail Transfer Protocol
from email.mime.text import MIMEText # Email management object
from glob import glob # Search for file paths
import os        # Interface with file system
import sys       # For retrieving command line arguments

# Change this if you're trying the script out!
debug = False

# Paths to input files and settings
birthdayspath = 'birthdays.txt'       # File with names and next birthdays

# Debug: send in now + minute

if debug:
	warningtime = datetime.datetime.now() + datetime.timedelta(seconds=120)
	warningtime = warningtime.strftime("%I:%M%p")
else:
	warningtime = '9:00am'                    # Time to send email warnings, in local time for the running machine.

admin_emailaddress = 'tzdw@uw.edu'    # Person launching the script
astrogrademail = 'uwastrograds@gmail.com' # Astro grad email address
message_subject = "Happy birthday {0}!!!" # Subject line of emails
#pythonpath = '/astro/apps6/anaconda2.0/bin/python'        # Which Python to use
pythonpath = "/astro/apps6/opt/anaconda2.4/bin/python"
thisfilepath = os.path.abspath(__file__)                  # Path to this file
logfilepath = os.path.abspath(os.path.join(os.path.dirname(__file__),'log.txt'))
logfile = open(logfilepath, 'a')
schedulerpath = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             'scheduler.sh'))

def prepare_scheduler():
    '''
    Make a `scheduler.sh` script that can be sourced to prepare the `at` jobs. 
    Run the script with: 
        $ source scheduler.sh
    '''
    birthdayslist = open(birthdayspath, 'r').readlines()
    # Get absolute paths to the message content files

    scheduler = open(schedulerpath, 'w') # Open the scheduler file (output)
    
    for birthday in birthdayslist:
        # From the birthday list: get the name, and date of birthday
        uname = birthday.split()[0]
        name = birthday.split()[1]
        month, day, year = map(int,birthday.split()[2:5])
        birthdaydate = datetime.datetime(year, month, day)
                                           
        
        scheduleline_birthday = ('echo \"{} {} {} {} \" | at {} {} \n'.format(pythonpath, 
                                                                                        thisfilepath, 
                                                                                        name,
                                                                                        uname,
                                                                                        warningtime, 
                                                                                        birthdaydate.strftime('%m%d%y')))
                                     
                                           
        scheduler.write(scheduleline_birthday)

    
    scheduler.close()

def send_email(from_address, to_address, cc_address, reply_to_address, subject, message=None):
    '''
    Send an email!
    '''
    name = subject.split()[2][:-3]
    if message is None:
            message = 'Wish {0} a <a href="https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&cad=rja&uact=8&ved=2ahUKEwiG89O96YnfAhXQJTQIHXh5DJMQjRx6BAgBEAU&url=https%3A%2F%2Fgiphy.com%2Fgifs%2Fbirthday-happy-pusheen-jxTnOS8Mkv8n6&psig=AOvVaw3MgGfOmRlFxhvVRFtXDL1i&ust=1544138277438054">happy birthday</a> today!'.format(name)
    msg = MIMEText(message.encode('utf-8'), 'html', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = from_address
    msg['To'] = to_address
    msg['cc'] = cc_address
    msg.add_header('reply-to', reply_to_address)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    # Read u and p
    username = open(os.path.join(os.path.dirname(__file__), 'u'), 'r').read().strip()
    p = open(os.path.join(os.path.dirname(__file__), 'p'),'r').read().strip()
    s.login(username, p)
    s.sendmail(from_address, [to_address] + [cc_address], msg.as_string())
    s.quit()    

if __name__ == "__main__":

    # When this script is run via command line:
    nargs = len(sys.argv)

    # If the script is run with no command line arguments:
    if nargs == 1:
        print('Preparing the scheduler.')
        prepare_scheduler()
        logmessage = ' '.join([str(datetime.datetime.now()), 'preparing scheduler'])+'\n'
        print('Updating log file: {}'.format(logfilepath))
        print('\nOnce complete, run:\n    source scheduler.sh')

    # Otherwise, assume the script is being run by an `at` job
    else:
        thisfilename, name, uname = sys.argv[:3]
        logmessage = ' '.join([str(datetime.datetime.now()),uname])+'\n'
        if uname != 'rerun':
                send_email(from_address=astrogrademail, 
                           to_address='astro-grads@astro.washington.edu', 
                           cc_address='{0}@uw.edu'.format(uname), 
                           reply_to_address=admin_emailaddress, 
                           subject=message_subject.format(name))
        else:
                send_email(from_address=astrogrademail,
                           to_address=admin_emailaddress,
                           cc_address=admin_emailaddress,
                           reply_to_address=astrogrademail,
                           subject='Rerun the birthday script!',
                           message='Hey, make sure the set up the birthday script ASAP!')
        logfile.write(logmessage)
        logfile.close()
