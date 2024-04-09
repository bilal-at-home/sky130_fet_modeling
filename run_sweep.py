import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()

from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

from PySpice.Spice.NgSpice.Shared import NgSpiceShared

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os


ngspice = NgSpiceShared.new_instance()

print(ngspice.exec_command('version -f'))
with open('ngspice_sweep.net', 'r') as file:
	circuit_template = file.read()

try:
	os.remove('sweep_nmos.csv')
except:
	print('can\'t remove nmos file')
	pass
try:
	os.remove('sweep_pmos.csv')
except:
	print('can\'t remove pmos file')
	pass

#vgs_list = np.arange(0,1.8+0.1,0.1)
#vds_list = [0.9]#np.arange(0,1.8+0.1,0.1)
#l_list = [0.15]#, 0.18, 0.2, 0.5, 0.8, 1.0, 2.0]

circuit_template = circuit_template.replace('let step_vgs = 0.5', 'let step_vgs = 0.01')
circuit_template = circuit_template.replace('let step_vds = 0.5', 'let step_vds = 0.01')
circuit_template = circuit_template.replace('set lvalues = ( 0.15 )','set lvalues = ( 0.15 0.18 0.25 0.5 1 2 5 )')

param_list = ['[w]','[l]','[gm]','[vth]','[gds]','[id]','[vds]','[vgs]', '[cgg]', '[cgd]', '[cgs]', '[cdd]', '[css]']


output_string1 = ''
output_string2 = ''
for item in param_list:
	output_string1 += '{$dut1}'+item+' '
	output_string2 += '{$dut2}'+item+' '
circuit_template = circuit_template.replace('{$dut1}[gm]',output_string1)
circuit_template = circuit_template.replace('{$dut2}[gm]',output_string2)
#print(circuit_template)

ngspice.load_circuit(circuit_template)
ngspice.exec_command('reset')
ngspice.run()

'''
#print(ngspice.ressource_usage())
#print(ngspice.status())
#plot = ngspice.plot(simulation=None, plot_name=ngspice.last_plot)
#print(plot)
'''