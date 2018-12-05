"""
-------------------------------------------------------------------------------- 
 Author: Mirko Palla.
 Date: February 19, 2008.
 Modified: Richard Terry
 Date: March 5, 2008.
 For: G.007 polony sequencer design [fluidics software] at the Church Lab - 
 Genetics Department, Harvard Medical School.
 
 Purpose: This program contains the complete code for class Mux, containing
 multiplexer communication subroutines in Python.

 This software may be used, modified, and distributed freely, but this
 header may not be modified and must appear at the top of this file. 
------------------------------------------------------------------------------- 
"""

import sys
import getpass
import time
from tel_net import Tel_net

class Mux:

	global mux_state
	global mux_state_00
	global session
	mux_state_00 = ([0,0,0,0,0])

	def __init__(self, logger=None):
		"""Initialize Ultimac Mux R/P PCB mux object with default parameters"""

		if logger is not None:			# if defined, place logger into Mux
			self.logging = logger

		self.session = Tel_net()

		mux_state = ([0,0,0,0,0,1,0,0])
		mux_state_00 = ([0,0,0,0,0])

		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		self.session.parse_read_string('m_dout[0]=' + str(mux_state[0]), '>')
		self.session.parse_read_string('m_dout[1]=' + str(mux_state[1]), '>')
		self.session.parse_read_string('m_dout[2]=' + str(mux_state[2]), '>')
		self.session.parse_read_string('m_dout[3]=' + str(mux_state[3]), '>')
		self.session.parse_read_string('m_dout[4]=' + str(mux_state[4]), '>')
		self.session.parse_read_string('m_dout[6]=' + str(mux_state[6]), '>')
		self.session.parse_read_string('m_dout[7]=' + str(mux_state[7]), '>')
		mux_state[5] = 0
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		mux_state[5] = 1
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		mux_state = ([0,0,0,0,0,0,1,0])
		self.session.parse_read_string('m_dout[6]=' + str(mux_state[6]), '>')
		self.session.parse_read_string('m_dout[7]=' + str(mux_state[7]), '>')
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		mux_state[5] = 1
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		mux_state = ([0,0,0,0,0,0,0,1])
		self.session.parse_read_string('m_dout[6]=' + str(mux_state[6]), '>')
		self.session.parse_read_string('m_dout[7]=' + str(mux_state[7]), '>')
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		mux_state[5] = 1
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		mux_state = ([0,0,0,0,0,0,1,1])
		self.session.parse_read_string('m_dout[6]=' + str(mux_state[6]), '>')
		self.session.parse_read_string('m_dout[7]=' + str(mux_state[7]), '>')
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		mux_state[5] = 1
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')

		self.logging.info("---\t-\t--> Mux object constructed")

