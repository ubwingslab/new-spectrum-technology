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

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import net_name
import netcfg
import numpy as np
import scipy.interpolate as interp
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
import random

def plots(nt_obj):
    x_coord = nt_obj.grid_x_coord
    #print(x_coord)
    y_coord = nt_obj.grid_y_coord
    #print(y_coord)
    list_all_bs = nt_obj.list_lte_bs
    #print(list_all_bs)
    list_all_mbs = nt_obj.list_lte_bs_mobile
    #print(list_all_mbs)
    random_mbs = random.choice(list_all_mbs)
    #print('random',random_mbs)
    index_mbs = []
    for bs in list_all_mbs:
        idx = nt_obj.name_list_all_nodes.index(bs)
        index_mbs.append(idx)
    #print(index_mbs)
    for idx in index_mbs:
        x_axis_plot_idx = [idx]
        y_axis_plot_idx = [idx]
    coord = {}
    for i in list_all_mbs:
        coord[str(i)+'x'] = []
        coord[str(i)+'y'] = []
    #print(coord)
    rate = {}
    for i in list_all_mbs:
        rate[str(i)] = []
        rate[str(i)] = []
    #print(rate)
    ##################################################################################
    rate_all_bs = []
    rate_moving_mbs = []
    for index in range(netcfg.plot_iteration_number):
        #print('index number',index+1)
        #print(index)
        xy_array = np.array([])
        total_rate_bs = []

        for bs in list_all_bs:
            intermediate_rate = []
            sum_intermediate_rate = []
            sum_rate = 0
            if bs in list_all_mbs:
                #print('a',bs)
                bs_obj = nt_obj.get_netelmt(bs) 
                bs_mbs_rate = bs_obj.rate
                rate_user = 0
                for serv_usr in bs_obj.served_user:
                    
                    serv_usr_obj = nt_obj.get_netelmt(serv_usr) 
                    #print(serv_usr_obj.name)
                    sinr = serv_usr_obj.sinr
                    if serv_usr_obj.oper_freq == 'micro':
                        rate_user = netcfg.micro_bandwidth * np.log2(1 + sinr)
                    elif serv_usr_obj.oper_freq == 'milli': 
                        rate_user = netcfg.milli_bandwidth * np.log2(1 + sinr)
                    else:
                        rate_user = netcfg.tera_bandwidth * np.log2(1 + sinr) 
                    #print(rate_user)
                    sum_rate = sum_rate + rate_user
                    rate_user = min(bs_mbs_rate,rate_user)
                    #intermediate_rate.append(rate_user)
                inter_rate_sum = rate_user
               
            else:
                #print('b',bs)
                bs_obj = nt_obj.get_netelmt(bs) 
                for serv_usr in bs_obj.served_user:
                    serv_usr_obj = nt_obj.get_netelmt(serv_usr) 
                    sinr = serv_usr_obj.sinr
                    if serv_usr_obj.oper_freq == 'micro':
                        rate_user = netcfg.micro_bandwidth * np.log2(1 + sinr)
                    elif serv_usr_obj.oper_freq == 'milli': 
                        rate_user = netcfg.milli_bandwidth * np.log2(1 + sinr)
                    else:
                        rate_user = netcfg.tera_bandwidth * np.log2(1 + sinr) 
                    intermediate_rate.append(rate_user)
                inter_rate_sum = sum(intermediate_rate)
                coord[str(bs)+'x'] = []
                coord[str(bs)+'y'] = []
                rate[str(bs)] = []
            if bs in list_all_mbs:
                idx = nt_obj.name_list_all_nodes.index(bs)
                #print('random',bs)
                bs_obj_mobile = nt_obj.get_netelmt(bs) 
                #print(bs)
                #print(fix_coord_array)
                #print(x_coord)
                #print(y_coord)
                next_best_location = bs_obj_mobile.next_best_loc_index
                data_array = bs_obj_mobile.data_needed_array
                #print(next_best_location)
                #print(data_array)
                xyz_coord = data_array[next_best_location[index]]
                #print(xyz_coord)
                x=bs_obj_mobile.best_x_coord[index]
                #print(x)
                y=bs_obj_mobile.best_y_coord[index]
                #print(y)
                xy_array = np.hstack((xy_array,x))
                xy_array = np.hstack((xy_array,y))
                #print(xy_array)
                current_coord = bs_obj_mobile.get_coord()
                new_coord = current_coord
                #print(new_coord)
                #print('aaaaaa',new_coord['x'],'...',new_coord['y'],'...',new_coord['z'])
                new_coord['x'] = x
                new_coord['y'] = y
                new_coord['z'] = 50
                coord[str(bs)+'x'].append(x)
                #print(coord[str(bs)+'x'])
                coord[str(bs)+'y'].append(y)
                #print(coord[str(bs)+'y'])
                #bs_obj_mobile.set_coord(new_coord)
                nt_obj.ini_dist()                  
                nt_obj.update_association()
                nt_obj.updt_band_association()
                nt_obj.update_association_mbs_bs_link()
                bs_obj_mobile.sinr_calc_mbs()
                for user in nt_obj.get_node_list(net_name.lte_ue):
                    #print('1')
                    user_obj = nt_obj.get_netelmt(user)
                    current_coord = user_obj.get_coord()
                    #print(current_coord)
                    new_coord = current_coord
                    #print(new_coord)
                    #print('aaaaaa',new_coord['x'],'...',new_coord['y'],'...',new_coord['z'])
                    x= random.choice(list(range(1,199)))
                    y= random.choice(list(range(1,199)))
                    new_coord['x'] = x
                    new_coord['y'] = y
                    new_coord['z'] = 0
                    user_obj.set_coord(new_coord)
                    #print(user,user_obj.get_coord())
                    #print('2')
                    user_obj.blk_detection()
                    #print('3')
                    user_obj.set_noise()
                    #print('4')
                    user_obj.sinr_calc()
                rate[str(bs)].append(inter_rate_sum) 
            total_rate_bs.append(inter_rate_sum)
        rate_all_bs.append(sum(total_rate_bs))
        
    return rate_all_bs