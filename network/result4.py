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
import result1, result2, result3, result6, result7

def plots(nt_obj):
    z2_list = []
    z3_list = []
    z4_list = []
    z5_list = []
    z6_list = []
    for i in range(netcfg.average_iteration_number):
        print(i)
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
            sum_rate = 0 
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
                    sum_rate = sum_rate + rate_user
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
        z2 = result6.plots(nt_obj)
        #print('a',sum(z2)/netcfg.plot_iteration_number)
        z2_list.append(sum(z2)/netcfg.plot_iteration_number)
        z3 = result2.plots(nt_obj)
        #print('b',sum(z3)/netcfg.plot_iteration_number)
        z3_list.append(sum(z3)/netcfg.plot_iteration_number)
        z4 = result3.plots(nt_obj)
        #print('c',sum(z4)/netcfg.plot_iteration_number)
        z4_list.append(sum(z4)/netcfg.plot_iteration_number)
        print('-------------------------------------------------------')
        #z5 = result6.plots(nt_obj)
        #z5_list.append(sum(z5)/netcfg.plot_iteration_number)
        z6 = result7.plots(nt_obj)
        z6_list.append(sum(z6)/netcfg.plot_iteration_number)
        #print('d',z2_list,'...',z3_list,'...',z4_list)
    #print('aa',sum(z2_list)/10)
    #print('Fixed', sum(z2_list)/netcfg.average_iteration_number)
    #print('Random Movement',sum(z3_list)/netcfg.average_iteration_number)
    #print('Best Location',sum(z4_list)/netcfg.average_iteration_number)
    print('Mobile',sum(z4_list)/netcfg.average_iteration_number)
    
    #print('Static',sum(z5_list)/netcfg.average_iteration_number)
    print('static', sum(z6_list)/netcfg.average_iteration_number)
    exit()
    x_axis = list(range(0,netcfg.plot_iteration_number))
    #plt.plot(x_axis, z1, c='r', marker='o',linestyle='-',label='Rate for users with fixed MBS ')
    plt.plot(x_axis, z2, c='b', marker='o',linestyle='--',label='Rate for all users served with one moving MBS')
    plt.plot(x_axis, z3, c='g', marker='o',linestyle='-.',label='Rate for all users served when all MBS moves randomly')
    plt.plot(x_axis, z4, c='k', marker='o',linestyle=':',label='Rate for all users when all MBS moves to next best location')
    plt.xlabel('Number of Iterations')
    plt.ylabel('Rate in Mbps')
    #ax.set_zlabel('Rate in Mbps')
    #ax.set_title('Fixed Mobile Base Stations)')
    plt.legend()
    plt.show()
