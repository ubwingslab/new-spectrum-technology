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

import sys, os
sys.path.insert(0, './network')
os.system('cls')

# import definitions of network elements 
import net_ntwk
import net_name, net_channel

# network configuration
import netcfg, flytera_cfg

# discrete simulations
import simpy, numpy as np

def run_net(beam_alignment_itvl = 10):
    '''
    Run Network with given beam alignment interval, default 10 ticks
    '''
    #######################################################
    ## create the network 
    #######################################################
    #print('Creating flying drone networks...')

    # create an empty network
    nt = net_ntwk.new_ntwk()
    # set network area
    nt.set_net_area(netcfg.area_x, netcfg.area_y, netcfg.area_z)                  

    # Add network elements, base stations, use equipments, etc.                                         
    nt.add_node(net_name.dhs, flytera_cfg.num_dhs)                    # add two drone hotspots

    # All nodes have been added, perform pre-processing, e.g., calculate the distance between nodes
    # Initialize channels between nodes
    # see net_ntwk.pre_processing for detailed definition
    nt.pre_processing()
    
    for node in nt.get_node_list(net_name.dhs):
        #print(node)
        dhs_obj = nt.get_netelmt(node)
        #print(dhs_obj.__dict__)
    #######################################################
    ## start the network 
    #######################################################

    # Create the environment of discrete simulation 
    env = simpy.Environment()

    # GUI
    # if netcfg.plot_net == True:
        # env.process(nt.gui.operation(env))

    # First, get the list of dhs
    node_list = nt.get_node_list(net_name.dhs)

    # Then, for each LTE BS, create a process       
    for name_node in node_list:
        obj_node = nt.get_netelmt(name_node)        # get the corresponding object
        env.process(obj_node.operation(env))        # create the operation process
        
    # Beam alignment
    #print('xxxx', beam_alignment_itvl)
    env.process(nt.beam_alignment(env, beam_alignment_itvl))
        
    # Network-wide operation
    env.process(nt.operation(env))

    # Run the network
    env.run(until=flytera_cfg.sim_tick)
