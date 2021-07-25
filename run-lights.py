#!/usr/bin/python

import datetime
import blinkt
import sys
import getopt
import json


# run-lights.py 
#
# Checks the current time of day and sets the LED lights to the appropriate color
# Based on the current time of day.
# This is used as an "OK to Wake" clock for overnight and during naps
#
# The lighting schedule is listed below the functions
#

# Intensity of the LEDs from 0.0 to 1.0
intensity = 0.1
day_intensity = 0.2

#########################################
# Functions
#########################################
def time_in_range(start, end, x):
	# Return true if x is in the range [start, end]
	if start <= end:
		return start <= x <= end
	else:
		return start <= x or x <= end

def clear_lights():
	# turn lights off
	blinkt.clear()
	blinkt.show()

def lights_on_green():
	# green
	#blinkt.set_all(0,255,0,intensity)
	blinkt.set_pixel(0,0,255,0,0)
	blinkt.set_pixel(1,0,255,0,0)
	blinkt.set_pixel(2,0,255,0,0)
	blinkt.set_pixel(3,0,255,0,intensity)
	blinkt.set_pixel(4,0,255,0,0)
	blinkt.set_pixel(5,0,255,0,0)
	blinkt.set_pixel(6,0,255,0,0)
	blinkt.set_pixel(7,0,255,0,0)
	blinkt.set_clear_on_exit(False)
	blinkt.show()

def lights_on_yellow():
	# yellow / orange
	#blinkt.set_all(255,69,0,intensity)
	blinkt.set_pixel(0,255,69,0,0)
	blinkt.set_pixel(1,255,69,0,0)
	blinkt.set_pixel(2,255,69,0,intensity)
	blinkt.set_pixel(3,255,69,0,0)
	blinkt.set_pixel(4,255,69,0,0)
	blinkt.set_pixel(5,255,69,0,intensity)
	blinkt.set_pixel(6,255,69,0,0)
	blinkt.set_pixel(7,255,69,0,0)
	blinkt.set_clear_on_exit(False)
	blinkt.show()

#########################################
# End Functions
#########################################

#########################################
# Main
#########################################
def main(argv):
	printonly = False

	opts, args = getopt.getopt(argv,"p",["printonly"])
	for opt, arg in opts:
		if opt in ("-p", "--printonly"):
			printonly = True

	# Get the current date and time and assign 
	# to a variable to be used later
	dto = datetime.datetime.now()
	time = dto.time()
	
	# Read in the sleep schedule from the file
	scheduleFile = open('/var/www/html/nap-schedule.json')
	times = json.load(scheduleFile)
	scheduleFile.close()
	bedtimeStart = times['bedtimeStart'].split(":")
	bedStartHour = int(bedtimeStart[0])
	bedStartMinute = int(bedtimeStart[1])
	bedtimeEnd = times['bedtimeEnd'].split(":")
	bedEndHour = int(bedtimeEnd[0])
	bedEndMinute = int(bedtimeEnd[1])
	naptimeStart = times['naptimeStart'].split(":")
	napStartHour = int(naptimeStart[0])
	napStartMinute = int(naptimeStart[1])
	naptimeEnd = times['naptimeEnd'].split(":")
	napEndHour = int(naptimeEnd[0])
	napEndMinute = int(naptimeEnd[1])
	
	#########################################
	# Overnight Schedule
	#########################################
	# Have 2 clauses for crossing the overnight barrier
	# Starts at start time and goes to midnight
	# Starts from midnight and goes to end time
	# Yellow light during night time
	# Green light for 1 hour after night time
	night1_start = datetime.time(bedStartHour,bedStartMinute,0)
	night1_end = datetime.time(0,0,0)
	night2_start = datetime.time(0,0,0)
	night2_end = datetime.time(bedEndHour,bedEndMinute,0)
	morning_start = datetime.time(bedEndHour,bedEndMinute,0)
	morning_end = datetime.time(bedEndHour+1,bedEndMinute,0)
	
	#########################################
	# Nap Schedule
	#########################################
	# Yellow light during nap time
	# Green light for 1 hour after nap time
	nap_start = datetime.time(napStartHour,napStartMinute,0)
	nap_end = datetime.time(napEndHour,napEndMinute,0)
	wake_start = datetime.time(napEndHour,napEndMinute,0)
	wake_end = datetime.time(napEndHour+1,napEndMinute,0)
	
	# Lights are off otherwise
	
	# Check if the current time is in one of the ranges
	if time_in_range(night1_start,night1_end,time):
		# yellow
		if printonly:
			print("yellow")
		else:
			lights_on_yellow()
	elif time_in_range(night2_start,night2_end,time):
		# yellow
		if printonly:
			print("yellow")
		else:
			lights_on_yellow()
	elif time_in_range(morning_start,morning_end,time):
		# green
		if printonly:
			print("green")
		else:
			lights_on_green()
	elif time_in_range(nap_start,nap_end,time):
		# yellow
		if printonly:
			print("yellow")
		else:
			lights_on_yellow()
	elif time_in_range(wake_start,wake_end,time):
		# green
		if printonly:
			print("green")
		else:
			lights_on_green()
	else:
		# off
		if printonly:
			print("black")
		else:
			clear_lights()

## Run the main program
if __name__ == "__main__":
	main(sys.argv[1:])

#########################################
# End 
#########################################