#--------------------------------------------------------------------------------------#
#	 Ultimac Mux R/P PCB FUNCTIONS	 #
#--------------------------------------------------------------------------------------#

    # Discrete valves

	def discrete_valve4_open(self):
		"Sets valve V4 to ON state"
		mux_state_00[0] = 1
		mux_state = ([0,0,0,0,0,1,0,0])
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		self.session.parse_read_string('m_dout[0]=' + str(mux_state_00[0]), '>')
		self.session.parse_read_string('m_dout[1]=' + str(mux_state_00[1]), '>')
		self.session.parse_read_string('m_dout[2]=' + str(mux_state_00[2]), '>')
		self.session.parse_read_string('m_dout[3]=' + str(mux_state_00[3]), '>')
		self.session.parse_read_string('m_dout[4]=' + str(mux_state_00[4]), '>')
		self.session.parse_read_string('m_dout[6]=' + str(mux_state[6]), '>')
		self.session.parse_read_string('m_dout[7]=' + str(mux_state[7]), '>')
		mux_state[5] = 0
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		mux_state[5] = 1
		#self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		self.logging.info("---\t-\t--> Switch 3-way discrete valve V4 to NO (ligase)")

	def discrete_valve4_close(self):
		"Sets valve V4 to OFF state"
		mux_state_00[0] = 0
		mux_state = ([0,0,0,0,0,1,0,0])
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		self.session.parse_read_string('m_dout[0]=' + str(mux_state_00[0]), '>')
		self.session.parse_read_string('m_dout[1]=' + str(mux_state_00[1]), '>')
		self.session.parse_read_string('m_dout[2]=' + str(mux_state_00[2]), '>')
		self.session.parse_read_string('m_dout[3]=' + str(mux_state_00[3]), '>')
		self.session.parse_read_string('m_dout[4]=' + str(mux_state_00[4]), '>')
		self.session.parse_read_string('m_dout[6]=' + str(mux_state[6]), '>')
		self.session.parse_read_string('m_dout[7]=' + str(mux_state[7]), '>')
		mux_state[5] = 0
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		mux_state[5] = 1
		#self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		self.logging.info("---\t-\t--> Switch 3-way discrete valve V4 to NC (ligase buffer)")

	def discrete_valve5_open(self):
		"Sets valve V5 to ON state"
		mux_state_00[1] = 1
		mux_state = ([0,0,0,0,0,1,0,0])
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		self.session.parse_read_string('m_dout[0]=' + str(mux_state_00[0]), '>')
		self.session.parse_read_string('m_dout[1]=' + str(mux_state_00[1]), '>')
		self.session.parse_read_string('m_dout[2]=' + str(mux_state_00[2]), '>')
		self.session.parse_read_string('m_dout[3]=' + str(mux_state_00[3]), '>')
		self.session.parse_read_string('m_dout[4]=' + str(mux_state_00[4]), '>')
		self.session.parse_read_string('m_dout[6]=' + str(mux_state[6]), '>')
		self.session.parse_read_string('m_dout[7]=' + str(mux_state[7]), '>')
		mux_state[5] = 0
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		mux_state[5] = 1
		#self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		self.logging.info("---\t-\t--> Switch 3-way discrete valve V5 to NO (from V3 to FC)")

	def discrete_valve5_close(self):
		"Sets valve V5 to OFF state"
		mux_state_00[1] = 0
		mux_state = ([0,0,0,0,0,1,0,0])
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		self.session.parse_read_string('m_dout[0]=' + str(mux_state_00[0]), '>')
		self.session.parse_read_string('m_dout[1]=' + str(mux_state_00[1]), '>')
		self.session.parse_read_string('m_dout[2]=' + str(mux_state_00[2]), '>')
		self.session.parse_read_string('m_dout[3]=' + str(mux_state_00[3]), '>')
		self.session.parse_read_string('m_dout[4]=' + str(mux_state_00[4]), '>')
		self.session.parse_read_string('m_dout[6]=' + str(mux_state[6]), '>')
		self.session.parse_read_string('m_dout[7]=' + str(mux_state[7]), '>')
		mux_state[5] = 0
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		mux_state[5] = 1
		#self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		self.logging.info("---\t-\t--> Switch 3-way discrete valve V5 to NC (from mixer to FC)")

	def discrete_valve6_open(self):
		"Sets valve V6 to ON state"
		mux_state_00[2] = 1
		mux_state = ([0,0,0,0,0,1,0,0])
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		self.session.parse_read_string('m_dout[0]=' + str(mux_state_00[0]), '>')
		self.session.parse_read_string('m_dout[1]=' + str(mux_state_00[1]), '>')
		self.session.parse_read_string('m_dout[2]=' + str(mux_state_00[2]), '>')
		self.session.parse_read_string('m_dout[3]=' + str(mux_state_00[3]), '>')
		self.session.parse_read_string('m_dout[4]=' + str(mux_state_00[4]), '>')
		self.session.parse_read_string('m_dout[6]=' + str(mux_state[6]), '>')
		self.session.parse_read_string('m_dout[7]=' + str(mux_state[7]), '>')
		mux_state[5] = 0
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		mux_state[5] = 1
		#self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		self.logging.info("---\t-\t--> Switch 3-way discrete valve V6 to NO (through FC 2)") 

	def discrete_valve6_close(self):
		"Sets valve V6 to OFF state"
		mux_state_00[2] = 0
		mux_state = ([0,0,0,0,0,1,0,0])
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		self.session.parse_read_string('m_dout[0]=' + str(mux_state_00[0]), '>')
		self.session.parse_read_string('m_dout[1]=' + str(mux_state_00[1]), '>')
		self.session.parse_read_string('m_dout[2]=' + str(mux_state_00[2]), '>')
		self.session.parse_read_string('m_dout[3]=' + str(mux_state_00[3]), '>')
		self.session.parse_read_string('m_dout[4]=' + str(mux_state_00[4]), '>')
		self.session.parse_read_string('m_dout[6]=' + str(mux_state[6]), '>')
		self.session.parse_read_string('m_dout[7]=' + str(mux_state[7]), '>')
		mux_state[5] = 0
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		mux_state[5] = 1
		#self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		self.logging.info("---\t-\t--> Switch 3-way discrete valve V6 to NC (through FC 1)")

	def discrete_valve7_open(self):
		"Sets valve V7 to ON state"
		mux_state_00[3] = 1
		mux_state = ([0,0,0,0,0,1,0,0])
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		self.session.parse_read_string('m_dout[0]=' + str(mux_state_00[0]), '>')
		self.session.parse_read_string('m_dout[1]=' + str(mux_state_00[1]), '>')
		self.session.parse_read_string('m_dout[2]=' + str(mux_state_00[2]), '>')
		self.session.parse_read_string('m_dout[3]=' + str(mux_state_00[3]), '>')
		self.session.parse_read_string('m_dout[4]=' + str(mux_state_00[4]), '>')
		self.session.parse_read_string('m_dout[6]=' + str(mux_state[6]), '>')
		self.session.parse_read_string('m_dout[7]=' + str(mux_state[7]), '>')
		mux_state[5] = 0
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		mux_state[5] = 1
		#self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		self.logging.info("---\t-\t--> Switch 3-way discrete valve V7 to NO (dH2O)")

	def discrete_valve7_close(self):
		"Sets valve V7 to OFF state"
		mux_state_00[3] = 0
		mux_state = ([0,0,0,0,0,1,0,0])
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		self.session.parse_read_string('m_dout[0]=' + str(mux_state_00[0]), '>')
		self.session.parse_read_string('m_dout[1]=' + str(mux_state_00[1]), '>')
		self.session.parse_read_string('m_dout[2]=' + str(mux_state_00[2]), '>')
		self.session.parse_read_string('m_dout[3]=' + str(mux_state_00[3]), '>')
		self.session.parse_read_string('m_dout[4]=' + str(mux_state_00[4]), '>')
		self.session.parse_read_string('m_dout[6]=' + str(mux_state[6]), '>')
		self.session.parse_read_string('m_dout[7]=' + str(mux_state[7]), '>')
		mux_state[5] = 0
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		mux_state[5] = 1
		#self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		self.logging.info("---\t-\t--> Switch 3-way discrete valve V7 to NC (air)")

    	# Reagent mixer

	def mixer_ON(self):
		"Mixing in mixer: ON"
		mux_state_00[4] = 1
		mux_state = ([0,0,0,0,0,1,0,0])
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		self.session.parse_read_string('m_dout[0]=' + str(mux_state_00[0]), '>')
		self.session.parse_read_string('m_dout[1]=' + str(mux_state_00[1]), '>')
		self.session.parse_read_string('m_dout[2]=' + str(mux_state_00[2]), '>')
		self.session.parse_read_string('m_dout[3]=' + str(mux_state_00[3]), '>')
		self.session.parse_read_string('m_dout[4]=' + str(mux_state_00[4]), '>')
		self.session.parse_read_string('m_dout[6]=' + str(mux_state[6]), '>')
		self.session.parse_read_string('m_dout[7]=' + str(mux_state[7]), '>')
		mux_state[5] = 0
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		mux_state[5] = 1
		#self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		self.logging.info("---\t-\t--> Mixing chamber in use")

	def mixer_OFF(self):
		"Mixing in mixer: OFF"
		mux_state_00[4] = 0
		mux_state = ([0,0,0,0,0,1,0,0])
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		self.session.parse_read_string('m_dout[0]=' + str(mux_state_00[0]), '>')
		self.session.parse_read_string('m_dout[1]=' + str(mux_state_00[1]), '>')
		self.session.parse_read_string('m_dout[2]=' + str(mux_state_00[2]), '>')
		self.session.parse_read_string('m_dout[3]=' + str(mux_state_00[3]), '>')
		self.session.parse_read_string('m_dout[4]=' + str(mux_state_00[4]), '>')
		self.session.parse_read_string('m_dout[6]=' + str(mux_state[6]), '>')
		self.session.parse_read_string('m_dout[7]=' + str(mux_state[7]), '>')
		mux_state[5] = 0
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		mux_state[5] = 1
		#self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		self.logging.info("---\t-\t--> Mixing chamber is off")

    	# Flowcell heater/cooler

	def set_to_temperature_control1(self):
		"Communication channel set to temperature controller 1"
		mux_state = ([0,0,0,0,0,1,0,1])
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		self.session.parse_read_string('m_dout[0]=' + str(mux_state[0]), '>')
		self.session.parse_read_string('m_dout[1]=' + str(mux_state[1]), '>')
		self.session.parse_read_string('m_dout[2]=' + str(mux_state[2]), '>')
		self.session.parse_read_string('m_dout[3]=' + str(mux_state[3]), '>')
		self.session.parse_read_string('m_dout[4]=' + str(mux_state[4]), '>')
		self.session.parse_read_string('m_dout[6]=' + str(mux_state[6]), '>')
		self.session.parse_read_string('m_dout[7]=' + str(mux_state[7]), '>')
		mux_state[5] = 0
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		mux_state[5] = 1
		#self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		self.logging.info("---\t-\t--> Switch communication to temperature controller 1")

	def set_to_temperature_control2(self):
		"Communication channel set to temperature controller 2"
		mux_state = ([1,0,0,0,0,1,0,1])
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		self.session.parse_read_string('m_dout[0]=' + str(mux_state[0]), '>')
		self.session.parse_read_string('m_dout[1]=' + str(mux_state[1]), '>')
		self.session.parse_read_string('m_dout[2]=' + str(mux_state[2]), '>')
		self.session.parse_read_string('m_dout[3]=' + str(mux_state[3]), '>')
		self.session.parse_read_string('m_dout[4]=' + str(mux_state[4]), '>')
		self.session.parse_read_string('m_dout[6]=' + str(mux_state[6]), '>')
		self.session.parse_read_string('m_dout[7]=' + str(mux_state[7]), '>')
		mux_state[5] = 0
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		mux_state[5] = 1
		#self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		self.logging.info("---\t-\t--> Switch communication to temperature controller 2")

	def set_to_reagent_block_cooler(self):
		"Communication channel set to reagent block cooler"
		mux_state = ([0,1,0,0,0,1,0,1])
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		self.session.parse_read_string('m_dout[0]=' + str(mux_state[0]), '>')
		self.session.parse_read_string('m_dout[1]=' + str(mux_state[1]), '>')
		self.session.parse_read_string('m_dout[2]=' + str(mux_state[2]), '>')
		self.session.parse_read_string('m_dout[3]=' + str(mux_state[3]), '>')
		self.session.parse_read_string('m_dout[4]=' + str(mux_state[4]), '>')
		self.session.parse_read_string('m_dout[6]=' + str(mux_state[6]), '>')
		self.session.parse_read_string('m_dout[7]=' + str(mux_state[7]), '>')
		mux_state[5] = 0
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		mux_state[5] = 1
		#self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		self.logging.info("---\t-\t--> Switch communication to reagent block cooler")

    	# Rotary valves

	def set_to_rotary_valve1(self):
		"Communication channel set to rotary valve 1"
		mux_state = ([0,0,1,0,0,1,0,1])
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		self.session.parse_read_string('m_dout[0]=' + str(mux_state[0]), '>')
		self.session.parse_read_string('m_dout[1]=' + str(mux_state[1]), '>')
		self.session.parse_read_string('m_dout[2]=' + str(mux_state[2]), '>')
		self.session.parse_read_string('m_dout[3]=' + str(mux_state[3]), '>')
		self.session.parse_read_string('m_dout[4]=' + str(mux_state[4]), '>')
		self.session.parse_read_string('m_dout[6]=' + str(mux_state[6]), '>')
		self.session.parse_read_string('m_dout[7]=' + str(mux_state[7]), '>')
		mux_state[5] = 0
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		mux_state[5] = 1
		#self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		self.logging.info("---\t-\t--> Switch communication to ten port rotary valve V1")

	def set_to_rotary_valve2(self):
		"Communication channel set to rotary valve 2"
		mux_state = ([1,0,1,0,0,1,0,1])
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		self.session.parse_read_string('m_dout[0]=' + str(mux_state[0]), '>')
		self.session.parse_read_string('m_dout[1]=' + str(mux_state[1]), '>')
		self.session.parse_read_string('m_dout[2]=' + str(mux_state[2]), '>')
		self.session.parse_read_string('m_dout[3]=' + str(mux_state[3]), '>')
		self.session.parse_read_string('m_dout[4]=' + str(mux_state[4]), '>')
		self.session.parse_read_string('m_dout[6]=' + str(mux_state[6]), '>')
		self.session.parse_read_string('m_dout[7]=' + str(mux_state[7]), '>')
		mux_state[5] = 0
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		mux_state[5] = 1
		#self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		self.logging.info("---\t-\t--> Switch communication to ten port rotary valve V2")

	def set_to_rotary_valve3(self):
		"Communication channel set to rotary valve 3"
		mux_state = ([0,1,1,0,0,1,0,1])
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		self.session.parse_read_string('m_dout[0]=' + str(mux_state[0]), '>')
		self.session.parse_read_string('m_dout[1]=' + str(mux_state[1]), '>')
		self.session.parse_read_string('m_dout[2]=' + str(mux_state[2]), '>')
		self.session.parse_read_string('m_dout[3]=' + str(mux_state[3]), '>')
		self.session.parse_read_string('m_dout[4]=' + str(mux_state[4]), '>')
		self.session.parse_read_string('m_dout[6]=' + str(mux_state[6]), '>')
		self.session.parse_read_string('m_dout[7]=' + str(mux_state[7]), '>')
		mux_state[5] = 0
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		mux_state[5] = 1
		#self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		self.logging.info("---\t-\t--> Switch communication to ten port rotary valve V3")

	def set_to_rotary_valve4(self):
		"Communication channel set to rotary valve 3"
		mux_state = ([1,1,1,0,0,1,0,1])
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		self.session.parse_read_string('m_dout[0]=' + str(mux_state[0]), '>')
		self.session.parse_read_string('m_dout[1]=' + str(mux_state[1]), '>')
		self.session.parse_read_string('m_dout[2]=' + str(mux_state[2]), '>')
		self.session.parse_read_string('m_dout[3]=' + str(mux_state[3]), '>')
		self.session.parse_read_string('m_dout[4]=' + str(mux_state[4]), '>')
		self.session.parse_read_string('m_dout[6]=' + str(mux_state[6]), '>')
		self.session.parse_read_string('m_dout[7]=' + str(mux_state[7]), '>')
		mux_state[5] = 0
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		mux_state[5] = 1
		#self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		self.logging.info("---\t-\t--> Switch communication to ten port rotary valve V3")


    	# Syringe pump

	def set_to_syringe_pump(self):
		"Communication channel set to syringe pump"
		mux_state = ([1,1,0,0,0,1,0,1])
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		self.session.parse_read_string('m_dout[0]=' + str(mux_state[0]), '>')
		self.session.parse_read_string('m_dout[1]=' + str(mux_state[1]), '>')
		self.session.parse_read_string('m_dout[2]=' + str(mux_state[2]), '>')
		self.session.parse_read_string('m_dout[3]=' + str(mux_state[3]), '>')
		self.session.parse_read_string('m_dout[4]=' + str(mux_state[4]), '>')
		self.session.parse_read_string('m_dout[6]=' + str(mux_state[6]), '>')
		self.session.parse_read_string('m_dout[7]=' + str(mux_state[7]), '>')
		mux_state[5] = 0
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		mux_state[5] = 1
		#self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		self.logging.info("---\t-\t--> Switch communication to syringe pump")

	def __del__(self):
		mux_state = ([0,0,0,0,0,0])
		self.session.parse_read_string('m_dout[0]=' + str(mux_state[0]), '>')
		self.session.parse_read_string('m_dout[1]=' + str(mux_state[1]), '>')
		self.session.parse_read_string('m_dout[2]=' + str(mux_state[2]), '>')
		self.session.parse_read_string('m_dout[3]=' + str(mux_state[3]), '>')
		self.session.parse_read_string('m_dout[4]=' + str(mux_state[4]), '>')
		self.session.parse_read_string('m_dout[5]=' + str(mux_state[5]), '>')
		self.session.parse_read_string('m_dout[6]=' + str(1), '>')
		self.session.parse_read_string('m_dout[7]=' + str(1), '>')
		self.session.parse_read_string('m_dout[6]=' + str(0), '>')
		self.session.parse_read_string('m_dout[7]=' + str(0), '>')
		self.session.parse_read_string('m_dout[6]=' + str(1), '>')
		self.session.parse_read_string('m_dout[7]=' + str(0), '>')
		self.session.parse_read_string('m_dout[6]=' + str(0), '>')
		return

