"""
--------------------------------------------------------------------------------
 Author: Mirko Palla.
 Date: April 29, 2008.
 Modified: Richard Terry
 Date: July 11, 2008.

 For: G.007 polony sequencer design [fluidics software] at the Church Lab -
 Genetics Department, Harvard Medical School.
 
 Purpose: This program contains the complete code for module Biochem,
 containing re-occurring biochecmistry subroutines in Python.

 This software may be used, modified, and distributed freely, but this
 header may not be modified and must appear at the top of this file. 
------------------------------------------------------------------------------- 
"""

import sys 
import time 
import commands

import ConfigParser  # Import configuration file parser class.
from logger import Logger  # Import logger class.
from threading import Thread  # Import threading class.

from mux import Mux  # Import mux class.
from serial_port import Serial_port  # Import serial port class.

from syringe_pump import Syringe_pump  # Import syringe_pump class. 
from rotary_valve import Rotary_valve  # Import rotary valve class. 
from temperature_control import Temperature_control  # Import temperature controller class.

class Biochem(Thread):  # Biochem is a sub-class of a Thread object [inheritance]

	def __init__(self, cycle_name, flowcell, logger):
		"Initialize biochemistry object with default parameters."

		self.state = 'biochemistry object'

		self.cycle_name = cycle_name  # set cycle-name parameter to specified value
		self.cycle = cycle_name[0:3]  # set cycle parameter to specified value
		self.flowcell = flowcell  # set flowcell number to specified value

		self.config = ConfigParser.ConfigParser()  # create configuration file parser object
		self.config.read('config.txt')  # fill it in with configuration parameters from file

		self.logging = logger  # initialize logger object
		Thread.__init__(self)  # instantiate thread

		self.mux = Mux(self.logging)  # create mux
		self.ser = Serial_port(self.config, self.logging)  # place serial port into Biochem

		self.rotary_valve = Rotary_valve(self.config, self.ser, self.logging)  # create rotary valve
		self.syringe_pump = Syringe_pump(self.config, self.ser, self.logging)  # create syringe pump
		self.temperature_control = Temperature_control(self.config, self.ser, self.logging)  # create flowcell heater/cooler

		self.get_config_parameters()  # retrieve all configuatrion parameters from file
		self.logging.info("%s\t%i\t--> Biochemistry object is constructed: [%s]" % (self.cycle_name, self.flowcell, self.state))

#--------------------------------------------------------------------------------------# 
# 				COMPLEX FUNCTIONS 				       # 
#--------------------------------------------------------------------------------------#

#------------------------------- Get_config_parameters -------------------------------------

	def get_config_parameters(self):
		"""Retieves all biochemistry and device related configuration parameters from the confi-
		guration file using the ConfigParser facility. It assigns each parameter to a field of 
		the biochemistry object, thus it can access it any time during a run."""

		self.logging.info("%s\t%i\t--> Retrieve configuration parameters from file: [%s]" % (self.cycle_name, self.flowcell, self.state))

		#----------------------- Tubing configuration ----------------------------------

		self.syringe_dead_volume = int(self.config.get("tube_constants","syringe_dead_volume"))
		self.multi_dead_volume = int(self.config.get("tube_constants","multi_dead_volume"))
		self.discrete_dead_volume = int(self.config.get("tube_constants","discrete_dead_volume"))
		self.rotary_dead_volume = int(self.config.get("tube_constants","rotary_dead_volume"))

		self.channel_volume = int(self.config.get("tube_constants","channel_volume"))
		self.flowcell_volume = int(self.config.get("tube_constants","flowcell_volume"))

		self.dH2O_to_V4 = int(self.config.get("tube_constants","dH2O_to_V4"))
		self.wash1_to_V = int(self.config.get("tube_constants","wash1_to_V"))
		self.wash1_to_V4 = int(self.config.get("tube_constants","wash1_to_V4"))
		self.V_to_V4 = int(self.config.get("tube_constants","V_to_V4"))
		self.V4_to_T = int(self.config.get("tube_constants","V4_to_T"))
		self.V5_to_T = int(self.config.get("tube_constants","V5_to_T"))
		self.ligase_to_V5 = int(self.config.get("tube_constants","ligase_to_V5"))
		self.T_to_Y = int(self.config.get("tube_constants","T_to_Y"))
		self.Y_to_FC = int(self.config.get("tube_constants","Y_to_FC"))
		self.FC_to_syringe = int(self.config.get("tube_constants","FC_to_syringe"))

		self.NaOH_to_V4 = int(self.config.get("tube_constants","NaOH_to_V4"))
		self.guadinine_to_V4 = int(self.config.get("tube_constants","guadinine_to_V4"))

		#---------------- Reagent block chamber configuration --------------------------

		self.primer_chamber_volume = int(self.config.get("block_constants","primer_chamber_volume"))
		self.nonamer_chamber_volume = int(self.config.get("block_constants","nonamer_chamber_volume"))
		self.spare_chamber_volume = int(self.config.get("block_constants","spare_chamber_volume"))
		self.ligase_chamber_volume = int(self.config.get("block_constants","ligase_chamber_volume"))
		self.buffer_chamber_volume = int(self.config.get("block_constants","buffer_chamber_volume"))
		self.A5_chamber_volume = int(self.config.get("block_constants","A5_chamber_volume"))
		self.A6_chamber_volume = int(self.config.get("block_constants","A6_chamber_volume"))

		#---------------------- Syringe configuration ----------------------------------

		self.full_stroke = int(self.config.get("syringe_constants","full_stroke"))

		self.pull_speed = int(self.config.get("syringe_constants","pull_speed"))
		self.slow_speed = int(self.config.get("syringe_constants","slow_speed"))
		self.fast_speed = int(self.config.get("syringe_constants","fast_speed"))
		self.critical_speed = int(self.config.get("syringe_constants","critical_speed"))
		self.final_pull_speed = int(self.config.get("syringe_constants","final_pull_speed"))
		self.empty_speed = int(self.config.get("syringe_constants","empty_speed"))
		self.mixer_empty_speed = int(self.config.get("syringe_constants","mixer_empty_speed"))

		#------------------------ Biochem parameters -----------------------------------

		self.stage_temp = int(self.config.get("biochem_parameters","stage_temp"))
		self.room_temp = int(self.config.get("biochem_parameters","room_temp"))
		self.temp_tolerance = int(self.config.get("biochem_parameters","temp_tolerance"))

		self.air_gap = int(self.config.get("biochem_parameters","air_gap"))
		self.front_gap = int(self.config.get("biochem_parameters","front_gap"))
		self.middle_gap = int(self.config.get("biochem_parameters","middle_gap"))
		self.back_gap = int(self.config.get("biochem_parameters","back_gap"))

		self.time_limit = int(self.config.get("biochem_parameters","time_limit"))
		self.mixer_iter = int(self.config.get("biochem_parameters","mixer_iter"))
		self.syringe_iter = int(self.config.get("biochem_parameters","syringe_iter"))
		self.slow_push_volume = int(self.config.get("biochem_parameters","slow_push_volume"))

		#------------------ Enzymatic reaction parameters ------------------------------

		self.exo_volume = int(self.config.get("exo_parameters","exo_volume"))
		self.exo_temp = int(self.config.get("exo_parameters","exo_temp"))
		self.exo_set_temp = int(self.config.get("exo_parameters","exo_set_temp"))
		self.exo_poll_temp = int(self.config.get("exo_parameters","exo_poll_temp"))
		self.exo_time = int(self.config.get("exo_parameters","exo_time"))

		self.exo_extra = int(self.config.get("exo_parameters","exo_extra"))

		#----------------------- Stripping parameters ----------------------------------

		self.guadinine_volume = int(self.config.get("stripping_parameters","guadinine_volume"))
		self.NaOH_volume = int(self.config.get("stripping_parameters","NaOH_volume"))
		self.dH2O_volume = int(self.config.get("stripping_parameters","dH2O_volume"))

		self.guadinine_time = int(self.config.get("stripping_parameters","guadinine_time"))
		self.NaOH_time = int(self.config.get("stripping_parameters","NaOH_time"))

		self.guadinine_extra = int(self.config.get("stripping_parameters","guadinine_extra"))
		self.NaOH_extra = int(self.config.get("stripping_parameters","NaOH_extra"))

		#--------------------- Hybridization parameters --------------------------------

		self.primer_volume = int(self.config.get("hyb_parameters","primer_volume"))

		self.hyb_temp1 = int(self.config.get("hyb_parameters","hyb_temp1"))
		self.hyb_set_temp1 = int(self.config.get("hyb_parameters","hyb_set_temp1"))
		self.hyb_poll_temp1 = int(self.config.get("hyb_parameters","hyb_poll_temp1"))
		self.hyb_time1 = int(self.config.get("hyb_parameters","hyb_time1"))

		self.hyb_temp2 = int(self.config.get("hyb_parameters","hyb_temp2"))
		self.hyb_set_temp2 = int(self.config.get("hyb_parameters","hyb_set_temp2"))
		self.hyb_poll_temp2 = int(self.config.get("hyb_parameters","hyb_poll_temp2"))
		self.hyb_time2 = int(self.config.get("hyb_parameters","hyb_time2"))

		self.hyb_extra = int(self.config.get("hyb_parameters","hyb_extra"))

		#----------------------- Ligation parameters -----------------------------------

		self.buffer_volume = int(self.config.get("lig_parameters","buffer_volume"))
		self.ligase_volume = int(self.config.get("lig_parameters","ligase_volume"))
		self.nonamer_volume = int(self.config.get("lig_parameters","nonamer_volume"))
		self.reagent_volume = self.ligase_volume + self.nonamer_volume

		self.lig_step1 = int(self.config.get("lig_parameters","lig_step1"))
		self.lig_set_step1 = int(self.config.get("lig_parameters","lig_set_step1"))
		self.lig_poll_step1 = int(self.config.get("lig_parameters","lig_poll_step1"))
		self.lig_time1 = int(self.config.get("lig_parameters","lig_time1"))

		self.lig_step2 = int(self.config.get("lig_parameters","lig_step2"))
		self.lig_set_step2 = int(self.config.get("lig_parameters","lig_set_step2"))
		self.lig_poll_step2 = int(self.config.get("lig_parameters","lig_poll_step2"))
		self.lig_time2 = int(self.config.get("lig_parameters","lig_time2"))

		self.lig_step3 = int(self.config.get("lig_parameters","lig_step3"))
		self.lig_set_step3 = int(self.config.get("lig_parameters","lig_set_step3"))
		self.lig_poll_step3 = int(self.config.get("lig_parameters","lig_poll_step3"))
		self.lig_time3 = int(self.config.get("lig_parameters","lig_time3"))

		self.lig_step4 = int(self.config.get("lig_parameters","lig_step4"))
		self.lig_set_step4 = int(self.config.get("lig_parameters","lig_set_step4"))
		self.lig_poll_step4 = int(self.config.get("lig_parameters","lig_poll_step4"))
		self.lig_time4 = int(self.config.get("lig_parameters","lig_time4"))

		self.mix_time = int(self.config.get("lig_parameters","mix_time"))
		self.lig_extra = int(self.config.get("lig_parameters","lig_extra"))

		#------------------------- Cycle constants -------------------------------------

		self.port_scheme = eval(self.config.get("cycle_constants","port_scheme"))

		#----------------------- Path lenghts / volumes --------------------------------

		self.V3_to_FC_end = self.V4_to_T + self.T_to_Y + self.Y_to_FC + self.channel_volume + self.flowcell_volume + self.rotary_dead_volume

		self.FC_wash = self.V3_to_FC_end + 2 * self.flowcell_volume  # total of 3 (1+2) flowcell volumes
		self.FC_draw = self.V4_to_T + self.T_to_Y + self.Y_to_FC + self.channel_volume + self.discrete_dead_volume - self.gap_volume(self.exo_volume)  # set draw volume parameter

