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

#######################################################
## Date: 02/02/2019
## Author: Zhangyu Guan
## Network-wide setting, control variables
#######################################################

#######################################################
##    Configurations related to network topology 
#######################################################

import numpy

# networking area, in meter
area_x = 200                        # x-axis
area_y = 200                        # y-axis
area_z = 200                        # z-axis
grid_area_x = 10
grid_area_y = 10

# The number of pixels per meter, used to enlarge the canvas of the GUI
num_pixel_per_meter = 5             # The x-dimension of the GUI canvas would be area_x * num_pixel_per_meter

# GUI related
min_flying_height = 0.25 * area_z   # minimum flying height
gui = 'on'                          # 'on', 'off'

# LTE network configuration
num_lte_bs = 1            # number of LTE base stations
num_lte_ue = 10            # number of user equipment (UE)
num_lte_bs_mobile = 1     # number of mobile base stations
num_blk    = 10           # number of blockages

# Wi-Fi network configuration
num_wifi_ap  = 1            # number of access point
num_wifi_usr = 3            # number of wi-fi clients

# Maximum transmit power of nodes, in mW
max_pwr = 100

# Default number of antennas
dft_num_ant     = 1         # for regular node
dft_num_ant_bs  = 16        # for lte base station
dft_num_ant_ue  = 1         # for lte UE
dft_num_ant_ap  = 1         # for wifi access point
dft_num_ant_usr = 1         # for wifi user

#######################################################
##    Configurations related to discrete simulation 
#######################################################
# The number of symbols used in channel covariance estimation for LTE base stations
num_sym_4chn_cov_est = 1000

# The unit of time is tick, each tick corresponds to 9us, the time slot duration of wifi

usec_per_tick   = 10*1e-6                        # duration of basic time slot, 10 us <=> 1 tick
sim_time_sec    = 100                            # Simulation time in second, e.g., 30 means 30 second
sim_time_tick   = sim_time_sec/usec_per_tick     # Simulation time in tick

chn_cohr_time_sec = 0.15                                        # Channel coherent time
chn_cohr_time_tic = chn_cohr_time_sec/usec_per_tick             # Coherent time in tick

wifi_tsmt_time_sec = 100*1e-6                                   # wifi transmission time in second, 10us
wifi_tsmt_time_tick = wifi_tsmt_time_sec/usec_per_tick          # wifi transmission time in tick

# maximum/minimum dimension of blockage in meter
max_blk_dim = 20
min_blk_dim = 5
total_tick = 1000
###################################################################
# Frequency (GHz), bandwidth (MHz),reference distance(m) and transmit power(mW) for Microwave frequency band
micro = 3
micro_bandwidth = 2
micro_ref_dist = 100
micro_tsmt_pwr = 1000
        
# Frequency (GHz), bandwidth (MHz),reference distance(m) and transmit power(mW) for Millimeter frequency band
milli = 30
milli_bandwidth = 40
milli_ref_dist = 10
milli_tsmt_pwr = 250
        
# Frequency (GHz),bandwidth (MHz) and transmit power(mW) for Terahertz frequency band
tera = 300
tera_bandwidth = 10000
tera_tsmt_pwr = 20

band = {'micro':'micro', 'milli':'milli', 'tera':'tera'}
freq = {'micro':micro, 'milli':milli, 'tera':tera}                                          #frequency
bandw = {'micro':micro_bandwidth, 'milli':milli_bandwidth, 'tera':tera_bandwidth}           #bandwidth
ref_dist = {'micro':micro_ref_dist, 'milli':milli_ref_dist}       #reference distance
tsmt_pwr = {'micro':micro_tsmt_pwr, 'milli':milli_tsmt_pwr, 'tera':tera_tsmt_pwr}       #tsmt power

noise_figure = 10                            #in dB
constant = 1.752817778*1e-15                 #(4*pi/speed of light)^2
alpha_los_micro = 2                          # LOS path loss exponent
alpha_nlos_micro = 4                         # NLOS path loss exponent
alpha_los_milli = 6                         # LOS path loss exponent
alpha_nlos_milli = 8                       # NLOS path loss exponent
alpha_tera = 10                            # LOS path loss exponent
abs_coeff = 0.5                              # absorption coefficient(gamma)
theta_bs_milli = numpy.pi/6                  # BS beamwidth of main lobe for milli
theta_ue_milli = numpy.pi/6                  # UE beamwidth of main lobe for milli
theta_bs_tera = numpy.pi/10                   # BS beamwidth of main lobe for tera
theta_ue_tera = numpy.pi/10                  # UE beamwidth of main lobe for tera
Gmax_bs_milli = 100                         # max gain for BS for milli
Gmin_bs_milli = 1                           # min gain for BS for milli
Gmax_ue_milli = 100                         # max gain for UE for milli
Gmin_ue_milli = 1                          # min gain for UE for milli
Gmax_bs_tera = 100                          # max gain for BS for tera
Gmax_ue_tera = 100                          # max gain for UE for tera
Gmin_bs_tera = 1                            # min gain for BS for tera
Gmin_ue_tera = 10                           # min gain for UE for tera
Gmax_mbs_tera = 100
Gmax_mbs_milli = 100
sinr_threshold = -1e-12   
reinforcement_threshold = 0.99
reinforcement_total_tick = 100
plot_iteration_number = 1
average_iteration_number = 1
backhaul_tera_threshold = 30

theta_gbs_tera_bkhaul = numpy.pi/8
theta_mbs_tera_bkhaul = numpy.pi/10 
Gmax_gbs_tera_bkhaul = 100
Gmin_gbs_tera_bkhaul = 1
Gmax_mbs_tera_bkhaul= 100
Gmin_mbs_tera_bkhaul = 1

theta_gbs_milli_bkhaul = numpy.pi/6 
theta_mbs_milli_bkhaul = numpy.pi/8 
Gmax_gbs_milli_bkhaul =100
Gmin_gbs_milli_bkhaul =1
Gmax_mbs_milli_bkhaul =100
Gmin_mbs_milli_bkhaul = 1
#esn2_threshold = 10000
###################################################################