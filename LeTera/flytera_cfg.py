# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
import scipy.io as sio

# Number of drone hotspots
num_dhs = 2                         

# Initial coordinates of the two drones, with distance around 10 meters
ini_axis_x = np.matrix('100   107')
ini_axis_y = np.matrix('100   107')
ini_axis_z = np.matrix('10     10')

#######################################################
## Load traces of the drones

## Variables contained in the traces:
## gyr_micro_1000_inst1
## gyr_micro_1000_inst2
## gyr_micro_1000_inst3
## gyr_micro_1000_inst4

## gyr_small_1000_inst1
## gyr_small_1000_inst2
## gyr_small_1000_inst3
## gyr_small_1000_inst4

## gyr_large_75_inst1
## gyr_large_75_inst2

## lac_micro_1000_inst1
## lac_micro_1000_inst2

## lac_small_1000_inst1
## lac_small_1000_inst2

## 1000 means there are 1000 samples, and 75 means 75 samples

## For all micro and small traces, the sampling rate is 200
## For large traces, the sampling rate is 15
#######################################################

# for conference version
mat_fname = 'dhs_trace.mat'    
dhs_trace = sio.loadmat(mat_fname)

# for journal version
new_mat_fname = 'all_data_trace.mat'  
dhs_new_trace = sio.loadmat(new_mat_fname)

# print(dhs_trace['lac_micro_1000_inst1'])print(dhs_new_trace['large_indoor_gyr_40_50'])
# exit(0)

# Trace selection
gry_trace_id    = [0, 1]            # [for dhs1, for dhs2]
gry_trace_name  = ['gyr_micro_1000_inst1', 'gyr_micro_1000_inst2', 'gyr_micro_1000_inst3', 'gyr_micro_1000_inst4',\
                   'gyr_small_1000_inst1', 'gyr_small_1000_inst2', 'gyr_small_1000_inst3', 'gyr_small_1000_inst4',\
                   'gyr_large_75_inst1',   'gyr_large_75_inst2'] 

gry_trace_name_new = ['large_indoor_gyr_0_10', 'large_indoor_gyr_10_20', 'large_indoor_gyr_20_30', 'large_indoor_gyr_30_40', 'large_indoor_gyr_40_50',\
                        'large_indoor_gyr_50_60', 'large_indoor_gyr_60_70', 'large_indoor_gyr_70_80', 'large_indoor_gyr_80_90', 'large_indoor_gyr_90_100',\
                        'large_outdoor_gyr_0_10', 'large_outdoor_gyr_10_20', 'large_outdoor_gyr_20_30', 'large_outdoor_gyr_30_40', 'large_outdoor_gyr_40_50',\
                        'large_outdoor_gyr_50_60', 'large_outdoor_gyr_60_70', 'large_outdoor_gyr_70_80', 'large_outdoor_gyr_80_90', 'large_outdoor_gyr_90_100',\
                        'large_windy_gyr_0_10', 'large_windy_gyr_10_20', 'large_windy_gyr_20_30', 'large_windy_gyr_30_40', 'large_windy_gyr_40_50',\
                        'large_windy_gyr_50_60', 'large_windy_gyr_60_70', 'large_windy_gyr_70_80', 'large_windy_gyr_80_90', 'large_windy_gyr_90_100',\
                        'micro_indoor_gyr_0_10', 'micro_indoor_gyr_10_20', 'micro_indoor_gyr_20_30', 'micro_indoor_gyr_30_40', 'micro_indoor_gyr_40_50',\
                        'micro_indoor_gyr_50_60', 'micro_indoor_gyr_60_70', 'micro_indoor_gyr_70_80', 'micro_indoor_gyr_80_90', 'micro_indoor_gyr_90_100',\
                        'micro_outdoor_gyr_0_10', 'micro_outdoor_gyr_10_20', 'micro_outdoor_gyr_20_30', 'micro_outdoor_gyr_30_40', 'micro_outdoor_gyr_40_50',\
                        'micro_outdoor_gyr_50_60', 'micro_outdoor_gyr_60_70', 'micro_outdoor_gyr_70_80', 'micro_outdoor_gyr_80_90', 'micro_outdoor_gyr_90_100',\
                        'micro_windy_gyr_0_10', 'micro_windy_gyr_10_20', 'micro_windy_gyr_20_30', 'micro_windy_gyr_30_40', 'micro_windy_gyr_40_50',\
                        'micro_windy_gyr_50_60', 'micro_windy_gyr_60_70', 'micro_windy_gyr_70_80', 'micro_windy_gyr_80_90', 'micro_windy_gyr_90_100',\
                        'small_indoor_gyr_0_10', 'small_indoor_gyr_10_20', 'small_indoor_gyr_20_30', 'small_indoor_gyr_30_40', 'small_indoor_gyr_40_50',\
                        'small_indoor_gyr_50_60', 'small_indoor_gyr_60_70', 'small_indoor_gyr_70_80', 'small_indoor_gyr_80_90', 'small_indoor_gyr_90_100',\
                        'small_outdoor_gyr_0_10', 'small_outdoor_gyr_10_20', 'small_outdoor_gyr_20_30', 'small_outdoor_gyr_30_40', 'small_outdoor_gyr_40_50',\
                        'small_outdoor_gyr_50_60', 'small_outdoor_gyr_60_70', 'small_outdoor_gyr_70_80', 'small_outdoor_gyr_80_90', 'small_outdoor_gyr_90_100',\
                        'small_windy_gyr_0_10', 'small_windy_gyr_10_20', 'small_windy_gyr_20_30', 'small_windy_gyr_30_40', 'small_windy_gyr_40_50',\
                        'small_windy_gyr_50_60', 'small_windy_gyr_60_70', 'small_windy_gyr_70_80', 'small_windy_gyr_80_90', 'small_windy_gyr_90_100']
                        