#-------------------------------- Gap volume calculation -------------------------------

	def gap_volume(self, reagent_volume):
		"Determines the positioning gap needed to center the reagent volume in the flowcell."

		gap_volume = int((reagent_volume - self.flowcell_volume) / 2)#RCT
		return gap_volume

#------------------------------ V to-V4 cleaning ----------------------------

	def clean_V_to_V4(self, rotary_valve):
		"Fills tube path V to V4 with Wash1 and dumps previous tube content to waste."

		self.logging.info("%s\t%i\t--> Clean V to V4 [%s]" % (self.cycle_name, self.flowcell, self.state))

		if(rotary_valve == 'V1'):
			self.mux.set_to_rotary_valve1()  #RCT switch communication to ten port rotary valve V1
			self.rotary_valve.set_valve_position(9)  #RCT set rotary valve to position 9
			self.mux.set_to_rotary_valve4()  #RCT switch communication to ten port rotary valve V4
			self.rotary_valve.set_valve_position(1)  #RCT set rotary valve to position 1
		elif(rotary_valve == 'V2'):
			self.mux.set_to_rotary_valve2()  #RCT switch communication to ten port rotary valve V1
			self.rotary_valve.set_valve_position(9)  #RCT set rotary valve to position 9
			self.mux.set_to_rotary_valve4()  #RCT switch communication to ten port rotary valve V4
			self.rotary_valve.set_valve_position(2) #RCT set rotary valve to position 2
		elif(rotary_valve == 'V3'):
			self.mux.set_to_rotary_valve3()  #RCT switch communication to ten port rotary valve V1
			self.rotary_valve.set_valve_position(9)  #RCT set rotary valve to position 9
			self.mux.set_to_rotary_valve4()  #RCT switch communication to ten port rotary valve V4
			self.rotary_valve.set_valve_position(3)  #RCT set rotary valve to position 3

		self.logging.info("%s\t%i\t--> Draw %i ul Wash 1 up to V4" % (self.cycle_name, self.flowcell, self.V_to_V4, 1))
		self.move_reagent(self.V_to_V4, self.pull_speed, 1, self.empty_speed, 3)  #RCT draw wash up to syringe pump port 1 and eject tube content to waste

#----------------------------------- Flowcell flushing ---------------------------------

	def flush_flowcell(self, V4_port):
		"Flushes flowcell 3-times with 'Wash' or dH2O."

		self.logging.info("%s\t%i\t--> Flush flowcell 3-times from port %s: [%s]" % (self.cycle_name, self.flowcell, V4_port, self.state))

		if self.flowcell == 0:
			from_port = 1  #RCT2 # set syringe pump port variable to 2

		else:
			from_port = 2  #RCT3 # set syringe pump port variable to 3

		self.mux.set_to_rotary_valve4()  # switch communication to ten port rotary valve V3
		self.rotary_valve.set_valve_position(V4_port) # switch rotary valve V3 to designated port

		self.logging.info("%s\t%i\t--> Flush flowcells 3-times (%i ul) and eject to waste" % (self.cycle_name, self.flowcell, flowcell_wash))
		self.move_reagent(self.FC_wash, self.fast_speed, from_port, self.empty_speed, 3)  #RCT flush flowcells 3-times and eject to waste

#------------------------------- Draw reagent into flowcell ----------------------------

	def draw_into_flowcell(self, draw_port, rotary_valve, rotary_port, reagent_volume):
		"Draws reagent into flowcell."
		
		self.logging.info("%s\t%i\t--> Draw reagent into flowcell %i: [%s]" % (self.cycle_name, self.flowcell, self.flowcell, self.state))

		if self.flowcell == 0:
			from_port = 1 # set syringe pump port variable to 2

		else:
			from_port = 2 # set syringe pump port variable to 3

		if (rotary_valve == 'V4'):
			FC_draw = self.V4_to_FC_end
		else:
			FC_draw = self.V_to_FC_end	

		self.draw_reagent(rotary_valve, rotary_port, reagent_volume)
		self.rotary_valve.set_valve_position(draw_port)
		self.logging.info("%s\t%i\t--> Do iterative flushes (%i ul) and eject to waste" % (self.cycle_name, self.flowcell, FC_draw))
		self.move_reagent_slow(FC_draw, self.pull_speed, from_port, self.empty_speed, 3)  #RCT do iterative flushes with last 200 ul stroke at slow syringe speed and eject to waste

#---------------------------- Reagent transfer through syringe -------------------------

	def move_reagent(self, fill_volume, from_speed, from_port, to_speed, to_port):
		"""Moves a given volume of reagent [1] into syringe at speed [2] through specified valve
		position [3], then transfers syringe content through valve position [4] into an other
		location in the fluidic system. All parameters are integers respectively."""

		if fill_volume != 0:
			self.mux.set_to_syringe_pump()  # switch communication to nine port syringe pump

			if fill_volume <= self.full_stroke:

				self.syringe_pump.set_speed(from_speed)  # draw into syringe
				self.syringe_pump.set_valve_position(from_port)
				self.syringe_pump.set_absolute_volume(fill_volume)
	
				self.syringe_pump.set_speed(to_speed)  # transfer fluid through 'to_port'
				self.syringe_pump.set_valve_position(to_port)
				self.syringe_pump.set_absolute_volume(0)

			else:
				iteration = int(fill_volume / self.full_stroke)
				remainder = int(fill_volume - (iteration * self.full_stroke))

				for i in range(0, iteration):
	
					self.syringe_pump.set_speed(from_speed)  # draw into syringe
					self.syringe_pump.set_valve_position(from_port)
					self.syringe_pump.set_absolute_volume(self.full_stroke)
	
					self.syringe_pump.set_speed(to_speed)  # transfer fluid through 'to_port'
					self.syringe_pump.set_valve_position(to_port)
					self.syringe_pump.set_absolute_volume(0)
	                
				if remainder != 0:
	 
					self.syringe_pump.set_speed(from_speed)  # draw remainder into syringe
					self.syringe_pump.set_valve_position(from_port)
					self.syringe_pump.set_absolute_volume(remainder)
	
					self.syringe_pump.set_speed(to_speed)  # transfer remainder fluid through 'to_port'
					self.syringe_pump.set_valve_position(to_port)
					self.syringe_pump.set_absolute_volume(0)

