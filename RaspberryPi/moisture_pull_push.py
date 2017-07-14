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

#############
# Functions #
#############
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
    usb = get_usb()