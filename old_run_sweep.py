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
#print(ngspice.exec_command('print all'))
#print(ngspice.exec_command('devhelp'))
#print(ngspice.exec_command('devhelp resistor'))

circuit_template = ' ** sch_path: /home/bilal/model_generation/fet_sweep.sch \n\
**.subckt fet_sweep \n\
VGS nmos_vgs GND {vgs} \n\
XM1 nmos_vds nmos_vgs GND GND sky130_fd_pr__nfet_01v8 L={l} W=5 nf=1 ad=\'int((nf+1)/2) * W/nf * 0.29\' \n\
+ as=\'int((nf+2)/2) * W/nf * 0.29\' pd=\'2*int((nf+1)/2) * (W/nf + 0.29)\' ps=\'2*int((nf+2)/2) * (W/nf + 0.29)\' \n\
+ nrd=\'0.29 / W\' nrs=\'0.29 / W\' sa=0 sb=0 sd=0 mult=1 m=1 \n\
VDS nmos_vds GND {vds} \n\
.save i(vds) \n\
**** begin user architecture code \n\
\n\
\n\
.lib D:\\Users\\Bilal\\TinyTapeout\\volare\\sky130\\versions\\bdc9412b3e468c102d01b7cf6337be06ec6e9c9a\\sky130A\\libs.tech\\combined\\sky130.lib.spice tt \n\
.param vds= \n\
.param vgs= \n\
.param l= \n\
.save all \n\
.control \n\
	set dut = \'@m.xm1.msky130_fd_pr__nfet_01v8\' \n\
	reset\n\
	set appendwrite \n\
	OP \n\
	*set wr_vecnames\n\
	wrdata sweep.csv {$dut}[gm] \n\
	**plot -2*vds#branch/@m.xm1.msky130_fd_pr__nfet_01v8[gm] \n\
	set appendwrite \n\
.endc \n\
 \n\
.GLOBAL GND \n\
.end \n\
'
try:
	os.remove('sweep.csv')
except:
	pass

vgs_list = np.arange(0,1.8+0.1,0.1)
vds_list = [0.9]#np.arange(0,1.8+0.1,0.1)
l_list = [0.15]#, 0.18, 0.2, 0.5, 0.8, 1.0, 2.0]
param_list = ['[w]','[l]','[gm]','[vth]','[gds]','[id]','[vds]','[vgs]', '[cgg]', '[cgd]', '[cgs]']
#param_list = ['[vgs]']
circuit_template = circuit_template.replace('set wr_vecnames','')
output_string = ''
for item in param_list:
	output_string += '{$dut}'+item+' '
circuit_template = circuit_template.replace('{$dut}[gm]',output_string)
for l in l_list:
	for vds in vds_list:
		for vgs in vgs_list:
			circuit_run = circuit_template.replace('.param l= ','.param l='+str(l)+' ')
			circuit_run = circuit_run.replace('.param vds= ','.param vds='+str(vds)+' ')
			circuit_run = circuit_run.replace('.param vgs= ','.param vgs='+str(vgs)+' ')
			#print(circuit_run)
			ngspice.load_circuit(circuit_run)
			ngspice.exec_command('reset')
			ngspice.run()

#print(ngspice.ressource_usage())
#print(ngspice.status())
#plot = ngspice.plot(simulation=None, plot_name=ngspice.last_plot)
#print(plot)