#------------------------- Slow reagent transfer through syringe -------------------------

	def move_reagent_slow(self, fill_volume, from_speed, from_port, to_speed, to_port):
		"""Moves a given volume of reagent [1] into syringe at speed [2] through specified valve
		position [3], then transfers syringe content through valve position [4] into an other
		location in the fluidic system. The last 200 ul reagent is drawn into the flowcell with 
		slower speed to avoid air bubble build up in the chambers. All parameters are integers 
		respectively."""

		if fill_volume != 0:
			self.mux.set_to_syringe_pump()  # switch communication to nine port syringe pump

			if fill_volume <= self.full_stroke:

				if fill_volume <= self.slow_push_volume:  # if flowcell-fill volume less than last slow-fill volume

					# Slow push in to aviod air bubbles

					self.syringe_pump.set_speed(self.final_pull_speed)  # draw into syringe
					self.syringe_pump.set_valve_position(from_port)
					self.syringe_pump.set_absolute_volume(fill_volume)

					self.syringe_pump.set_speed(to_speed)  # transfer fluid through 'to_port'
					self.syringe_pump.set_valve_position(to_port)
					self.syringe_pump.set_absolute_volume(0)
				else:
					first_push_volume = fill_volume - self.slow_push_volume  #  calculate first push volume

					self.syringe_pump.set_speed(from_speed)  # draw into syringe
					self.syringe_pump.set_valve_position(from_port)
					self.syringe_pump.set_absolute_volume(first_push_volume)

					self.syringe_pump.set_speed(to_speed)  # transfer fluid through 'to_port'
					self.syringe_pump.set_valve_position(to_port)
					self.syringe_pump.set_absolute_volume(0)

					# Slow push in to aviod air bubbles
	
					if self.slow_push_volume != 0:

						self.syringe_pump.set_speed(self.final_pull_speed)  # draw into syringe
						self.syringe_pump.set_valve_position(from_port)
						self.syringe_pump.set_absolute_volume(self.slow_push_volume)

						self.syringe_pump.set_speed(to_speed)  # transfer fluid through 'to_port'
						self.syringe_pump.set_valve_position(to_port)
						self.syringe_pump.set_absolute_volume(0)	
			else:
				first_push_volume = fill_volume - self.slow_push_volume  #  calculate first push volume
	
				iteration = int(first_push_volume / self.full_stroke)
				remainder = int(first_push_volume - (iteration * self.full_stroke))

				for i in range(0, iteration):
	
					self.syringe_pump.set_speed(from_speed)  # draw into syringe
					self.syringe_pump.set_valve_position(from_port)
					self.syringe_pump.set_absolute_volume(self.full_stroke)

					self.syringe_pump.set_speed(to_speed)  # transfer fluid through 'to_port'
					self.syringe_pump.set_valve_position(to_port)
					self.syringe_pump.set_absolute_volume(0)

				if remainder != 0:
	                
					self.syringe_pump.set_speed(from_speed)  # draw remainder into syringe
					self.syringe_pump.set_valve_position(from_port)
					self.syringe_pump.set_absolute_volume(remainder)

					self.syringe_pump.set_speed(to_speed)  # transfer remainder fluid through 'to_port'
					self.syringe_pump.set_valve_position(to_port)
					self.syringe_pump.set_absolute_volume(0)

					# Slow push in to aviod air bubbles
	
					if self.slow_push_volume != 0:

						self.syringe_pump.set_speed(self.final_pull_speed)  # draw into syringe
						self.syringe_pump.set_valve_position(from_port)
						self.syringe_pump.set_absolute_volume(self.slow_push_volume)

						self.syringe_pump.set_speed(to_speed)  # transfer fluid through 'to_port'
						self.syringe_pump.set_valve_position(to_port)
						self.syringe_pump.set_absolute_volume(0)

#----------------------------- Air gap drawing to valves -------------------------------

	def draw_air_to_valve(self, valve, gap_size=None):
		"""Draws a 30 ul volume of air plug in front of specified valve COM-port
		assuming that all V10 ports open to air."""

		self.logging.info("%s\t%i\t--> Draw air bubble to valve %s COM-port: [%s]" % (self.cycle_name, self.flowcell, valve, self.state))

		if gap_size is None:
			gap_size = self.air_gap  # if no argument given, use default air gap size

		if valve == 'V1':

			self.mux.set_to_rotary_valve1()  # switch communication to ten port rotary valve V1
			self.rotary_valve.set_valve_position(10)
			self.mux.set_to_rotary_valve4()  # switch communication to ten port rotary valve V4 
			self.rotary_valve.set_valve_position(1)

		elif valve == 'V2':

			self.mux.set_to_rotary_valve2()  # switch communication to ten port rotary valve V2
			self.rotary_valve.set_valve_position(10)  # switch rotary valve V2 to port 10
			self.mux.set_to_rotary_valve4()  # switch communication to ten port rotary valve V4 
			self.rotary_valve.set_valve_position(2)

		elif valve == 'V3':

			self.mux.set_to_rotary_valve3()  # switch communication to ten port rotary valve V3
			self.rotary_valve.set_valve_position(10)  # switch rotary valve V3 to port 10
			self.mux.set_to_rotary_valve4()  # switch communication to ten port rotary valve V4 
			self.rotary_valve.set_valve_position(3)

		elif valve == 'V4':

			self.mux.set_to_rotary_valve4()  # switch communication to ten port rotary valve V2
			self.rotary_valve.set_valve_position(10)  # switch rotary valve V2 to port 10

		if self.flowcell == 0:
			from_port = 1 # set syringe pump port variable to 1

		else:
			from_port = 2 # set syringe pump port variable to 3

		self.logging.info("%s\t%i\t--> Draw %i ul air gap in front of COM-port" % (self.cycle_name, self.flowcell, gap_size))
		self.move_reagent(gap_size, self.pull_speed, from_port, self.empty_speed, 3)  # draw air gap in front of COM-port

#----------------------------- Room temperature setting --------------------------------

	def set_to_RT(self):
		"Sets temperataure controller to room temperature (30 C)."

		self.logging.info("%s\t%i\t--> Set temperature controller to %i C: [%s]" % (self.cycle_name, self.flowcell, self.room_temp, self.state))

		if self.flowcell == 0:
			self.mux.set_to_temperature_control1()  # set communication to temperature controller 1
		else:
			self.mux.set_to_temperature_control2()  # set communication to temperature controller 2

		self.temperature_control.set_temperature(self.room_temp)  # set temperature controller to 30 C

		t0 = time.time()  # get current time
		tc = self.temperature_control.get_temperature()  # get current flowcell temperature

		while abs(self.room_temp - tc) > 2:

			tc = self.temperature_control.get_temperature()
			delta = time.time() - t0 # elapsed time in seconds

			sys.stdout.write("TIME\t ---\t-\t--> Elapsed time: %i s and current temperature: %0.2f C\r" % (int(delta), tc))
			sys.stdout.flush()

			if delta > self.time_limit * 60:
				break
		print '\n'

#------------------------- Steady-state temperature waiting ----------------------------

	def wait_for_SS(self, set_temp, poll_temp, tolerance=None):
		"""Waits until steady-state temperature is reached, or exits wait block if ramping
		time exceeds timeout parameter set in configuration file."""

		self.logging.info("%s\t%i\t--> Wait for steady-state - poll temperature %i C: [%s]" % (self.cycle_name, self.flowcell, poll_temp, self.state))

		if tolerance is None:  # if temperature tolerance is not defined, set default to +/- 1 C
			tolerance = 1

		t0 = time.time()  # get current time
		tc = self.temperature_control.get_temperature() # get current flowcell temperature

		if set_temp - poll_temp >= 0:  # if ramping up
			if poll_temp >= tc:
				while abs(poll_temp - tc) > tolerance:

					tc = self.temperature_control.get_temperature()
					time.sleep(1)

					delta = time.time() - t0 # elapsed time in seconds
					sys.stdout.write("TIME\t ---\t-\t--> Elapsed time: %i s and current temperature: %0.2f C\r" % (int(delta), tc))
					sys.stdout.flush()
                         
					if delta > self.time_limit * 60:
						self.logging.warn("%s\t%i\t --> Time limit %s exceeded -> [current: %0.2f, target: %0.2f] C: [%s]" % (self.cycle_name, self.flowcell, self.time_limit, tc, poll_temp, self.state))
						break
		else:  # if ramping down
			if poll_temp <= tc:
				while abs(poll_temp - tc) > tolerance:

					tc = self.temperature_control.get_temperature()
					time.sleep(1)

					delta = time.time() - t0 # elapsed time in seconds
					sys.stdout.write("TIME\t ---\t-\t--> Elapsed time: %i s and current temperature: %0.2f C\r" % (int(delta), tc))
					sys.stdout.flush()
                         
					if delta > self.time_limit * 60:
						self.logging.warn("%s\t%i\t --> Time limit %s exceeded -> [current: %0.2f, target: %0.2f] C: [%s]" % (self.cycle_name, self.flowcell, self.time_limit, tc, poll_temp, self.state))
						break		
		print '\n'
		elapsed = (time.time() - t0) / 60

		self.logging.warn("%s\t%i\t--> Time to set steady-state temperature: %0.2f minutes and current temperature: %0.2f C: [%s]\r" % (self.cycle_name, self.flowcell, elapsed, tc, self.state))

