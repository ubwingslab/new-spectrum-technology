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
## Date: 02/03/2019
## Author: Zhangyu Guan
## Name space of network elements and attributes
#######################################################

##------------------------------------------
##          general definitions
##------------------------------------------

# whether to register an element in ntwk
if_rgst    = 'if_rgst'     

##------------------------------------------
##          network elements
##------------------------------------------

# Node type
ntwk        = 'ntwk'
lte_bs      = 'lte_bs'
lte_bs_cog  = 'lte_bs_cog'
lte_ue      = 'lte_ue'
wifi_ap     = 'wifi_ap'
wifi_usr    = 'wifi_usr'
wifi        = 'wifi'
lte         = 'lte'
dhs         = 'dhs'         # Drone hotspot

# Group type
group_bs    = 'group_bs'
group_ue    = 'group_ue'
group_ap    = 'group_ap'
group_usr   = 'group_usr'
group_dhs   = 'group_dhs'

# The list of supported node type, will be cheked when adding new nodes to the network
# used in net_ntwk.add_node()
node_type_list = [lte_bs, lte_bs_cog, lte_ue, wifi_ap, wifi_usr, dhs]

# Map the node type to the corresponding group 
node2group = {lte_bs:group_bs, lte_bs_cog:group_bs, lte_ue:group_ue, wifi_ap:group_ap, wifi_usr:group_usr, dhs:group_dhs}

# Channel
chnl     = 'chnl'          # channel module for a node, managing all channels from the node to other nodes
chnl_n2n = 'chnl_n2n'      # channel from node to node
Rayleigh = 'Rayleigh'
Rician   = 'Rician'

# Dimension of channel matrix 
chn_row = 'row_num_tsmtant'					# row: number of transmit antennas
chn_col = 'col_num_revrant'					# column: number of receiver antennas
chn_third_dim = 'third_dim_num_timeslot'    # third dimension: number of time slots    

# status of network element
on  = 'on'                  # The network element is active
off = 'off'                 # is inactive

# GUI
gui     = 'gui'
title   = 'Coexistence LTE and Wi-Fi'
title1  = 'Drone networks in mmWave/THz bands'