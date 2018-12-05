"""
-------------------------------------------------------------------------------- 
 Author: Rich Terry.
 Date: February 12, 2008.
 Modified by: Mirko Palla
 Date: March 5, 2008.

 For: G.007 polony sequencer design [fluidics software] at the Church Lab - 
 Genetics Department, Harvard Medical School.
 
 Purpose: This program contains the complete code for class Rotary_valve, 
 containing rotary valve communication subroutines in Python.

 This software may be used, modified, and distributed freely, but this
 header may not be modified and must appear at the top of this file. 
------------------------------------------------------------------------------- 
"""

class Rotary_valve:

	global serport;

	def __init__(self, config, serial_port, logger=None):
		"Initialize Rheodyne rotary valve object with default parameters."

		self._baud_rate = int(config.get("communication","rotary_valve_baud"))
		self._read_length = int(config.get("communication","read_length"))
		self._sleep_time = float(config.get("communication","sleep_time"))

		if logger is not None:
			self.logging = logger

		self.serport = serial_port		
		self.state = 'rotary valve initialized'

		self.logging.info("---\t-\t--> Rotary valve object constructed")		

#--------------------------------------------------------------------------------------#
#													 Rheodyne rotary valve FUNCTIONS														 #
#--------------------------------------------------------------------------------------#
#
# Performs low-level functional commands (e.g. set rotary valve position). Each command 
# implemented here must know the command set of the hardware being controlled, but does 
# not need to know how to communicate with the device (how to poll it, etc). Each 
# functional command will block until execution is complete.
#
#--------------------------------------------------------------------------------------#
#																	BASIC SETTINGS																			 #
#--------------------------------------------------------------------------------------#

	def set_valve_position(self, valve_position):
		"Switch valve to given port on rotary valve, an integer."

		self.serport.set_baud(self._baud_rate)	# set baud rate of rotary valve

		valve_position = '0' + (str(hex(valve_position)[2:])).capitalize()
		valve_position_string = 'P' + valve_position + '\r'

		self.serport.write_serial(valve_position_string)

		find_string = valve_position
		response_string_size = 2

		self.serport.parse_read_string('S\r', find_string, response_string_size)

		self.logging.info("---\t-\t--> Set rotary valve to position %s" % valve_position)