#------------------------- Incubate and count elapsed time ----------------------------

	def incubate_reagent(self, time_m):
		"""Incubates reagent for given amount of time and dynamically counts elapsed time 
		in seconds to update user about incubation state."""

		self.logging.info("%s\t%i\t--> Incubate reagent for %i min: [%s]" % (self.cycle_name, self.flowcell, time_m, self.state))

		incubation_time = time_m * 60  # incubation time in seconds

		for tc in range(0, incubation_time):

			time.sleep(1)
			sys.stdout.write('TIME\t ---\t-\t--> Elapsed time: ' + str(tc) + ' of ' + str(incubation_time) + ' seconds\r')
			sys.stdout.flush()

#-------------------------------- Draw reagent ----------------------------------

	def draw_reagent(self, rotary_valve, rotary_port, reagent_volume):
		"Moves nonamer up to V com."

		#RCTreagent = self.cycle[1:]  # nonamer key 
		#RCTvalve = self.port_scheme[self.cycle][1]  # get rotary valve for nonamers from configuration schematics
		#RCTnonamer_port = self.port_scheme[self.cycle][2]  # get nonamer port on rotary valve V1/2 from configuration schematics

		if rotary_valve == 'V1':
			self.mux.set_to_rotary_valve4()  #RCT switch communication to ten port rotary valve V4
			self.rotary_valve.set_valve_position(1)
			self.mux.set_to_rotary_valve1()  #RCT switch communication to ten port rotary valve V1
			self.rotary_valve.set_valve_position(rotary_port)

		elif rotary_valve == 'V2':
			self.mux.set_to_rotary_valve4()  #RCT switch communication to ten port rotary valve V4
			self.rotary_valve.set_valve_position(2)
			self.mux.set_to_rotary_valve2()  #RCT switch communication to ten port rotary valve V2
			self.rotary_valve.set_valve_position(rotary_port)

		elif rotary_valve == 'V3':
			self.mux.set_to_rotary_valve4()  #RCT switch communication to ten port rotary valve V4
			self.rotary_valve.set_valve_position(3)
			self.mux.set_to_rotary_valve3()  #RCT switch communication to ten port rotary valve V3
			self.rotary_valve.set_valve_position(rotary_port)

		elif rotary_valve == 'V4':
			self.mux.set_to_rotary_valve4()  #RCT switch communication to ten port rotary valve V4
			self.rotary_valve.set_valve_position(rotary_port)

		self.draw_air_to_valve(rotary_valve)
		self.move_reagent(reagent_volume, self.slow_speed, self.flowcell+1, self.empty_speed, 3)  #RCT pull reagent volume
		self.draw_air_to_valve(rotary_valve)

#----------------------------------- Ligase mixing -------------------------------------

	def ligase_mix(self, mix_time):
		"Mixes ligase with nonamer."

		self.logging.info("%s\t%i\t--> Mix reagent in mixing chamber for %i seconds: [%s]" % (self.cycle_name, self.flowcell, mix_time, self.state))

#--------------------------------------------------------------------------------------# 
# 							PRIMING FUNCTIONS 			       # 
#--------------------------------------------------------------------------------------#

#----------------------------- Prime rotary valve 1 chambers ---------------------------

	def prime_rotary_valve1(self):
		"Primes reagent block chambers in ten port rotary valve V1."

		self.logging.info("%s\t%i\t--> Prime rotary valve V1 reagent block chambers: [%s]" % (self.cycle_name, self.flowcell, self.state))

		self.mux.set_to_rotary_valve1()  # switch communication to ten port rotary valve V1
		self.rotary_valve.set_valve_position(1)  # switch rotary valve V1 to port 1
		self.logging.info("%s\t%i\t--> Prime position 1 with %i ul pre-loaded fluid" % (self.cycle_name, self.flowcell, self.nonamer_chamber_volume))
		self.move_reagent(self.prime_volume, self.fast_speed, 1, self.empty_speed, 3)

		self.mux.set_to_rotary_valve1()  # switch communication to ten port rotary valve V1
		self.rotary_valve.set_valve_position(2)  # switch rotary valve V1 to port 2
		self.logging.info("%s\t%i\t--> Prime position 2 with %i ul pre-loaded fluid" % (self.cycle_name, self.flowcell, self.nonamer_chamber_volume))
		self.move_reagent(self.prime_volume, self.fast_speed, 1, self.empty_speed, 3)

		self.mux.set_to_rotary_valve1()  # switch communication to ten port rotary valve V1
		self.rotary_valve.set_valve_position(3)  # switch rotary valve V1 to port 3
		self.logging.info("%s\t%i\t--> Prime position 3 with %i ul pre-loaded fluid" % (self.cycle_name, self.flowcell, self.nonamer_chamber_volume))
		self.move_reagent(self.prime_volume, self.fast_speed, 1, self.empty_speed, 3)

		self.mux.set_to_rotary_valve1()  # switch communication to ten port rotary valve V1
		self.rotary_valve.set_valve_position(4)  # switch rotary valve V1 to port 4
		self.logging.info("%s\t%i\t--> Prime position 4 with %i ul pre-loaded fluid" % (self.cycle_name, self.flowcell, self.nonamer_chamber_volume))
		self.move_reagent(self.prime_volume, self.fast_speed, 1, self.empty_speed, 3)

		self.mux.set_to_rotary_valve1()  # switch communication to ten port rotary valve V1
		self.rotary_valve.set_valve_position(5)  # switch rotary valve V1 to port 5
		self.logging.info("%s\t%i\t--> Prime position 5 with %i ul pre-loaded fluid" % (self.cycle_name, self.flowcell, self.nonamer_chamber_volume))
		self.move_reagent(self.prime_volume, self.fast_speed, 1, self.empty_speed, 3)

		self.mux.set_to_rotary_valve1()  # switch communication to ten port rotary valve V1
		self.rotary_valve.set_valve_position(6)  # switch rotary valve V1 to port 6
		self.logging.info("%s\t%i\t--> Prime position 6 with %i ul pre-loaded fluid" % (self.cycle_name, self.flowcell, self.nonamer_chamber_volume))
		self.move_reagent(self.prime_volume, self.fast_speed, 1, self.empty_speed, 3)

		self.mux.set_to_rotary_valve1()  # switch communication to ten port rotary valve V1
		self.rotary_valve.set_valve_position(7)  # switch rotary valve V1 to port 7
		self.logging.info("%s\t%i\t--> Prime position 7 with %i ul pre-loaded fluid" % (self.cycle_name, self.flowcell, self.nonamer_chamber_volume))
		self.move_reagent(self.prime_volume, self.fast_speed, 1, self.empty_speed, 3)

		self.mux.set_to_rotary_valve1()  # switch communication to ten port rotary valve V1
		self.rotary_valve.set_valve_position(8)  # switch rotary valve V1 to port 8
		self.logging.info("%s\t%i\t--> Prime position 8 with %i ul pre-loaded fluid" % (self.cycle_name, self.flowcell, self.nonamer_chamber_volume))
		self.move_reagent(self.prime_volume, self.fast_speed, 1, self.empty_speed, 3)

		self.mux.set_to_rotary_valve1()  # switch communication to ten port rotary valve V1
		self.rotary_valve.set_valve_position(9)  # switch rotary valve V1 to port 9
		self.logging.info("%s\t%i\t--> Prime position 9 with %i ul pre-loaded fluid" % (self.cycle_name, self.flowcell, self.nonamer_chamber_volume))
		self.move_reagent(self.prime_volume, self.fast_speed, 1, self.empty_speed, 3)

		self.mux.set_to_rotary_valve1()  # switch communication to ten port rotary valve V1
		self.rotary_valve.set_valve_position(10) # switch rotary valve V1 to port 10
		self.logging.info("%s\t%i\t--> Draw %i ul Wash 1 up to V1-COM" % (self.cycle_name, self.flowcell, 5 * self.wash1_to_V))
		self.move_reagent(5 * self.wash1_to_V, self.fast_speed, 1, self.empty_speed, 3) # draw Wash 1 up to V1-10

