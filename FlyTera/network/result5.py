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
  
    fix_coord_array = np.array([])
    rate_all_users = []
    i=0
    x_axis_plot = []
    y_axis_plot = []
    ##################################################################################
    for bs in list_all_mbs:
        #print(bs)
        bs_obj_mbs = nt_obj.get_netelmt(bs) 
        fix_coord_list = []
        bs_obj_mbs = nt_obj.get_netelmt(bs) 
        #print('xxxxxx',bs_obj_mbs.name)
        x=bs_obj_mbs.coord_x
        fix_coord_list.append(x)
        y=bs_obj_mbs.coord_y
        x_axis_plot.append(x)
        y_axis_plot.append(y)
        #print(x,y)
        fix_coord_list.append(y)
        if i ==0:
            fix_coord_array = np.hstack((fix_coord_array,fix_coord_list))
        else:
            fix_coord_array = np.vstack((fix_coord_array,fix_coord_list))
        i+=1
    #print(fix_coord_array)   
    #print(np.size(fix_coord_array,0))
    ##################################################################################
    rate_all_bs = []
    rate_moving_mbs = []
    
    for index in range(len(nt_obj.grid_x_coord)):
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
                    sinr = serv_usr_obj.sinr
                    if serv_usr_obj.oper_freq == 'micro':
                        rate_user = netcfg.micro_bandwidth * np.log2(1 + sinr)
                    elif serv_usr_obj.oper_freq == 'milli': 
                        rate_user = netcfg.milli_bandwidth * np.log2(1 + sinr)
                    else:
                        rate_user = netcfg.tera_bandwidth * np.log2(1 + sinr) 
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
 
            if bs == random_mbs:
                #print('random',bs)
                bs_obj_mobile = nt_obj.get_netelmt(bs) 
                #print(bs)
                #print(fix_coord_array)
                #print(x_coord)
                #print(y_coord)
                #print('a',index)
                if index >= len(nt_obj.grid_x_coord):
                    index = index - int(index/len(nt_obj.grid_x_coord))*len(nt_obj.grid_x_coord)   
                #print('b',index)
                x= x_coord[index]
                y= y_coord[index]
                xy_array = np.hstack((xy_array,x))
                xy_array = np.hstack((xy_array,y))
                #print(xy_array)
                if (fix_coord_array == xy_array).all(-1).any():
                #if xy_array in fix_coord_array:
                    xy_array  = xy_array
                    
                else:
                    current_coord = bs_obj_mobile.get_coord()
                    new_coord = current_coord
                    #print(new_coord)
                    #print('aaaaaa',new_coord['x'],'...',new_coord['y'],'...',new_coord['z'])
                    new_coord['x'] = x
                    new_coord['y'] = y
                    new_coord['z'] = 50
                    x_axis_plot.append(x)
                    y_axis_plot.append(y)
                    bs_obj_mobile.set_coord(new_coord)
                    nt_obj.ini_dist()                  
                    nt_obj.update_association()
                    nt_obj.updt_band_association()
                    nt_obj.update_association_mbs_bs_link()
                    bs_obj_mobile.sinr_calc_mbs()
                    for user in nt_obj.get_node_list(net_name.lte_ue):
                        #print('1')
                        user_obj = nt_obj.get_netelmt(user)
                        #print('2')
                        user_obj.blk_detection()
                        #print('3')
                        user_obj.set_noise()
                        #print('4')
                        user_obj.sinr_calc()
                rate_moving_mbs.append(inter_rate_sum) 
            total_rate_bs.append(inter_rate_sum)
        rate_all_bs.append(sum(total_rate_bs))
        #print('c',index)
    return rate_all_bs
    # x =x_axis_plot
    # y =y_axis_plot
    # #print(len(x))
    # #print(len(y))
    
    # #fig = plt.figure()
    # #ax = fig.add_subplot(111, projection='3d')

    # x =x_axis_plot
    # y =y_axis_plot
    # z1 = rate_all_bs
    # z2 = rate_moving_mbs
    # #print(len(z1))
    # #print(len(z2))
    # #print('z1z1',z1)
    # #print('z2z2',z2)
    
    # ax.scatter3D(x, y, z1, c='r', marker='o',label='Rate for all users')
    # #ax.plot(x,y,z1, color='r')
    # ax.scatter3D(x, y, z2, c='b', marker='^', label='Rate for users served by moving MBS')
    # #ax.plot(x,y,z2, color='b')
    # ax.set_xlabel('X Coord')
    # ax.set_ylabel('Y Coord')
    # ax.set_zlabel('Rate in Mbps')
    # ax.set_title('Rate analysis with one moving MBS')
    # plt.legend()
    # plt.show()
