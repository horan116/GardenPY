#!/usr/bin/python3
'''
Here we are going to manage pulling moisture data from our sensor as well
as pushing this data in a proper fashion to AWS SQS. We are going to assume
that the aws cli is installed and configured.
'''

###########
# Imports #
###########

import time
import serial
import subprocess
import logging

###########
# Globals #
###########

logfile = "/var/log/moisture_pull_push.log"

###########
# Logging #
###########

logging.basicConfig(filename=logfile, 
                    level=logging.INFO,
                    format="%(asctime)s:%(levelname)s:%(message)s")

###########
# Classes #
###########

#############
# Functions #
#############
def get_usb():
	# Lets make sure we have the correct usb device because it has been sketchy at best it being USB0
    try:
	    ls = subprocess.Popen(['ls', '/dev/'], stdout=subprocess.PIPE)
	    output = subprocess.check_output(['grep', '-i', 'usb'], stdin=ls.stdout)
	    return output.decode('utf-8').strip()

    except CalledProcessError as e:
        logging.error("Failed to find USB Device. Make sure your Arduino is attach to this Pi.")
        logging.error(e)


########
# Main #
########

if __name__ == '__main__':
    usb = get_usb()