#----------------------------- Prime rotary valve 2 chambers ---------------------------

	def prime_rotary_valve2(self):
		"Primes reagent block chambers in ten port rotary valve V2."

		self.logging.info("%s\t%i\t--> Prime rotary valve V2 reagent block chambers: [%s]" % (self.cycle_name, self.flowcell, self.state))

		self.mux.set_to_rotary_valve2()  # switch communication to ten port rotary valve V2
		self.rotary_valve.set_valve_position(1)  # switch rotary valve V2 to port 1
		self.logging.info("%s\t%i\t--> Prime position 1 with %i ul pre-loaded fluid" % (self.cycle_name, self.flowcell, self.nonamer_chamber_volume))
		self.move_reagent(self.prime_volume, self.fast_speed, 1, self.empty_speed, 3)

		self.mux.set_to_rotary_valve2()  # switch communication to ten port rotary valve V2
		self.rotary_valve.set_valve_position(2)  # switch rotary valve V2 to port 2
		self.logging.info("%s\t%i\t--> Prime position 2 with %i ul pre-loaded fluid" % (self.cycle_name, self.flowcell, self.nonamer_chamber_volume))
		self.move_reagent(self.prime_volume, self.fast_speed, 1, self.empty_speed, 3)

		self.mux.set_to_rotary_valve2()  # switch communication to ten port rotary valve V2
		self.rotary_valve.set_valve_position(3)  # switch rotary valve V2 to port 3
		self.logging.info("%s\t%i\t--> Prime position 3 with %i ul pre-loaded fluid" % (self.cycle_name, self.flowcell, self.nonamer_chamber_volume))
		self.move_reagent(self.prime_volume, self.fast_speed, 1, self.empty_speed, 3)

		self.mux.set_to_rotary_valve2()  # switch communication to ten port rotary valve V2
		self.rotary_valve.set_valve_position(4)  # switch rotary valve V2 to port 4
		self.logging.info("%s\t%i\t--> Prime position 4 with %i ul pre-loaded fluid" % (self.cycle_name, self.flowcell, self.nonamer_chamber_volume))
		self.move_reagent(self.prime_volume, self.fast_speed, 1, self.empty_speed, 3)

		self.mux.set_to_rotary_valve2()  # switch communication to ten port rotary valve V2
		self.rotary_valve.set_valve_position(5)  # switch rotary valve V2 to port 5
		self.logging.info("%s\t%i\t--> Prime position 5 with %i ul pre-loaded fluid" % (self.cycle_name, self.flowcell, self.nonamer_chamber_volume))
		self.move_reagent(self.prime_volume, self.fast_speed, 1, self.empty_speed, 3)

		self.mux.set_to_rotary_valve2()  # switch communication to ten port rotary valve V2
		self.rotary_valve.set_valve_position(6)  # switch rotary valve V2 to port 6
		self.logging.info("%s\t%i\t--> Prime position 6 with %i ul pre-loaded fluid" % (self.cycle_name, self.flowcell, self.nonamer_chamber_volume))
		self.move_reagent(self.prime_volume, self.fast_speed, 1, self.empty_speed, 3)

		self.mux.set_to_rotary_valve2()  # switch communication to ten port rotary valve V2
		self.rotary_valve.set_valve_position(7)  # switch rotary valve V2 to port 7
		self.logging.info("%s\t%i\t--> Prime position 7 with %i ul pre-loaded fluid" % (self.cycle_name, self.flowcell, self.nonamer_chamber_volume))
		self.move_reagent(self.prime_volume, self.fast_speed, 1, self.empty_speed, 3)

		self.mux.set_to_rotary_valve2()  # switch communication to ten port rotary valve V2
		self.rotary_valve.set_valve_position(8)  # switch rotary valve V2 to port 8
		self.logging.info("%s\t%i\t--> Prime position 8 with %i ul pre-loaded fluid" % (self.cycle_name, self.flowcell, self.nonamer_chamber_volume))
		self.move_reagent(self.prime_volume, self.fast_speed, 1, self.empty_speed, 3)

		self.mux.set_to_rotary_valve2()  # switch communication to ten port rotary valve V2
		self.rotary_valve.set_valve_position(9)  # switch rotary valve V2 to port 9
		self.logging.info("%s\t%i\t--> Prime position 9 with %i ul pre-loaded fluid" % (self.cycle_name, self.flowcell, self.nonamer_chamber_volume))
		self.move_reagent(self.prime_volume, self.fast_speed, 1, self.empty_speed, 3)

		self.mux.set_to_rotary_valve2()  # switch communication to ten port rotary valve V2
		self.rotary_valve.set_valve_position(10) # switch rotary valve V2 to port 10
		self.logging.info("%s\t%i\t--> Draw %i ul Wash 1 up to V1-COM" % (self.cycle_name, self.flowcell, 5 * self.wash1_to_V))
		self.move_reagent(5 * self.wash1_to_V, self.fast_speed, 1, self.empty_speed, 3) #RCT draw Wash1 up to V2-10

#----------------------------- Prime rotary valve 3 chambers ---------------------------

	def prime_rotary_valve3(self):
		"Primes reagent block chambers in ten port rotary valve V3."

		self.logging.info("%s\t%i\t--> Prime rotary valve V3 reagent block chambers: [%s]" % (self.cycle_name, self.flowcell, self.state))

		self.mux.set_to_rotary_valve3()  # switch communication to ten port rotary valve V3
		self.rotary_valve.set_valve_position(1)  # switch rotary valve V3 to port 1
		self.logging.info("%s\t%i\t--> Prime position 1 with %i ul pre-loaded fluid" % (self.cycle_name, self.flowcell, self.nonamer_chamber_volume))
		self.move_reagent(self.prime_volume, self.fast_speed, 1, self.empty_speed, 3)

		self.mux.set_to_rotary_valve3()  # switch communication to ten port rotary valve V3
		self.rotary_valve.set_valve_position(2)  # switch rotary valve V3 to port 2
		self.logging.info("%s\t%i\t--> Prime position 2 with %i ul pre-loaded fluid" % (self.cycle_name, self.flowcell, self.nonamer_chamber_volume))
		self.move_reagent(self.prime_volume, self.fast_speed, 1, self.empty_speed, 3)

		self.mux.set_to_rotary_valve3()  # switch communication to ten port rotary valve V3
		self.rotary_valve.set_valve_position(3)  # switch rotary valve V3 to port 3
		self.logging.info("%s\t%i\t--> Prime position 3 with %i ul pre-loaded fluid" % (self.cycle_name, self.flowcell, self.nonamer_chamber_volume))
		self.move_reagent(self.prime_volume, self.fast_speed, 1, self.empty_speed, 3)

		self.mux.set_to_rotary_valve3()  # switch communication to ten port rotary valve V3
		self.rotary_valve.set_valve_position(4)  # switch rotary valve V3 to port 4
		self.logging.info("%s\t%i\t--> Prime position 4 with %i ul pre-loaded fluid" % (self.cycle_name, self.flowcell, self.nonamer_chamber_volume))
		self.move_reagent(self.prime_volume, self.fast_speed, 1, self.empty_speed, 3)

		self.mux.set_to_rotary_valve3()  # switch communication to ten port rotary valve V3
		self.rotary_valve.set_valve_position(5)  # switch rotary valve V3 to port 5
		self.logging.info("%s\t%i\t--> Prime position 5 with %i ul pre-loaded fluid" % (self.cycle_name, self.flowcell, self.nonamer_chamber_volume))
		self.move_reagent(self.prime_volume, self.fast_speed, 1, self.empty_speed, 3)

		self.mux.set_to_rotary_valve3()  # switch communication to ten port rotary valve V3
		self.rotary_valve.set_valve_position(6)  # switch rotary valve V3 to port 6
		self.logging.info("%s\t%i\t--> Prime position 6 with %i ul pre-loaded fluid" % (self.cycle_name, self.flowcell, self.nonamer_chamber_volume))
		self.move_reagent(self.prime_volume, self.fast_speed, 1, self.empty_speed, 3)

		self.mux.set_to_rotary_valve3()  # switch communication to ten port rotary valve V3
		self.rotary_valve.set_valve_position(7)  # switch rotary valve V3 to port 7
		self.logging.info("%s\t%i\t--> Prime position 7 with %i ul pre-loaded fluid" % (self.cycle_name, self.flowcell, self.nonamer_chamber_volume))
		self.move_reagent(self.prime_volume, self.fast_speed, 1, self.empty_speed, 3)

		self.mux.set_to_rotary_valve3()  # switch communication to ten port rotary valve V3
		self.rotary_valve.set_valve_position(8)  # switch rotary valve V3 to port 8
		self.logging.info("%s\t%i\t--> Prime position 8 with %i ul pre-loaded fluid" % (self.cycle_name, self.flowcell, self.nonamer_chamber_volume))
		self.move_reagent(self.prime_volume, self.fast_speed, 1, self.empty_speed, 3)

		self.mux.set_to_rotary_valve3()  # switch communication to ten port rotary valve V3
		self.rotary_valve.set_valve_position(9)  # switch rotary valve V3 to port 9
		self.logging.info("%s\t%i\t--> Prime position 9 with %i ul pre-loaded fluid" % (self.cycle_name, self.flowcell, self.nonamer_chamber_volume))
		self.move_reagent(self.prime_volume, self.fast_speed, 1, self.empty_speed, 3)

		self.mux.set_to_rotary_valve3()  # switch communication to ten port rotary valve V3
		self.rotary_valve.set_valve_position(10) # switch rotary valve V3 to port 10
		self.logging.info("%s\t%i\t--> Draw %i ul Wash 1 up to V3-COM" % (self.cycle_name, self.flowcell, 5 * self.wash1_to_V))
		self.move_reagent(5 * self.wash1_to_V, self.fast_speed, 1, self.empty_speed, 3) #RCT draw Wash1 up to V3-10

