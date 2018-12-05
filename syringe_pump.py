"""
-------------------------------------------------------------------------------- 
 Author: Richard Terry.
 Date: February 12, 2008.
 Modified by: Mirko Palla
 Date: March 5, 2008.

 For: G.007 polony sequencer design [fluidics software] at the Church Lab - 
 Genetics Department, Harvard Medical School.
 
 Purpose: This program contains the complete code for class Syringe_pump, 
 containing Cavro XCalibur syringe pump communication subroutines in Python.

 This software may be used, modified, and distributed freely, but this
 header may not be modified and must appear at the top of this file. 
------------------------------------------------------------------------------- 
"""

class Syringe_pump:

	global serport

	def __init__(self, config, serial_port, logger=None):
		"Initialize Cavro XCalibur syringe pump object with default parameters."

		#--------------------------------- Serial configuration ---------------------------

		self._baud_rate = int(config.get("communication","syringe_pump_baud"))
		self._read_length = int(config.get("communication","read_length"))
		self._sleep_time = float(config.get("communication","sleep_time"))

		if logger is not None:
			self.logging = logger

		self.serport = serial_port				
		self.state = 'syringe pump initialized'

		self.logging.info("---\t-\t--> Syringe pump object constructed")

#--------------------------------------------------------------------------------------#
#												Cavro XCalibur syringe pump FUNCTIONS													 #
#--------------------------------------------------------------------------------------#
#
# Performs low-level functional commands (e.g. set pump flow rate, draw volume, etc). 
# Each command implemented here must know the command set of the hardware being 
# controlled, but does not need to know how to communicate with the device (how to poll 
# it, etc). Each functional command will block until execution is complete.
#

#--------------------------------------------------------------------------------------#
#																	BASIC SETTINGS																			 #
#--------------------------------------------------------------------------------------#

	def initialize_syringe(self):	
		"Initializes syringe pump with default operation settings."
					 
		self.serport.set_baud(self._baud_rate)

		# Initialize syringe dead volume
		self.serport.write_serial('/1k5R\r')
		self.serport.read_serial(3)

		find_string = chr(96)
		response_string_size = 4
		self.serport.parse_read_string('/1QR\r', find_string, response_string_size)

		# Initialize move to zero position, full dispense, full force
		self.serport.write_serial('/1Z0R\r')
		self.serport.read_serial(3)

		find_string = chr(96)
		response_string_size = 4
		self.serport.parse_read_string('/1QR\r', find_string, response_string_size)

		# Initialize speed, range is 0-40, the maximum speed is 0 (1.25 strokes/second)
		self.serport.write_serial('/1S20R\r')
		self.serport.read_serial(3)

		find_string = chr(96)
		response_string_size = 4
		self.serport.parse_read_string('/1QR\r', find_string, response_string_size)

		self.logging.info("---\t-\t--> Initialized syringe pump object")

	def set_valve_position(self, valve_position):
		"Sets to given syringe pump valve position, an integer"
					 
		self.serport.set_baud(self._baud_rate)

		self.serport.write_serial('/1I' + str(valve_position) + 'R\r')
		self.serport.read_serial(3)

		find_string = chr(96)
		response_string_size = 4
		self.serport.parse_read_string('/1QR\r', find_string, response_string_size)

		self.logging.info("---\t-\t--> Set syringe pump valve position to %i" % valve_position)

	def set_speed(self, speed):
		"""Sets syringe pump move speed (an integer) in range of 0-40, where the 
		maximum speed is 0 equivalent to 1.25 strokes/second = 1250 ul/s."""

		self.serport.set_baud(self._baud_rate)

		self.serport.write_serial('/1S' + str(speed) + 'R\r')
		self.serport.read_serial(3)

		find_string = chr(96)
		response_string_size = 4
		self.serport.parse_read_string('/1QR\r', find_string, response_string_size)

		self.logging.info("---\t-\t--> Set syringe pump speed to %i" % speed)

	def set_absolute_volume(self, absolute_volume):
		"""Sets syringe pump absolute volume (an integer) in ragne of 0-1000, where 0 is
		the syringe initial position and the maximum filling volume is the stroke of 
		the syringe (1000 ul)."""

		self.serport.set_baud(self._baud_rate)

		# Increments = (pump resolution * volume ul) / (syringe size ml * ul/ml)
		absolute_steps = (3000 * absolute_volume) / (1 * 1000)

		self.serport.write_serial('/1A' + str(absolute_steps) + 'R\r')	# 'P' command for relative pick-up, 'A' for absolute position 
		self.serport.read_serial(3)

		find_string = chr(96)
		response_string_size = 4
		self.serport.parse_read_string('/1QR\r', find_string, response_string_size)

		self.logging.info("---\t-\t--> Set syringe pump absolute volume to %i" % absolute_volume)

