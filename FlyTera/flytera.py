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
## Date: 06/02/2019
## Author: Sabarish and Zhangyu
#######################################################

import sys
sys.path.insert(0, './network')
sys.path.insert(0, './gui')

# import definitions of network elements 
import net_ntwk, net_ctl
import net_name, net_channel
import control_logic
# network configuration
import netcfg

# discrete simulations
import simpy, numpy as np
import random
from matplotlib import pyplot as pp

import ESN2_training
import plot3d,result,result4,plots
# import matplotlib.pyplot as plt
# import networkx as nx
# G=nx.Graph()
exit()
#######################################################
## create the network 
#######################################################

print('Creating network with mobile base stations...')

# create an empty network
nt = net_ntwk.new_ntwk()
# set network area
nt.set_net_area(netcfg.area_x, netcfg.area_y, netcfg.area_z)                  

#print(nt.net_width,'\t',nt.net_length,'\t',nt.net_height)


nt.set_grid_mid_points()

#exit(0)
# Add network elements, base stations, use equipments, etc.                                         
nt.add_node(net_name.lte_bs, netcfg.num_lte_bs)                    # add ground base stations
nt.add_node(net_name.lte_bs_mobile, netcfg.num_lte_bs_mobile)      # add mobile base stations
nt.add_node(net_name.lte_ue, netcfg.num_lte_ue)                    # add LTE user equipments
#nt.add_node(net_name.lte_bs_mobile, netcfg.num_lte_bs_mobile)      # add mobile base stations
nt.add_node(net_name.blk, netcfg.num_blk)                          # add blockages

name_list_mobile_bs = nt.list_lte_bs_mobile
# print(name_list_mobile_bs)


for a in name_list_mobile_bs:
    idx = nt.list_lte_bs_mobile.index(a)
    #print(idx)
#exit(0)
# nx.draw(G)
# plt.show()
# plt.savefig("path.png")
# nx.draw_graphviz(G)
# nx.write_dot(G,'file.dot')
nt.add_gui()                                                       # add GUI

nt.ini_dist()


list_users= nt.get_node_list(net_name.lte_ue)

# for user in list_users:
    # user_obj = nt.get_netelmt(user)
    # print(user_obj.__dict__)
    #print(user_obj.serving_bs)
    #print(user_obj.oper_freq)
    #user_obj.updt_band()
    #print(user_obj.__dict__)
    #print(user_obj.oper_freq)
    #print (user_obj.oper_freq)#[user_obj.oper_freq])
    #print("usr obj", user_obj.oper_freq)
#exit(0)

# for user in list_users:
    # user_obj = nt.get_netelmt(user)
    # noise_user = user_obj.get_noise()
    # print(noise_user)
# exit(0)
#print('updating association')
nt.update_association()
nt.updt_band_association()
nt.update_association_mbs_bs_link()
#print('updating band association')



for bs in nt.get_node_list(net_name.lte_bs):
    bs_obj = nt.get_netelmt(bs)
    #print('a',bs_obj.served_user,'\n') 

for user in list_users:
    user_obj = nt.get_netelmt(user)
    #print(user_obj.coord_x,user_obj.coord_y,user_obj.coord_z,user_obj.sinr,'\n')
    #print(user_obj.__dict__)
    user_obj.blk_detection()
    user_obj.set_noise()
    #print(user_obj.oper_freq)
    #print('op freq',user_obj.oper_freq)
    #print('a')
    user_obj.sinr_calc()
    #print(user_obj.oper_freq)
    for bs in nt.get_node_list(net_name.lte_bs):
        bs_obj = nt.get_netelmt(bs)
        #print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
        #print('b',bs_obj.served_user,'\n')  
        
#exit(0)


# for bs in nt.get_node_list(net_name.lte_bs):
    # bs_obj = nt.get_netelmt(bs)
    # print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    # print('b',bs_obj.__dict__,'\n')   

for bs in name_list_mobile_bs:
    #print('aba',bs)
    bs_obj = nt.get_netelmt(bs)
    bs_obj.sinr_calc_mbs()
    #print(bs_obj.__dict__)
    #print(sinr)


for bs in nt.get_node_list(net_name.lte_bs):
    bs_obj = nt.get_netelmt(bs)
    #print(bs_obj.served_user,'\n')  
    
#exit(0)    
name_list_blk = nt.get_node_list(net_name.blk)
#print (name_list_blk)

for blk in name_list_blk:
    blk_obj = nt.get_netelmt(blk)
    #print(blk_obj.__dict__,'\n')  


    