#----------------------------- Prime rotary valve 4 chambers ---------------------------

	def prime_rotary_valve4(self):
		"Primes reagent block chambers in ten port rotary valve V3."

		self.logging.info("%s\t%i\t--> Prime rotary valve V3 reagent block chambers: [%s]" % (self.cycle_name, self.flowcell, self.state))

		self.mux.set_to_rotary_valve1()  # switch communication to ten port rotary valve V1
		self.rotary_valve.set_valve_position(9)  # switch rotary valve V1 to port 9
		self.mux.set_to_rotary_valve4()  # switch communication to ten port rotary valve V4
		self.rotary_valve.set_valve_position(1)  # switch rotary valve V3 to port 1
		self.logging.info("%s\t%i\t--> Prime position 1 with %i ul pre-loaded fluid" % (self.cycle_name, self.flowcell, self.nonamer_chamber_volume))
		self.move_reagent(self.prime_volume, self.fast_speed, 1, self.empty_speed, 3)

		self.mux.set_to_rotary_valve2()  # switch communication to ten port rotary valve V2
		self.rotary_valve.set_valve_position(9)  # switch rotary valve V2 to port 9
		self.mux.set_to_rotary_valve4()  # switch communication to ten port rotary valve V4
		self.rotary_valve.set_valve_position(2)  # switch rotary valve V4 to port 2
		self.logging.info("%s\t%i\t--> Prime position 2 with %i ul pre-loaded fluid" % (self.cycle_name, self.flowcell, self.nonamer_chamber_volume))
		self.move_reagent(self.prime_volume, self.fast_speed, 1, self.empty_speed, 3)

		self.mux.set_to_rotary_valve3()  # switch communication to ten port rotary valve V3
		self.rotary_valve.set_valve_position(9)  # switch rotary valve V3 to port 9
		self.mux.set_to_rotary_valve4()  # switch communication to ten port rotary valve V4
		self.rotary_valve.set_valve_position(3)  # switch rotary valve V4 to port 3
		self.logging.info("%s\t%i\t--> Prime position 3 with %i ul pre-loaded fluid" % (self.cycle_name, self.flowcell, self.nonamer_chamber_volume))
		self.move_reagent(self.prime_volume, self.fast_speed, 1, self.empty_speed, 3)

		self.mux.set_to_rotary_valve4()  # switch communication to ten port rotary valve V4
		self.rotary_valve.set_valve_position(4) # switch rotary valve V4 to port 4
		self.logging.info("%s\t%i\t--> Draw %i ul guadinine up to V4-COM" % (self.cycle_name, self.flowcell, 5 * self.guadinine_to_V4))
		self.move_reagent(5 * self.guadinine_to_V4, self.fast_speed, 1, self.empty_speed, 3) #RCT draw guadinine up to V4-4

		self.mux.set_to_rotary_valve4()  # switch communication to ten port rotary valve V4
		self.rotary_valve.set_valve_position(6) # switch rotary valve V4 to port 6
		self.logging.info("%s\t%i\t--> Draw %i ul NaOH up to V4-COM" % (self.cycle_name, self.flowcell, 5 * self.NaOH_to_V4))
		self.move_reagent(5 * self.NaOH_to_V4, self.fast_speed, 1, self.empty_speed, 3) #RCT draw NaOH up to V4-9

		self.mux.set_to_rotary_valve4()  # switch communication to ten port rotary valve V4
		self.rotary_valve.set_valve_position(7) # switch rotary valve V4 to port 7
		self.logging.info("%s\t%i\t--> Draw %i ul dH2O up to V4-COM" % (self.cycle_name, self.flowcell, 5 * self.dH2O_to_V4))
		self.move_reagent(5 * self.dH2O_to_V4, self.fast_speed, 1, self.empty_speed, 3) #RCT draw dH2O up to V4-7

		self.mux.set_to_rotary_valve4()  # switch communication to ten port rotary valve V4
		self.rotary_valve.set_valve_position(9) # switch rotary valve V4 to port 9
		self.logging.info("%s\t%i\t--> Draw %i ul Wash up to V4-COM" % (self.cycle_name, self.flowcell, 5 * self.wash1_to_V4))
		self.move_reagent(5 * self.wash1_to_V4, self.fast_speed, 1, self.empty_speed, 3) #RCT draw "Wash 1" up to V4-9

#-------------------------- Prime ligase chamber ------------------------

	def prime_ligase(self):
		"Primes ligase and ligation buffer chambers in reagent cooling block."

		self.logging.info("%s\t%i\t--> Prime ligase chamber: [%s]" % (self.cycle_name, self.flowcell, self.state))

		self.mux.discrete_valve5_open()  #RCT switch 2-way discrete valve V5 to NO (ligase)
		self.logging.info("%s\t%i\t--> Prime ligase chamber with %i ul pre-loaded fluid" % (self.cycle_name, self.flowcell, self.ligase_chamber_volume))
		self.move_reagent(self.ligase_prime_volume, self.fast_speed, 1, self.empty_speed, 3) #RCT prime ligase chamber

		self.mux.discrete_valve5_close()  #RCT switch 2-way discrete valve V5 to NC (ligase)

#-------------------------------- Reagent block priming --------------------------------

	def prime_reagent_block(self):
		"Primes all reagent block chambers with 'Wash 1'."

		self.logging.info("%s\t%i\t--> Prime reagent block chambers: [%s]" % (self.cycle_name, self.flowcell, self.state))

		self.syringe_pump_init()  # initialize syringe pump
		self.prime_rotary_valve1()  # prime reagent block chambers in ten port rotary valve V1
		self.prime_rotary_valve2()  # prime reagent block chambers in ten port rotary valve V2
		self.prime_rotary_valve3()  # prime reagent block chambers in ten port rotary valve V3
		self.prime_rotary_valve4()  # prime reagent block chambers in ten port rotary valve V4
		self.prime_ligase()  # prime ligase/ligase buffer chambers in nine port syringe

#---------------------------------- Priming flowcells ----------------------------------

	def prime_flowcells(self):
		"Primes both flowcells with 'Wash 1' as initialization step."

		self.logging.info("%s\t%i\t--> Prime both flowcells: [%s]" % (self.cycle_name, self.flowcell, self.state))
		flush_volume = self.V4_to_FC_end + self.wash1_to_V4
		self.mux.set_to_rotary_valve4()  #RCT switch communication to ten port rotary valve V4
		self.rotary_valve.set_valve_position(9)

		self.logging.info("%s\t%i\t--> Draw %i ul 'Wash' via V4 through flowcell 1 to syringe port 1" % (self.cycle_name, self.flowcell, self.V4_to_FC1_end))
		self.move_reagent(flush_volume, self.fast_speed, 1, self.empty_speed, 3)  #RCT draw "Wash 1" via V3-V4 through flowcell 1 to syringe port 2

		if self.cycle[2] == 2:  # if two flowcells installed
			self.logging.info("%s\t%i\t--> Draw %i ul 'Wash' via V4 through flowcell 2 to syringe port 2" % (self.cycle_name, self.flowcell, self.V4_to_FC2_end))
			self.move_reagent(flush_volume, self.fast_speed, 2, self.empty_speed, 3)  #RCT draw "Wash" via V4 through flowcell 2 to syringe port 2

#------------------------------ Fluidic sub-system priming -----------------------------

	def prime_fluidics_system(self):
		"""Primes all fluid lines, flowcells and reagent block chambers with 'Wash 1'.
		Assume that all reagent block chambers and bottles are filled with 'Wash 1'."""

		self.logging.info("%s\t%i\t--> Prime fluidics system: [%s]" % (self.cycle_name, self.flowcell, self.state))
		self.prime_flowcells()  #RCT prime both flowcells with "Wash"
		self.prime_reagent_block()  #RCT prime reagent block chambers with "Wash" 
		self.prime_flowcells()  #RCT prime both flowcells with "Wash"

#--------------------------------------------------------------------------------------# 
# 				INITIALIZATION FUNCTIONS 			       # 
#--------------------------------------------------------------------------------------#

