#!/usr/local/bin/python

"""
-------------------------------------------------------------------------------- 
 Author: Mirko Palla.
 Date: May 8, 2008.

 For: G.007 polony sequencer design [fluidics software] at the Church Lab - 
 Genetics Department, Harvard Medical School.

 Purpose: given function command, this utility program performs any fluidics 
 method contained in biochemistry module.

 This software may be used, modified, and distributed freely, but this
 header may not be modified and must appear at the top of this file.
------------------------------------------------------------------------------- 
"""

import sys
import time

#----------------------------- Input argument handling ---------------------------------

if len(sys.argv) == 1:
	print """\n
     ----------------------------------------------------------------------   
     -                                                                    -      
     -            WELCOME TO THE BIOCHEMISTRY UTILITY PROGRAM             -
     -                                                                    -
     -        Usage: python biochem_utils.py flowcell-number method       -
     -                                                                    -
     ----------------------------------------------------------------------

     |  Methods defined here:
     |  
     |  clean_V1_to_syringe(self)
     |      Fills tube path V1 to syringe port 5 with dH2O and dumps previous tube content to waste.
     |  
     |  clean_V2_to_syringe(self)
     |      Fills tube path V2 to syringe port 6 with dH2O and dumps previous tube content to waste.
     |  
     |  clean_flowcell_and_syringe(self)
     |      Cleans flowcell-to-syringe path and syringe pump completely with 'Wash 1' first then with dH2O, 
     |      making sure that there is no left over reagent leading to or in the syringe pump after a biochemistry step.
     |      This function also flushes the flowcell, thus incorporates the 'flowcell_flush' procedure inherently.
     |  
     |  cycle_ligation(self)
     |      Performs a cycle of polony sequencing biochemistry consisting of:
     |      
     |      - chemical stripping
     |      - primer hybridization
     |      - query nonamer ligation (stepup temperature, peg)
     |      
     |      Reagent requirements:
     |      
     |      - see 'cycle_list' valve-port map in configuration file
     |  
     |  draw_air_to_mixer(self, gap_size)
     |      Draws a specific volume of air plug to mixing chamber's input/output needle
     |  
     |  draw_air_to_syringe(self)
     |      Draws a specific volume of air plug to syringe's COM-port.
     |  
     |  draw_air_to_valve(self, valve)
     |      Draws a 60 ul volume of air plug in front of specified valve COM-port
     |      assuming that the V1-10/V2-10 & V3-8 ports open to air.
     |  
     |  draw_into_flowcell(self, draw_volume, port)
     |      Draws reagent into flowcell.
     |  
     |  exo_start(self)
     |      Digests unprotected bead-bound ePCR primers with Exonuclease I using rotary
     |      valve 2 to prepare polony sequencing. Does the following:
     |      
     |      - incubate reaction mix at 'exo_set_temp' for 'exo_time' minutes
     |      - flush flowcell with 'Wash 1'
     |      
     |      Reagent requirements:
     |      
     |      - V2-6 : 625 ul reaction mix
     |      - V3-2 : 650 ul 'Wash 1'
     |  
     |  fill_with_air_to_valve(self, valve)
     |      Fills tube with air to specified valve COM-port and sets discrete valve V7 
     |      open to dH2O as default state.
     |  
     |  flush_flowcell(self, port)
     |      Flushes flowcell 3-times with 'Wash 1' or dH2O.
     |  
     |  get_config_parameters(self)
     |      Retieves all biochemistry and device related configuration parameters from the confi-
     |      guration file using the ConfigParser facility. It assigns each parameter to a field of 
     |      the biochemistry object, thus it can access it any time during a run.
     |  
     |  get_excel_volumes(self)
     |      Extracts path length and tube cross-sectional area information from standard Excel file
     |      containing all internal and external volume calculations in the G.007 fluidics sub-system.
     |      It automatically calculates total path volumes in both cases, creating a dictionary object
     |      holding volume data specified by the following format:
     |      
     |              volumes[point_B][point_A] = 'total path volume from point A to point B in the system'
     |      
     |      This function creates two dictionary objects as fields of the 'Biochem' object: one for
     |      volume calculations internal, while the other for volume calculations external to manifold
     |      respectively.
     |      
     |      If changes occur in either path length or cross-sectional area data, the numbers must be
     |      updated accordingly, but the file format and data tabulation cannot be changed.
     |  
     |  hyb(self)
     |      Runs primer hybridization protocol for polony sequencing. Does the following:
     |      
     |      - incubate primer at 'hyb_temp1' for 'hyb_time1' minutes
     |      - incubate primer at 'hyb_temp2' for 'hyb_time2' minutes
     |      - flush flowcell with 'Wash 1'
     |      
     |      Reagent requirements:
     |      
     |      - V3-i : 650 ul hyb mix (650 ul 6x SSPE w/ 0.01 TX100, 6.5 ul each 1mM primer)
     |      - V3-2 : 650 ul 'Wash 1'
     |  
     |  incubate_reagent(self, time_m)
     |      Incubates reagent for given amount of time and dynamically counts elapsed time 
     |      in seconds to update user about incubation state.
     |  
     |  init(self)
     |      Initialize biochemistry sub-system.
     |  
     |  lig_stepup_peg(self, valve, nonamer_port)
     |      Runs stepup peg ligation reaction protocol for polony sequencing. Does the following:
     |      
     |      - prime flowcell with Quick ligase buffer
     |      - incubate quick ligation mix at the following steps:
     |      
     |              5' at 18C
     |              5' at 25C
     |              5' at 30C
     |              5' at 37C
     |      
     |      - flush flowcell with 'Wash 1'
     |      
     |      Reagent requirements:
     |      
     |      - valve-nonamer_port: 625 ul Quick ligation mix (165ul 2x Qlig buff, 24ul 100uM nonamer mix, 6ul Qlig, 135ul dH2O)
     |      - V4-7 : 625 ul 1x Quick ligase buffer
     |      - V3-8 : 625 ul 'Wash 1'
     |  
     |  ligase_mix(self, mix_time)
     |      Mixes ligase with nonamer in mixing chamber.
     |  
     |  mixer_init(self)
     |      Prime mixing chamber with dH2O as initialization step in a multi-step iterative 
     |      volume filling manner. With increasing fill volume in every iteration, the side of 
     |      the mixing chamber is cleaned from residue. Assumes, that rotary valve V2 to syringe 
     |      pump port 6 path is filled with dH2O.
     |  
     |  move_reagent(self, fill_volume, from_speed, from_port, to_speed, to_port)
     |      Moves a given volume of reagent [1] into syringe at speed [2] through specified valve
     |      position [3], then transfers syringe content through valve position [4] into an other
     |      location in the fluidic system. All parameters are integers respectively.
     |  
     |  move_reagent_slow(self, fill_volume, from_speed, from_port, to_speed, to_port)
     |      Moves a given volume of reagent [1] into syringe at speed [2] through specified valve
     |      position [3], then transfers syringe content through valve position [4] into an other
     |      location in the fluidic system. The last 200 ul reagent is drawn into the flowcell with 
     |      slower speed to avoid air bubble build up in the chambers. All parameters are integers 
     |      respectively.
     |  
     |  nonamer_prep(self, valve, nonamer_port)
     |      Moves nonamer and ligase into mixing chamber.
     |  
     |  prime_flowcells(self)
     |      Primes both flowcells with 'Wash 1' as initialization step.
     |  
     |  prime_fluidics_system(self)
     |      Primes all fluid lines, flowcells and reagent block chambers with 'Wash 1'.
     |      Assume that all reagent block chambers and bottles are filled with 'Wash 1'.
     |  
     |  prime_ligase(self)
     |      Primes ligase and ligation buffer chambers in reagent cooling block.
     |  
     |  prime_reagent_block(self)
     |      Primes all reagent block chambers with 'Wash 1'.
     |  
     |  prime_rotary_valve1(self)
     |      Primes reagent block chambers in ten port rotary valve V1.
     |  
     |  prime_rotary_valve2(self)
     |      Primes reagent block chambers in ten port rotary valve V2.
     |  
     |  prime_rotary_valve3(self)
     |      Primes reagent block chambers in ten port rotary valve V3.
     |  
     |  push_back_to_reagent_chamber(self, key)
     |      Pushes anchor primer, nonamer and Exonuclease 1 back to the reagent block cooler,
     |      after reagent usage in biochemistry steps (hybridization, ligation).
     |  
     |  reagent_block_init(self)
     |      Set reagent block cooler to constant temperature, 4 Celsius degrees.
     |  
     |  rotary_valve1_init(self)
     |      Initialize reagent start point for dH2O in ten port rotary valve V1.
     |  
     |  rotary_valve2_init(self)
     |      Initialize reagent start point for dH2O in ten port rotary valve V2.
     |  
     |  rotary_valve3_init(self)
     |      Initialize external reagent start points in ten port rotary valve V3.
     |  
     |  run(self)
     |      Runs polony sequencing cycle(s) based on cycle-name and flowcell-number list 
     |      already contained in biochemistry object.
     |  
     |  set_to_RT(self)
     |      Sets temperataure controller to room temperature (30 C).
     |  
     |  strip_chem(self)
     |      Performs chemical stripping protocol for polony sequencing. Does the following:
     |      
     |      - flush flowcell with dH2O
     |      - flush flowcell with guanidine HCl and incubate for 1' at RT
     |      - flush flowcell with dH2O
     |      - flush flowcell with NaOH and incubate for 1' at RT
     |      - flush flowcell with dH2O
     |      - flush flowcell with 'Wash 1'
     |  
     |  syringe_pump_init(self)
     |      Initializes syringe pump by moving it to zero position and setting speed to 20.
     |  
     |  temperature_control_init(self)
     |      Set temperature controller 1/2 to OFF state to avoid any temperature
     |      control operation left-over from a possible previous process.
     |  
     |  wait_for_SS(self, set_temp, poll_temp, tolerance=None)
     |      Waits until steady-state temperature is reached, or exits wait block if ramping
     |      time exceeds timeout parameter set in configuration file.\n\n"""

	sys.exit()