env = simpy.Environment()
# # GUI
#if netcfg.gui == 'on':
  #  env.process(nt.gui.operation(env))
# create the network operation process for training
env.process(net_ctl.ctl_operation(env, nt))  
env.run(until=netcfg.total_tick)

#exit(0)
#input('...')
nt.train_data_prep()

for bs in name_list_mobile_bs:
    bs_obj = nt.get_netelmt(bs)
    bs_obj.esn_train() 
    #print(bs_obj.__dict__)
pp.show()

exit()

for bs in nt.get_node_list(net_name.lte_bs):
    bs_obj = nt.get_netelmt(bs)
    #print(bs_obj.__dict__,'\n')
    


env_control = simpy.Environment()
# create the network operation process for control logic
env_control.process(control_logic.ctl_operation(env_control, nt))  
env_control.run(until=netcfg.reinforcement_total_tick)
#exit()

for bs in name_list_mobile_bs:
    bs_obj = nt.get_netelmt(bs) 
    bs_idx = nt.list_lte_bs_mobile.index(bs)
    #ESN2_training.data_prep(bs_obj,bs_idx)

    

pp.show()
#exit()
result4.plots(nt)
exit()
# result.plots(nt)
# exit()
if netcfg.reinforcement_threshold ==0:
    result2.plots(nt)
else:
    result3.plots(nt)
exit()


# print(nt.name_list_all_nodes)

# list_base_stations= nt.get_node_list(net_name.lte_bs)

# for bs in list_base_stations:                    
    # idx = nt.name_list_all_nodes.index(bs)       # find the index of this name
    # #user_dist_row_to_other_nodes = nt.dist_matrix[idx]
    # #print(idx)
    # second_row = nt.dist_matrix[1]
    # print (second_row)
    # print(nt.dist_matrix[1][idx])

   
#exit(0)

#print(nt.get_node_list(net_name.lte_bs))


# list_blk= nt.get_node_list(net_name.blk)
# for blk in list_blk:
    # blk_obj = nt.get_netelmt(blk)
    # blk_obj.blk_aabb_box()
# exit(0)

#print(nt.name_list_all_nodes)
#Sexit(0)


#nt.gui.ping()



#print(dir(nt))
#exit(0)



#exit(0)
# #1 - Get the name list of all BS
# name_list_bs = nt.get_node_list(net_name.lte_bs)
# print(name_list_bs)
# #exit(0)

# #2 - Get the object of each BS
# for bs_name in name_list_bs:
    # bs_obj = nt.get_netelmt(bs_name)
    # #exit(0)
    # print(bs_obj.served_user)
# exit(0)

# x = nt.get_node_list(net_name.lte_bs)
# print(x)
# n = 1
# for bs_name in x:
    # bs_obj = nt.get_netelmt(bs_name)
    # dic_coord = bs_obj.get_coord()
    # print(bs_name, dic_coord)
    # new_dic_coord = dic_coord
    # new_dic_coord['x'] = dic_coord['x'] + n
    # new_dic_coord['y'] = dic_coord['y'] + n
    # new_dic_coord['z'] = dic_coord['z'] + n
    
    # bs_obj.set_coord(new_dic_coord)
    # dic_coord = bs_obj.get_coord()
    # print(bs_name, dic_coord)
    
    # print(nt.name_list_all_nodes)
    # print(nt.axis_x)
    
    # n+=1 
    
# # All nodes have been added, perform pre-processing, e.g., calculate the distance between nodes
# # Initialize channels between nodes
# # see net_ntwk.pre_processing for detailed definition
# nt.pre_processing()

# #######################################################
# ## start the network 
# #######################################################

# Create the environment of discrete simulation 
#env = simpy.Environment()

# # # Update channel state information
# # env.process(nt.chnl_state_gen(env, netcfg.cohr_time))

# # Create operations for each LTE base station

# Network operations
env.process(nt.operation(env))


# GUI
if netcfg.gui == 'on':
    env.process(nt.gui.operation(env))
    
# create the network operation process
env.process(net_ctl.ctl_operation(env, nt))   

# First, get the list of mobile LTE base stations

# Then, for each mobile LTE BS, create a process       
for name_node in name_list_mobile_bs:
    obj_node = nt.get_netelmt(name_node)        # get the corresponding object
    env.process(obj_node.operation(env))        # create the operation process

# Run the network
env.run(until=netcfg.total_tick)
input('...')