# print(dhs_trace['gyr_micro_1000_inst4'])
# exit(0)
#print(np.repeat(200,np.size(gry_trace_name_new)))
#exit()

# Sampling rate for each trace
gry_trace_smpl_rate = np.repeat(200,np.size(gry_trace_name_new))            
# print(gry_trace_smpl_rate)

# Large scale linear acceleration is not collected, will be generated randomly
lac_trace_id   = [0, 1]              # [for dhs1, for dhs2]
lac_trace_name = ['lac_micro_1000_inst1', 'lac_micro_1000_inst2', 'lac_small_1000_inst1', 'lac_small_1000_inst2',\
                  'lac_large_inst1', 'lac_large_inst2']
                  
lac_trace_name_new = ['large_indoor_laac_0_10', 'large_indoor_laac_10_20', 'large_indoor_laac_20_30', 'large_indoor_laac_30_40', 'large_indoor_laac_40_50',\
                        'large_indoor_laac_50_60', 'large_indoor_laac_60_70', 'large_indoor_laac_70_80', 'large_indoor_laac_80_90', 'large_indoor_laac_90_100',\
                        'large_outdoor_laac_0_10', 'large_outdoor_laac_10_20', 'large_outdoor_laac_20_30', 'large_outdoor_laac_30_40', 'large_outdoor_laac_40_50',\
                        'large_outdoor_laac_50_60', 'large_outdoor_laac_60_70', 'large_outdoor_laac_70_80', 'large_outdoor_laac_80_90', 'large_outdoor_laac_90_100',\
                        'large_windy_laac_0_10', 'large_windy_laac_10_20', 'large_windy_laac_20_30', 'large_windy_laac_30_40', 'large_windy_laac_40_50',\
                        'large_windy_laac_50_60', 'large_windy_laac_60_70', 'large_windy_laac_70_80', 'large_windy_laac_80_90', 'large_windy_laac_90_100',\
                        'micro_indoor_laac_0_10', 'micro_indoor_laac_10_20', 'micro_indoor_laac_20_30', 'micro_indoor_laac_30_40', 'micro_indoor_laac_40_50',\
                        'micro_indoor_laac_50_60', 'micro_indoor_laac_60_70', 'micro_indoor_laac_70_80', 'micro_indoor_laac_80_90', 'micro_indoor_laac_90_100',\
                        'micro_outdoor_laac_0_10', 'micro_outdoor_laac_10_20', 'micro_outdoor_laac_20_30', 'micro_outdoor_laac_30_40', 'micro_outdoor_laac_40_50',\
                        'micro_outdoor_laac_50_60', 'micro_outdoor_laac_60_70', 'micro_outdoor_laac_70_80', 'micro_outdoor_laac_80_90', 'micro_outdoor_laac_90_100',\
                        'micro_windy_laac_0_10', 'micro_windy_laac_10_20', 'micro_windy_laac_20_30', 'micro_windy_laac_30_40', 'micro_windy_laac_40_50',\
                        'micro_windy_laac_50_60', 'micro_windy_laac_60_70', 'micro_windy_laac_70_80', 'micro_windy_laac_80_90', 'micro_windy_laac_90_100',\
                        'small_indoor_laac_0_10', 'small_indoor_laac_10_20', 'small_indoor_laac_20_30', 'small_indoor_laac_30_40', 'small_indoor_laac_40_50',\
                        'small_indoor_laac_50_60', 'small_indoor_laac_60_70', 'small_indoor_laac_70_80', 'small_indoor_laac_80_90', 'small_indoor_laac_90_100',\
                        'small_outdoor_laac_0_10', 'small_outdoor_laac_10_20', 'small_outdoor_laac_20_30', 'small_outdoor_laac_30_40', 'small_outdoor_laac_40_50',\
                        'small_outdoor_laac_50_60', 'small_outdoor_laac_60_70', 'small_outdoor_laac_70_80', 'small_outdoor_laac_80_90', 'small_outdoor_laac_90_100',\
                        'small_windy_laac_0_10', 'small_windy_laac_10_20', 'small_windy_laac_20_30', 'small_windy_laac_30_40', 'small_windy_laac_40_50',\
                        'small_windy_laac_50_60', 'small_windy_laac_60_70', 'small_windy_laac_70_80', 'small_windy_laac_80_90', 'small_windy_laac_90_100'] 

