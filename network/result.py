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
import result1,result2,result3,result5

def plots(nt_obj):
    
    list_all_mbs = nt_obj.list_lte_bs_mobile
    #print(list_all_mbs)
    x_axis_plot = []
    y_axis_plot = []
    ##################################################################################
    for bs in nt_obj.list_lte_bs:
        #print(bs)
        total_rate_bs = []
        bs_obj_mbs = nt_obj.get_netelmt(bs) 
        fix_coord_list = []
        bs_obj_mbs = nt_obj.get_netelmt(bs) 
        #print('xxxxxx',bs_obj_mbs.name)
        x=bs_obj_mbs.coord_x
        fix_coord_list.append(x)
        y=bs_obj_mbs.coord_y
        x_axis_plot.append(x)
        y_axis_plot.append(y)
        
    #print(x_axis_plot)
    #print(y_axis_plot)
    total_rate_mbs = []
    total_rate_bs = []
    for bs in nt_obj.list_lte_bs:
        intermediate_rate = []
        sum_intermediate_rate = []
        if bs in list_all_mbs:
            #print('a',bs)
            bs_obj = nt_obj.get_netelmt(bs) 
            bs_mbs_rate = bs_obj.rate
            for serv_usr in bs_obj.served_user:
                serv_usr_obj = nt_obj.get_netelmt(serv_usr) 
                sinr = serv_usr_obj.sinr
                if serv_usr_obj.oper_freq == 'micro':
                    rate_user = netcfg.micro_bandwidth * np.log2(1 + sinr)
                elif serv_usr_obj.oper_freq == 'milli': 
                    rate_user = netcfg.milli_bandwidth * np.log2(1 + sinr)
                else:
                    rate_user = netcfg.tera_bandwidth * np.log2(1 + sinr) 
                rate_user = min(bs_mbs_rate,rate_user)
                intermediate_rate.append(rate_user)
            inter_rate_sum_bs = sum(intermediate_rate)
            total_rate_bs.append(inter_rate_sum_bs)
            total_rate_mbs.append(inter_rate_sum_bs)
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
            inter_rate_sum_bs = sum(intermediate_rate)
            total_rate_bs.append(inter_rate_sum_bs) 
        
    #print('bs rate',total_rate_bs)
    #print('mbs rate',total_rate_mbs)
    fig = plt.figure(1)
    #ax = fig.add_subplot(111, projection='3d')
    
    x_bs = x_axis_plot[0:netcfg.num_lte_bs]
    y_bs = y_axis_plot[0:netcfg.num_lte_bs]
    x_mbs = x_axis_plot[netcfg.num_lte_bs:]
    y_mbs = y_axis_plot[netcfg.num_lte_bs:]
    z1 = sum(total_rate_bs)#[0:netcfg.num_lte_bs]
    #z2 = np.add(total_rate_mbs,z1)
    #z3 = total_rate_mbs
    #print(z2)
    z1 = np.repeat(z1,netcfg.plot_iteration_number)
    z2 = result1.plots(nt_obj)
    z3 = result2.plots(nt_obj)
    z4 = result3.plots(nt_obj)
    z5 = result5.plots(nt_obj)
    # z4_size = np.size(z4)
    # z4_1 = z4[0:z4_size-int(0.95*z4_size)]
    # z4_2 = z4[z4_size-int(0.95*z4_size):]
    # #print(z4_2)
    # z_4_2 = sorted(z4_2, key = float)
    # #print(z_4_2)
    # z4 = z4_1 + z_4_2
    #print(np.size(z4_1))
    #print(np.size(z4_2))
    x_axis = list(range(1,netcfg.plot_iteration_number+1))
    x_axis_all_grid = list(range(len(nt_obj.grid_x_coord)))
    
    font = {'family' : 'sans',
        'size'   : 16}	
    plt.rc('font', **font)
    #plt.plot(x_axis, z1, c='r', marker='o',linestyle='-',label='Rate for users with fixed MBS ')
    #plt.plot(x_axis_all_grid, z2, c='b', marker='o',linestyle='--',label='Rate for all users served with one moving MBS')
    plt.plot(x_axis, z5, c='k',linestyle='--', label='MBS moves to all grid locations')
    plt.plot(x_axis, z2, c='g', marker='.',linestyle='--',label='Fixed MBS')
    plt.plot(x_axis, z3, c='m', marker='.',linestyle='-.',label='MBS moving randomly')
    plt.plot(x_axis, z4, c='b', marker='.',label='MBS moves to next best location')
    plt.xlabel('Network Run Time (slot)')
    plt.ylabel('Sum Rate (Mbps)')
    plt.legend()
    
    
    # font = {'family' : 'sans',
        # 'size'   : 14}	
    # plt.rc('font', **font)
    # fig = plt.figure(2)
    # plt.plot(x_axis_all_grid, z5, c='b',label='MBS moves to all grid locations')
    # plt.xlabel('Network Run Time (slot)')
    # plt.ylabel('Sum Rate(Mbps)')
    # #ax.set_zlabel('Rate in Mbps')
    # #ax.set_title('Fixed Mobile Base Stations)')
    # plt.legend()
    plt.show()