#-------------------- Temperature control 1-2 initialization ---------------------------

	def temperature_control_init(self):
		"""Set temperature controller 1-2 to OFF state to avoid any temperature
		control operation left-over from a possible previous process."""

		self.logging.info("%s\t%i\t--> Initialize temperature controller 1-2: [%s]" % (self.cycle_name, self.flowcell, self.state))

		self.mux.set_to_temperature_control1()  # Switch communication to temperature controller 1.
		self.temperature_control.set_temperature(self.room_temp)  # set flowcell temperature to room temperature
		self.wait_for_SS(self.room_temp, self.room_temp, self.temp_tolerance)  # wait until steady-state temperature is reached

		self.mux.set_to_temperature_control2()  # Switch communication to temperature controller 2.
		self.temperature_control.set_temperature(self.room_temp)  # set flowcell temperature to room temperature
		self.wait_for_SS(self.room_temp, self.room_temp, self.temp_tolerance)  # wait until steady-state temperature is reached

#-------------------------- Reagent block initialization -------------------------------

	def reagent_block_init(self):
		"Initialize reagent block temperature and prime wells."

		self.logging.info("%s\t%i\t--> Initialize reagent block cooler: [%s]" % (self.cycle_name, self.flowcell, self.state))
		self.prime_reagent_block() # pull all well contents up to valve com port
		self.mux.set_to_reagent_block_cooler()  # set communication to reagent block cooler
		self.temperature_control.set_temperature(self.stage_temp) # set reagent block temperature

#-------------------------- Syringe pump initialization -------------------------------

	def syringe_pump_init(self):
		"Initializes syringe pump by moving it to zero position and setting speed to 20."

		self.logging.info("%s\t%i\t--> Initialize syringe pump: [%s]" % (self.cycle_name, self.flowcell, self.state))

		self.mux.set_to_syringe_pump()  # set communication to syringe pump
		self.syringe_pump.initialize_syringe()  # initialize syringe pump

#--------------------------- Biochemistry initialization -------------------------------

	def init(self):
		"Initialize biochemistry sub-system."

		self.logging.info("%s\t%i\t--> Initialize biochemistry sub-system: [%s]" % (self.cycle_name, self.flowcell, self.state))

		self.temperature_control_init()  # initialize temperature controller 1/2
		self.syringe_pump_init()   # initialize syringe pump
		self.reagent_block_init()  # set reagent block to constant temperature, 4 Celsius degrees

#--------------------------------------------------------------------------------------# 
# 				BIOCHEMISTRY FUNCTIONS 				       # 
#--------------------------------------------------------------------------------------#

#---------------------------------- Strip_chem sub. ------------------------------------

	def strip_chem(self):
		"""Performs chemical stripping protocol for polony sequencing. Does the following:

		- flush flowcell with dH2O
		- flush flowcell with guanidine HCl and incubate for 1' at RT
		- flush flowcell with dH2O
		- flush flowcell with NaOH and incubate for 1' at RT
		- flush flowcell with dH2O
		- flush flowcell with 'Wash 1'"""

		#commands.getstatusoutput('mplayer -ao alsa speech/strip_chem.wav')

		t0 = time.time()  # get current time
		self.state = 'strip_chem' # update function state of biochemistry object

		self.logging.info("%s\t%i\t--> In %s subroutine" % (self.cycle_name, self.flowcell, self.state))

		if self.flowcell == 0:
			from_port = 1 #RCT set syringe pump port variable to 1

		else:
			from_port = 2 #RCT set syringe pump port variable to 2

		total_volume1 = self.FC_draw - self.gap_volume(self.HCl_volume)
		total_volume2 = self.FC_draw - self.gap_volume(self.NaOH_volume)

		self.mux.set_to_rotary_valve4()  #RCT switch communication to ten port rotary valve V4
		self.rotary_valve.set_valve_position(7)  #RCT switch rotary valve V4 to port 7

		self.logging.info("%s\t%i\t--> Draw %i ul dH2O into system" % (self.cycle_name, self.flowcell, self.dH2O_volume))
		self.move_reagent(self.dH2O_volume, self.pull_speed, from_port, self.empty_speed, 3) #RCT draw dH2O into system
		self.logging.info("%s\t%i\t--> Draw %i ul guadinine into system" % (self.cycle_name, self.flowcell, self.guadinine_volume))
		self.draw_into_flowcell(7, 'V4', 4, self.guadinine_volume + self.guadinine_extra)  #RCT push guadinine into flowcell with dH2O
		self.incubate_reagent(self.guadinine_time)  # incubate reagent for 1 min


		self.logging.info("%s\t%i\t--> Draw %i ul NaOH into system" % (self.cycle_name, self.flowcell, self.NaOH_volume))
		self.draw_into_flowcell(7, 'V4', 6, self.NaOH_volume + self.NaOH_extra)  #RCT push NaOH into flowcell with dH2O
		self.incubate_reagent(self.NaOH_time)  # incubate reagent for 1 min

		self.flush_flowcell(7)  # flush entire flowcell 3-times w/ dH2O

		delta = (time.time() - t0) / 60	# calculate elapsed time for stripping

		self.logging.warn("%s\t%i\t--> Finished checmical strip - duration: %0.2f minutes\n" % (self.cycle_name, self.flowcell, delta))

#-------------------------------------- Hyb sub. ---------------------------------------

	def hyb(self):
		"""Runs primer hybridization protocol for polony sequencing. Does the following:

		- incubate primer at 'hyb_temp1' for 'hyb_time1' minutes
		- incubate primer at 'hyb_temp2' for 'hyb_time2' minutes
		- flush flowcell with 'Wash 1'

		Reagent requirements:

		- V3-i : 650 ul hyb mix (650 ul 6x SSPE w/ 0.01 TX100, 6.5 ul each 1mM primer)
		- V3-2 : 650 ul 'Wash 1'"""

		#commands.getstatusoutput('mplayer -ao alsa speech/hyb.wav')

		t0 = time.time()  # get current time
		self.state = 'hyb' # update function state of biochemistry object

		self.logging.info("%s\t%i\t--> In %s subroutine" % (self.cycle_name, self.flowcell, self.state))

		if self.flowcell == 0:
			from_port = 1 #RCT set syringe pump port variable to 2

		else:
			from_port = 2 #RCT set syringe pump port variable to 3

		primer_valve = self.port_scheme[self.cycle][0]  # get anchor primer rotary valve from configuration schematics
		primer_port = self.port_scheme[self.cycle][1]  # get anchor primer port on rotary valve from configuration schematics

		if self.flowcell == 0:
			self.mux.set_to_temperature_control1()  # set to temperature controller 1
		else:
			self.mux.set_to_temperature_control2()  # set to temperature controller 2

		self.temperature_control.set_temperature(self.hyb_set_temp1)  # set flowcell temperature to 52 C
		self.wait_for_SS(self.hyb_set_temp1, self.hyb_poll_temp1, self.temp_tolerance)  # wait until steady-state temperature is reached
		self.logging.info("%s\t%i\t--> Draw %i ul anchor primer (Ai) into system from rotary valve" % (self.cycle_name, self.flowcell, self.primer_volume))
		self.draw_into_flowcell(9, primer_valve, primer_port, self.primer_volume + self.primer_extra)  #RCT push anchor primer into flowcell with Wash
		self.incubate_reagent(self.hyb_time1)  # incubate reagent for 2 min

		if self.flowcell == 0:
			self.mux.set_to_temperature_control1()  # set to temperature controller 1
		else:
			self.mux.set_to_temperature_control2()  # set to temperature controller 2

		self.temperature_control.set_temperature(self.hyb_set_temp2)  # set flowcell temperature to 42 C
		self.wait_for_SS(self.hyb_set_temp2, self.hyb_poll_temp2, self.temp_tolerance)  # wait until steady-state temperature is reached
		self.incubate_reagent(self.hyb_time2)  # incubate reagent for 2 min

		if self.flowcell == 0:
			self.mux.set_to_temperature_control1()  # set to temperature controller 1
		else:
			self.mux.set_to_temperature_control2()  # set to temperature controller 2

		self.temperature_control.set_control_off()  # turn external temperature controller OFF

		self.flush_flowcell(9)  # flush entire flowcell 3-times w/ Wash
		self.set_to_RT()  #RCT set flowcell temperature to room temperature

		delta = (time.time() - t0) / 60	# calculate elapsed time for primer hybridization

		self.logging.warn("%s\t%i\t--> Finished primer hybridization - duration: %0.2f minutes\n" % (self.cycle_name, self.flowcell, delta))

