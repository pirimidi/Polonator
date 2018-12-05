"""
-------------------------------------------------------------------------------- 
 Author: Richard Terry.
 Date: February 12, 2008.
 Modified by: Mirko Palla
 Date: March 5, 2008.

 For: G.007 polony sequencer design [fluidics software] at the Church Lab - 
 Genetics Department, Harvard Medical School.
 
 Purpose: This program contains the complete code for class Temperature_control, 
 containing temperature controller communication subroutines in Python.

 This software may be used, modified, and distributed freely, but this
 header may not be modified and must appear at the top of this file. 
------------------------------------------------------------------------------- 
"""

import time

class Temperature_control:

	global serport

	def __init__(self, config, serial_port, logger=None):
		"Initialize PR-59 temperature controller object with default parameters."

		self._baud_rate = int(config.get("communication","temperature_control_baud"))
		self._read_length = int(config.get("communication","read_length"))
		self._sleep_time = float(config.get("communication","sleep_time"))

		if logger is not None:
			self.logging = logger

		self.serport = serial_port	
		self.state = 'temperature control initialized'

		self.logging.info("---\t-\t--> Temperature controller object constructed")

#--------------------------------------------------------------------------------------#
#												PR-59 temperature controller FUNCTIONS												 #
#--------------------------------------------------------------------------------------#
#
# Performs low-level functional commands (e.g. set target temperature, PID constants, 
# etc). Each command implemented here must know the command set of the hardware being 
# controlled, but does not need to know how to communicate with the device (how to poll 
# it, etc). Each functional command will block until execution is complete.
#
#--------------------------------------------------------------------------------------#
#																	BASIC SETTINGS																			 #
#--------------------------------------------------------------------------------------#

	def set_control_on(self):
		"Sets RUN flag in regulator, so main output is opened."

		self.serport.set_baud(self._baud_rate)
		find_string = '\r'
		response_string_size = 10
		self.serport.parse_read_string('$W\r', find_string, response_string_size)	# set RUN flag command

		self.logging.info("---\t-\t--> Set temperature control ON")

	def set_control_off(self):
		"Clears RUN flag in regulator, so main output is blocked."

		self.serport.set_baud(self._baud_rate)
		find_string = '\r'
		response_string_size = 10
		self.serport.parse_read_string('$Q\r', find_string, response_string_size)	# clear RUN flag command 

		self.logging.info("---\t-\t--> Set temperature control OFF")

#--------------------------------------------------------------------------------------#
#																REGULATOR SETTINGS											 							 #
#--------------------------------------------------------------------------------------#

	def set_temperature(self, temperature):
		"Sets main temperature reference (C), a float - register [0]."

		self.set_control_on()
		temp_string = '$R0=' + str(temperature) + '\r'	# set register 0 value to 'temperature', a float
		find_string = '\r'
		response_string_size = 11
		self.serport.parse_read_string(temp_string, find_string, response_string_size)

		self.logging.info("---\t-\t--> Set temperature controller to %i C [set_temp]" % temperature)

#--------------------------------------------------------------------------------------#
#																	STATUS CHECKING																			 #
#--------------------------------------------------------------------------------------#

	def get_temperature(self):
		"Gets temperature sensor 1 reading, a float - register [100]."

		self.serport.set_baud(self._baud_rate)

		find_string = '\r'
		response_string_size = 21

		temperature = self.serport.parse_read_string('$R100?\r', find_string, response_string_size)	# get register 100 value, a float
		string_start_index = temperature.find('+')
		string_end_index = temperature.find('e')
		temperature = float(temperature[string_start_index : string_end_index] + 'e+01')

		#self.logging.info("---\t-\t--> Get current temperature: %i C" % temperature)
		return temperature

