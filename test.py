#!/usr/local/bin/python

import sys
import time
import ConfigParser

from logger import Logger				
from biochem import Biochem				

config = ConfigParser.ConfigParser()
config.readfp(open('config.txt'))

t0 = time.time()                
logger = Logger(config)   

b = Biochem('WL1', 0, logger)

#b.mux.discrete_valve4_open()
b.mux.discrete_valve4_close()