#print(gry_trace_name_new)
#print(lac_trace_name_new)
#exit()                        
#lac_trace_smpl_rate = [200, 200, 200, 200]  
lac_trace_smpl_rate = np.repeat(200,np.size(gry_trace_name_new))

#######################################################
##    Configurations related to discrete simulation 
#######################################################
time_wait  = 0.1       # time to wait, used for animation only
sim_tick   = 1000    # the number ticks to simulate
beam_index = 1000

#######################################################
##    Antenna model 
#######################################################
angle   = 5               # Beamwidth in degree 
radius  = 0.04            # Radius of receive surface in meter 


bw_milli = 4000             # bandwidth for mmwave in MHz
bw_tera = 10000           # bandwidth for tera in MHz
freq_milli = 30           # frequency for mmwave in GHz
freq_tera = 300           # frequency for tera in GHz
mol_abs_coeff_milli = 1.111e-4
mol_abs_coeff_tera = 1.25e-3
tr_pow_milli = 250        #in mW
tr_pow_tera = 20          #in mW
ant_gain = 10
boltzmann_const = 1.3806e-23   #J/K
ref_temp = 296                 #K
'''bandwidth(MHz), frequency(GHz), mol_abs_coeff, normalizing_constant, standard deviation, boltzmann constant, reference temperature'''
milli = bw_milli, freq_milli, mol_abs_coeff_milli, tr_pow_milli, ant_gain, boltzmann_const, ref_temp
tera = bw_tera, freq_tera, mol_abs_coeff_tera, tr_pow_tera, ant_gain, boltzmann_const, ref_temp
const_data = {'milli': milli, 'tera':tera}
# Beam searching time
beam_sch_time = 0.01      # in second, takes values from [0.01, 0.05, 0.1, 0.5] 

# Beam alignment interval
beam_alignment_itvl = [1, 50, 100]

# Plot, updated as the network runs
sim_index   = 0           # 0, 1, 2, updating data1, data2, data3, respectively. sim_time updated if 0

sim_time    = [0]
data_bai1   = []
data_bai100 = []
data_bai1000 = []
data1       = []
data2       = []
data3       = []
distance    = []
data_tr_xyz = []
data_tr_rpy = []
data_rx_xyz = []
data_rx_rpy = []
beam_plot_data = []
data_snr_db_1 = []
data_snr_db_100 = []

#######################################################
##    Configurations for different figures
#######################################################


fig1 = {'gry_trace_id':(25, 27), 'lac_trace_id':(25, 27), 'beam_alignment_itvl':(1, 50, 100), 'beam_width': 5, 'oper_freq':'tera'}       #large_windy,large_windy (case 1)23252529
fig2 = {'gry_trace_id':(14, 15), 'lac_trace_id':(14, 15), 'beam_alignment_itvl':(1, 50, 100), 'beam_width': 5, 'oper_freq':'tera'}       #large_outdoor,large_outdoor xxxxxxx
fig3 = {'gry_trace_id':(14, 27), 'lac_trace_id':(14, 27), 'beam_alignment_itvl':(1, 50, 100), 'beam_width': 5, 'oper_freq':'tera'}       #large_outdoor,large windy yyyyyyy

figs = {'1':fig1, '2':fig2, '3':fig3}