#-------------------------------- Lig_stepup_peg sub. ----------------------------------

	def lig_stepup_peg(self):
		"""Runs stepup peg ligation reaction protocol for polony sequencing. Does the following:

		- prime flowcell with Quick ligase buffer
		- incubate quick ligation mix at the following steps:

			5' at 18C
			5' at 25C
			5' at 30C
			5' at 37C

		- flush flowcell with 'Wash 1'

		Reagent requirements:

		- valve-nonamer_port : 625 ul Quick ligation mix (165ul 2x Qlig buff, 24ul 100uM nonamer mix, 6ul Qlig, 135ul dH2O)
		- V4-7 : 625 ul 1x Quick ligase buffer
		- V3-8 : 625 ul 'Wash 1'"""

		#commands.getstatusoutput('mplayer -ao alsa speech/lig_stepup_peg.wav')

		t0 = time.time()  # get current time
		self.state = 'lig_stepup_peg' # update function state of biochemistry object

		self.logging.info("%s\t%i\t--> In %s subroutine" % (self.cycle_name, self.flowcell, self.state))

		if self.flowcell == 0:
			from_port = 1 #RCT set syringe pump port variable to 2
 
		else:
			from_port = 2 #RCT set syringe pump port variable to 3

		nonamer_valve = self.port_scheme[self.cycle][2]  # get nonamer rotary valve from configuration schematics
		nonamer_port = self.port_scheme[self.cycle][3]  # get nonamer port on rotary valve from configuration schematics

	def draw_into_flowcell(self, draw_port, rotary_valve, rotary_port, reagent_volume):
	def draw_reagent(self, rotary_valve, rotary_port, reagent_volume):

		self.draw_reagent(nonamer_valve, 8, self.buffer_volume)  #RCT pull up ligation buffer
		self.draw_into_flowcell(9, nonamer_valve, nonamer_port, self.nonamer_volume + self.nonamer_extra)  #RCT push anchor primer into flowcell with
		b_volume = self.V4_to_syringe + self.i_volumes['V4']['LIGATION BUFFER']
		self.logging.info("%s\t%i\t--> Draw ligase buffer up to syringe port 7 with %i ul" % (self.cycle_name, self.flowcell, b_volume))
		self.move_reagent(b_volume, self.slow_speed, 7, self.empty_speed, 4) # draw ligase buffer up to syringe port 7

		self.logging.info("%s\t%i\t--> Draw %i ul ligase buffer into system (to mixer)" % (self.cycle_name, self.flowcell, self.buffer_volume))
		self.move_reagent(self.buffer_volume, self.slow_speed, 7, self.pull_speed, 8) # draw ligase buffer into system (to mixer)

		self.logging.info("%s\t%i\t--> Push ligase buffer into mixing chamber with %i ul air" % (self.cycle_name, self.flowcell, self.syringe_8_to_mixer * 2))
		self.move_reagent(self.syringe_8_to_mixer * 2, self.slow_speed, 1, self.slow_speed, 8) # draw ligase buffer into mixing chamber with air

		self.logging.info("%s\t%i\t--> Draw %i ul ligase buffer into system" % (self.cycle_name, self.flowcell, self.buffer_volume))
		self.move_reagent(self.buffer_volume, self.critical_speed, from_port, self.empty_speed, 4) # draw ligase buffer into system
		self.draw_air_to_mixer(self.middle_gap)  # draw air to mixing chamber's input/output needle

		self.logging.info("%s\t%i\t--> Push %i ul ligase buffer back to reagent chamber" % (self.cycle_name, self.flowcell, b_volume))
		self.move_reagent(b_volume, self.slow_speed, 1, self.slow_speed, 7)  # push ligase buffer back to reagent chamber
		
		self.nonamer_prep()  # mix nonamer with ligase
		self.mux.discrete_valve5_close()  # set dicrete valve 5 explicitely to close!

		self.logging.info("%s\t%i\t--> Draw %i ul ligase-nonamer mix into system" % (self.cycle_name, self.flowcell, self.reagent_volume))
		self.move_reagent(self.reagent_volume, self.critical_speed, from_port, self.empty_speed, 4) # draw ligase-nonamer mix into system
		self.draw_air_to_mixer(self.back_gap)  # draw air to mixing chamber's input/output needle

		self.logging.info("%s\t%i\t--> Draw %i ul ligase-nonamer mix just passed discrete valve V5" % (self.cycle_name, self.flowcell, self.mixer_to_V5 + self.back_gap))
		self.move_reagent(self.mixer_to_V5 + self.back_gap, self.pull_speed, from_port, self.empty_speed, 4) # draw ligase-nonamer mix just passed V5

		if self.flowcell == 0:
			self.mux.set_to_temperature_control1()  # set to temperature controller 1
		else:
			self.mux.set_to_temperature_control2()  # set to temperature controller 2

		self.temperature_control.set_temperature(self.lig_set_step1)  # set flowcell temperature to 18 C
		self.wait_for_SS(self.lig_set_step1, self.lig_poll_step1, self.temp_tolerance)  # wait until steady-state temperature is reached
		self.draw_into_flowcell(self.FC_draw + self.lig_extra, 2)  # draw reagent into flowcell with "Wash 1"
		self.incubate_reagent(self.lig_time1)  # incubate reagent for 5 min

		if self.flowcell == 0:
			self.mux.set_to_temperature_control1()  # set to temperature controller 1
		else:
			self.mux.set_to_temperature_control2()  # set to temperature controller 2

		self.temperature_control.set_temperature(self.lig_set_step2)  # set flowcell temperature to 25 C
		self.wait_for_SS(self.lig_set_step2, self.lig_poll_step2, self.temp_tolerance)  # wait until steady-state temperature is reached
		self.incubate_reagent(self.lig_time2)  # incubate reagent for 5 min

		if self.flowcell == 0:
			self.mux.set_to_temperature_control1()  # set to temperature controller 1
		else:
			self.mux.set_to_temperature_control2()  # set to temperature controller 2

		self.temperature_control.set_temperature(self.lig_set_step3)  # set flowcell temperature to 30 C
		self.wait_for_SS(self.lig_set_step3, self.lig_poll_step3, self.temp_tolerance)  # wait until steady-state temperature is reached
		self.incubate_reagent(self.lig_time3)  # incubate reagent for 5 min

		if self.flowcell == 0:
			self.mux.set_to_temperature_control1()  # set to temperature controller 1
		else:
			self.mux.set_to_temperature_control2()  # set to temperature controller 2

		self.temperature_control.set_temperature(self.lig_set_step4)  # set flowcell temperature to 37 C
		self.wait_for_SS(self.lig_set_step4, self.lig_poll_step4, self.temp_tolerance)  # wait until steady-state temperature is reached
		self.incubate_reagent(self.lig_time4)  # incubate reagent for 5 min

		if self.flowcell == 0:
			self.mux.set_to_temperature_control1()  # set to temperature controller 1
		else:
			self.mux.set_to_temperature_control2()  # set to temperature controller 2

		self.temperature_control.set_control_off()  # turn external temperature controller OFF
		self.clean_flowcell_and_syringe()  # flush flowcell with "Wash 1" and clean syringe pump with dH2O completely
		#self.set_to_RT()  # set flowcell temperature to room temperature

		delta = (time.time() - t0) / 60	# calculate elapsed time for stepup peg ligation

		self.logging.warn("%s\t%i\t--> Finished step-up peg ligation - duration: %0.2f minutes\n" % (self.cycle_name, self.flowcell, delta))

#--------------------------------------------------------------------------------------# 
# 				SEQUENCING ALGORTIHMS 				       # 
#--------------------------------------------------------------------------------------#

#------------------------------------- Run sub. ----------------------------------------

	def run(self):
		"""Runs polony sequencing cycle(s) based on cycle-name and flowcell-number list 
		already contained in biochemistry object."""

		time.sleep(1)
		self.state = 'running' 		# update function state of biochemistry object

		#----------------------- Flowcell preparation ----------------------------------

		if self.cycle[0:2] == 'WL' and self.flowcell == 0:	# if white light image cycle on flowcell 0
			self.init()					# do only once at beginning
			#self.exo_start()
			self.logging.info("%s\t%i\t--> Device initialization and Exonuclease I digestion is done: [%s]\n" % (self.cycle_name, self.flowcell, self.state))

		elif self.cycle[0:2] == 'WL' and self.flowcell == 1:	# if white light image cycle on flowcell 1
			#self.exo_start()
			self.logging.info("%s\t%i\t--> Exonuclease I digestion is done: [%s]\n" % (self.cycle_name, self.flowcell, self.state))

		else:
			self.cycle_ligation()  # perform query cycle on selected flowcell

#--------------------------------- Cycle_ligation sub. ---------------------------------

	def cycle_ligation(self):
		"""Performs a cycle of polony sequencing biochemistry consisting of:

		- chemical stripping
		- primer hybridization
		- query nonamer ligation (stepup temperature, peg)

		Reagent requirements:

		- see 'cycle_list' valve-port map in configuration file"""

		t0 = time.time()  # get current time
		self.state = 'cycle_ligation' # update function state of biochemistry object

		self.logging.info("%s\t%i\t--> In %s subroutine" % (self.cycle_name, self.flowcell, self.state))
		self.syringe_pump_init()  # initialize syringe pump

		self.strip_chem()  # perform polony sequencing biochemistry
		self.hyb()
		self.lig_stepup_peg()

		delta = (time.time() - t0) / 60  # calculate elapsed time for polony cycle

		self.logging.warn("%s\t%i\t--> Finished cycle ligation - duration: %0.2f minutes\n" % (self.cycle_name, self.flowcell, delta))