elif len(sys.argv) < 3:
	print '\n--> Error: not correct input!\n--> Usage: python biochem_utils.py flowcell-number method\n'
	sys.exit()

else:
	import ConfigParser						# Import configuration parser class.
	from logger import Logger				# Import logger class.
	from biochem import Biochem				# Import biochecmistry class.

	#--------------------- G.007 fluidics sub-system initialization ------------------------

	config = ConfigParser.ConfigParser()
	config.readfp(open('config.txt'))

	t0 = time.time()                # get current time
	logger = Logger(config)         # initialize logger object

	print '\n'

	biochem = Biochem('WL1', int(sys.argv[1]), logger)  # Initialize biochemistry object - cycle-name and flowcell-number need to be passed.

	#---------------------------------------------------------------------------------------
	#				 			  FLUIDICS SUB-SYSTEM FUNCTIONS
	#---------------------------------------------------------------------------------------

	logger.info('---\t-\t--> Started %s method execution - biochem_utils.py' % sys.argv[2])
	method = sys.argv[2]  # set method to second argument

	if method == 'clean_V1_to_syringe':
		biochem.clean_V1_to_syringe()

	elif method == 'clean_V2_to_syringe':
		biochem.clean_V2_to_syringe()

	elif method == 'clean_flowcell_and_syringe':
		biochem.clean_flowcell_and_syringe()

	elif method is 'cycle_ligation':
		biochem.cycle_ligation()

	elif method == 'draw_air_to_mixer':
		print "INFO\t---\t-\t--> Please, enter the air gap size [integer]: ",
		gap_size = int(sys.stdin.readline().strip())  # use stdin explicitly and remove trailing newline character
		biochem.draw_air_to_mixer(gap_size)

	elif method == 'draw_air_to_syringe':
		biochem.draw_air_to_syringe()

	elif method == 'draw_air_to_valve':
		print "INFO\t---\t-\t--> Please, enter valve name (V1, V2, V3) air to be drawn [string]: ",
		valve = str(sys.stdin.readline().strip())  # use stdin explicitly and remove trailing newline character
		biochem.draw_air_to_valve(valve)

	elif method == 'draw_into_flowcell':
		print "INFO\t ---\t-\t--> Please, enter name of reagent (Wash 1 / dH2O) to be drawn [string]: ",
		reagent = str(sys.stdin.readline().strip())  # use stdin explicitly and remove trailing newline character

		if reagent == 'Wash 1':
			port = 2
		else:
			port = 8

		print "\rINFO\t---\t-\t--> Please, enter volume to be drawn into flowcell [integer]: ",
		draw_volume = int(sys.stdin.readline().strip())  # use stdin explicitly and remove trailing newline character

		biochem.draw_into_flowcell(draw_volume, port)

	elif method == 'exo_start':
		biochem.exo_start()

	elif method == 'fill_with_air_to_valve':
		print "INFO\t---\t-\t--> Please, enter valve name (V1, V2, V3) air to be drawn [string]: ",
		valve = str(sys.stdin.readline().strip())  # use stdin explicitly and remove trailing newline character
		biochem.fill_with_air_to_valve(valve)

	elif method == 'flush_flowcell':
		print "INFO\t---\t-\t--> Please, enter name of reagent (Wash 1 / dH2O) to use as flush [string]: ",
		reagent = str(sys.stdin.readline().strip())  # use stdin explicitly and remove trailing newline character

		if reagent == 'Wash 1':
			port = 2
		elif reagent == 'dH2O':
			port = 8

		biochem.flush_flowcell(port)

	elif method == 'hyb':
		print "INFO\t---\t-\t--> Please, enter cycle name [string]: ",
		biochem.cycle = str(sys.stdin.readline().strip())[0:3]  # use stdin explicitly and remove trailing newline character
		biochem.hyb()

	elif method == 'incubate_reagent':
		print "INFO\t---\t-\t--> Please, enter incubation time in minutes [integer]: ",
		time = int(sys.stdin.readline().strip())  # use stdin explicitly and remove trailing newline character
		biochem.incubate_reagent(time)

	elif method == 'init':
		biochem.init()

	elif method == 'lig_stepup_peg':
		print "INFO\t---\t-\t--> Please, enter cycle name [string]: ",
		biochem.cycle = str(sys.stdin.readline().strip())[0:3]  # use stdin explicitly and remove trailing newline character
		biochem.lig_stepup_peg()

	elif method == 'ligase_mix':
		print "INFO\t---\t-\t--> Please, enter mixing time in seconds [integer]: ",
		time = int(sys.stdin.readline().strip())  # use stdin explicitly and remove trailing newline character
		biochem.ligase_mix(time)

	elif method == 'mixer_init':
		biochem.mixer_init()

	elif method == 'move_reagent':
		print "INFO\t---\t-\t--> Please, enter: fill_volume, from_speed, from_port, to_speed, to_port separated by single space [integers]: ",
		v = sys.stdin.readline().strip().split(' ')  # use stdin explicitly and remove trailing newline character
		biochem.move_reagent(int(v[0]), int(v[1]), int(v[2]), int(v[3]), int(v[4]))

	elif method == 'move_reagent_slow':
		print "INFO\t---\t-\t--> Please, enter: fill_volume, from_speed, from_port, to_speed, to_port separated by single space [integers]: ",
		v = sys.stdin.readline().strip().split(' ')  # use stdin explicitly and remove trailing newline character
		biochem.move_reagent_slow(int(v[0]), int(v[1]), int(v[2]), int(v[3]), int(v[4]))

	elif method == 'nonamer_prep':
		print "INFO\t---\t-\t--> Please, enter cycle name [string]: ",
		biochem.cycle = str(sys.stdin.readline().strip())[0:3]  # use stdin explicitly and remove trailing newline character
		biochem.nonamer_prep()

	elif method == 'prime_flowcells':
		biochem.prime_flowcells()

	elif method == 'prime_fluidics_system':
		biochem.prime_fluidics_system()

	elif method == 'prime_ligase':
		biochem.prime_ligase()

	elif method == 'prime_reagent_block':
		biochem.prime_reagent_block()

	elif method == 'prime_rotary_valve1':
		biochem.prime_rotary_valve1()

	elif method == 'prime_rotary_valve2':
		biochem.prime_rotary_valve2()

	elif method == 'prime_rotary_valve3':
		biochem.prime_rotary_valve3()

	elif method == 'push_back_to_reagent_chamber':
		print "INFO\t---\t-\t--> Please, enter reagent (A, N, E) to push back [character]: ",
		reagent = str(sys.stdin.readline().strip())  # use stdin explicitly and remove trailing newline character

		if reagent != 'E':
			print "\rINFO\t---\t-\t--> Please, enter cycle name [string]: ",
			biochem.cycle = str(sys.stdin.readline().strip())[0:3]  # use stdin explicitly and remove trailing newline character
	
		biochem.push_back_to_reagent_chamber(reagent)

	elif method == 'reagent_block_init':
		biochem.reagent_block_init()

	elif method == 'rotary_valve1_init':
		biochem.rotary_valve1_init()

	elif method == 'rotary_valve2_init':
		biochem.rotary_valve2_init()

	elif method == 'rotary_valve3_init':
		biochem.rotary_valve3_init()

	elif method == 'run':
		print "INFO\t---\t-\t--> Please, enter cycle name [string]: ",
		biochem.cycle = str(sys.stdin.readline().strip())[0:3]  # use stdin explicitly and remove trailing newline character
		biochem.run()

	elif method == 'set_to_RT':
		biochem.set_to_RT()

	elif method == 'strip_chem':
		biochem.strip_chem()

	elif method == 'syringe_pump_init':
		biochem.syringe_pump_init()

	elif method == 'temperature_control_init':
		biochem.temperature_control_init()

	elif method == 'wait_for_SS':
		print "INFO\t---\t-\t--> Please, enter: set_temp, poll_temp, tolerance separated by single space [integers]: ",
		v = sys.stdin.readline().strip().split(' ')  # use stdin explicitly and remove trailing newline character
		biochem.wait_for_SS(int(v[0]), int(v[1]), int(v[2]))

	else:
		print '\nWARN\t ---\t-\t--> Error: not correct method input!\nWARN\t ---\t-\t--> Double check method name (2nd argument)\n'
		sys.exit()

	#-------------------------- Duration of biochemistry test ------------------------------

	delta = (time.time() - t0) / 60  # Calculate elapsed time for flowcell flush.
	logger.info('---\t-\t--> Finished %s method execution - duration: %0.2f minutes\n' % (method, delta))

