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

# networking area, in meter
area_x = 200                        # x-axis
area_y = 200                        # y-axis
area_z = 200                        # z-axis

# The number of pixels per meter, used to enlarge the canvas of the GUI
num_pixel_per_meter = 5             # The x-dimension of the GUI canvas would be area_x * num_pixel_per_meter

# GUI related
min_flying_height = 0.25 * area_z   # minimum flying height
plot_net = True                     # True, False

# LTE network configuration
num_lte_bs = 2              # number of LTE base stations
num_lte_ue = 10             # number of user equipment (UE)

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
sim_time_sec    = 2                              # Simulation time in second, e.g., 30 means 30 second
sim_time_tick   = sim_time_sec/usec_per_tick     # Simulation time in tick

chn_cohr_time_sec = 0.15                                        # Channel coherent time
chn_cohr_time_tic = chn_cohr_time_sec/usec_per_tick             # Coherent time in tick

wifi_tsmt_time_sec = 100*1e-6                                   # wifi transmission time in second, 10us
wifi_tsmt_time_tick = wifi_tsmt_time_sec/usec_per_tick          # wifi transmission time in tick

noise_figure = 10 
tr_pwr_milli = 250 #in mW
tr_pwr_tera = 20 #in mW
path_loss_milli = 1
path_loss_tera = 2
