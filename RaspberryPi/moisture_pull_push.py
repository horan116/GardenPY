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
import sys.exit
import os.path, os.getusername
import serial
import subprocess
import logging
import boto3

###########
# Globals #
###########

logfile = "/var/log/moisture_pull_push.log"

###########
# Logging #
###########

try:
    logging.basicConfig(filename=logfile, 
                        level=logging.INFO,
                        format="%(asctime)s:%(levelname)s:%(message)s")
                    
except PermissionError as e:
    print("Unable to write to file. Run with elevated priv's or create file and give permissions to this user.")
    print(e)

###########
# Classes #
###########

class SQS():
    '''
    Here is are going to manage our SQS calls. While we could keep this linear, encapsulation
    will make this easier to manage as multiple developers interact with this script. Remember
    we will be following best practices, aws configure should be ran ahead of time. 
    '''

    def __init__(self):
        '''
        Some definitions that we can set during instantiation for the SQS Queue.
        '''
        self.sqs = boto3.client('sqs')
        self.queue_name = "GardenPY"
        self.queue_url = self.sqs.list_queues(QueueNamePrefix="GardenPY")['QueueUrls'][0]

    def get_queue_name(self):
        '''
        Getter used for troubleshooting
        '''
        return self.queue_name
    
    def get_queue_url(self):
        '''
        Getter used for troubleshooting
        '''
        return self.queue_url

#############
# Functions #
#############

def check_aws():
    # Lets make sure our AWS configuration has taken place.
    if not os.path.isfile(os.path.expanduser('~/.aws/credentials')) or not os.path.isfile(os.path.expanduser('~/.aws/config')):
        print("Cannot locate configuration files for AWS for {}.".format(os.getusername()))
        sys.exit(0)

def get_usb():
	# Lets make sure we have the correct usb device because it has been sketchy at best it being USB0
    try:
	    ls = subprocess.Popen(['ls', '/dev/'], stdout=subprocess.PIPE)
	    output = subprocess.check_output(['grep', '-i', 'usb'], stdin=ls.stdout)
	    return output.decode('utf-8').strip()

    except subprocess.CalledProcessError as e:
        logging.error("Failed to find USB Device. Make sure your Arduino is attach to this Pi.")
        logging.error(e)

def read_serial(usb):
	# Now that we have our USB device. Lets go ahead and pull the latest data from our soil.
	# Once some data is found on our serial connection, we will break the while loop and return the data.

	device = '/dev/{0}'.format(usb)
	
	input = serial.Serial(
	port=device,
	baudrate=9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1
	)

	while True:
		time.sleep(1)
		data = input.readline()
		if data:
			return data.strip()

########
# Main #
########

if __name__ == '__main__':
    logging.info("=====Beginning Execution=====")
    check_aws()
    usb = get_usb()
    data = read_serial(usb)
    sqs = SQS()
    print(sqs.get_queue_name())
    print(sqs.get_queue_url())


    