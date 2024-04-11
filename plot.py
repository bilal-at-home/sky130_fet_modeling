import matplotlib
import matplotlib.pyplot as plt
import csv
import numpy as np
import os
import pandas
import math

filename_list = ['sweep_nmos.csv','sweep_pmos.csv']
param_list = ['[w]','[l]','[gm]','[vth]','[gds]','[id]','[vds]','[vgs]', '[cgg]', '[cgd]', '[cgs]', '[cdd]', '[css]']

param_list_extended = []
param_list_new  = []
count = 0
for item in param_list:
	param_list_new.append(item.replace('sweep_','').replace('[','').replace('sweep_','').replace(']',''))
param_list = param_list_new

for item in param_list:
	count += 1 
	param_list_extended.append('temp'+str(count))
	param_list_extended.append(item)

#print(param_list_extended)
for filename in filename_list:
	with open(filename,'r') as csvfile:
		file = pandas.read_csv(csvfile,header=None,index_col=False,skipinitialspace=True,sep='\\s+',names=param_list_extended,usecols=param_list)
	file['delta'] = file.apply(lambda row: 2*row.id/row.gm, axis=1)
	l_list = [0.15, 0.18, 0.25, 0.5, 1, 2]
	#l_list = [0.15]
	fig1, ax1 = plt.subplots()
	fig2, ax2 = plt.subplots()
	fig3, ax3 = plt.subplots()
	fig4, ax4 = plt.subplots()
	fig5, ax5 = plt.subplots()
	fig6, ax6 = plt.subplots()
	fig7, ax7 = plt.subplots()
	vds = 0.5
	vgs = 0.9
	for l in l_list:
		file_l = file.loc[(file['l']==l*1e-6)]
		to_print = file_l.loc[(file_l['vds']>vds)&(file_l['vds']<vds+0.01)]
		#plt.plot(file.loc[(file['l']==1.5e-7)&(file['vds']>0.89)&(file['vds']<0.91)]['vgs'],file.loc[(file['l']==1.5e-7)&(file['vds']>0.89)&(file['vds']<0.91)]['id'],'*')
		#plt.show()
		ax1.plot(to_print['delta'],to_print['id']/to_print['w'],'-',label=l)
		ax3.plot(to_print['delta'],to_print['gm']/to_print['gds'],'-',label=l)
		ax4.plot(to_print['delta'],to_print['gm']/to_print['cgg']/2/math.pi/1e9,'-',label=l)
		ax5.plot(to_print['delta'],to_print['gm']/to_print['id']*to_print['gm']/to_print['cgg']/2/math.pi/1e9,'-',label=l)
		ax6.plot(to_print['delta'],to_print['cgg']*1e15,'-',label=l)
		ax7.plot(to_print['delta'],abs(to_print['cgs'])/to_print['cgg'],'-',label=l)
		#ax7[1].plot(to_print['delta'],to_print['cgd']/to_print['cgg'],'-',label=l)
	for l in l_list:
		file_l = file.loc[(file['l']==l*1e-6)]
		to_print = file_l.loc[(file_l['vgs']>vgs)&(file_l['vgs']<vgs+0.01)]
		ax2.plot(to_print['vds'],1/to_print['gds']/1000,'-',label=l)
	#print(to_print)

	ax1.set_xlim(0.1,0.5)
	#ax1.set_ylim(0.0,100)
	ax1.set_xlabel(u'Δ [V]')
	ax1.set_ylabel(u'Id/W [uA/um]')
	ax1.set_title(u'Current density v/s Δ = 2Id/gm @vds='+str(vds))
	ax1.legend()
	ax1.grid('both')
	fig1.savefig(filename.replace('sweep_','').replace('.csv','_')+'CurrentDensity.png')

	ax2.set_xlim(0.1,1.8)
	ax2.set_ylim(0.0,200)
	ax2.set_xlabel(u'Vds [V]')
	ax2.set_ylabel(u'rds [kOhm]')
	ax2.set_title(u'Rds v/s Vds @W=5um;vgs='+str(vgs))
	ax2.legend()
	ax2.grid('both')
	fig2.savefig(filename.replace('sweep_','').replace('.csv','_')+'RdsVds.png')

	ax3.set_xlim(0.1,0.5)
	ax3.set_ylim(0.0,300)
	ax3.set_xlabel(u'Δ [V]')
	ax3.set_ylabel(u'gmrds')
	ax3.set_title(u'gmRds v/s Δ @W=5um;vds='+str(vds))
	ax3.legend()
	ax3.grid('both')
	fig3.savefig(filename.replace('sweep_','').replace('.csv','_')+'gmRds.png')

	ax4.set_xlim(0.1,0.5)
	#ax4.set_ylim(0.0,170)
	ax4.set_xlabel(u'Δ [V]')
	ax4.set_ylabel(u'fT [Ghz]')
	ax4.set_title(u'fT v/s Δ @W=5um;vds='+str(vds))
	ax4.legend()
	ax4.grid('both')
	fig4.savefig(filename.replace('sweep_','').replace('.csv','_')+'fT.png')

	ax5.set_xlim(0.1,0.5)
	#ax4.set_ylim(0.0,170)
	ax5.set_xlabel(u'Δ [V]')
	ax5.set_ylabel(u'gm/Id .fT')
	ax5.set_title(u'gm/Id . fT v/s Δ @W=5um;vds='+str(vds))
	ax5.legend()
	ax5.grid('both')
	fig5.savefig(filename.replace('sweep_','').replace('.csv','_')+'gmIdfT.png')

	ax6.set_xlim(0.1,0.5)
	#ax4.set_ylim(0.0,170)
	ax6.set_xlabel(u'Δ [V]')
	ax6.set_ylabel(u'Cgg [fF]')
	ax6.set_title(u'W=5um Δ @vds='+str(vds))
	ax6.legend()
	ax6.grid('both')
	fig6.savefig(filename.replace('sweep_','').replace('.csv','_')+'Cgg.png')

	ax7.set_xlim(0.1,0.5)
	#ax4.set_ylim(0.0,170)
	ax7.set_xlabel(u'Δ [V]')
	ax7.set_ylabel(u'Kcgs')
	ax7.set_title(u'W=5um Δ @vds='+str(vds))
	ax7.legend()
	ax7.grid('both')
	fig7.savefig(filename.replace('sweep_','').replace('.csv','_')+'Kcgs.png')

plt.show()
