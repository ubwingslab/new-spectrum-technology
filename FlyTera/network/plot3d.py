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

def plots(nt_obj):
    x_coord = nt_obj.grid_x_coord
    #print(x_coord)
    y_coord = nt_obj.grid_y_coord
    #print(y_coord)
    
    list_bs = nt_obj.list_lte_bs
    #print(list_bs)
    #exit()
    bs_obj = nt_obj.get_netelmt(list_bs[0])
    bs_m_obj = nt_obj.get_netelmt(list_bs[2])
    z_coord = 50
    #print(z_coord)
    rate_list_for_plot_gbs =  []
    rate_list_for_plot_mbs = []
    for i in range(len(x_coord)):
        #print(i)
        rate_list_mbs = []
        rate_list_gbs = []
        #print('mbs user',bs_obj.served_user)
        for serv_usr in bs_obj.served_user:
            serv_usr_obj = nt_obj.get_netelmt(serv_usr) 
            sinr = serv_usr_obj.sinr
            if serv_usr_obj.oper_freq == 'micro':
                rate_mbs = netcfg.micro_bandwidth * np.log2(1 + sinr)
            elif serv_usr_obj.oper_freq == 'milli': 
                rate_mbs = netcfg.milli_bandwidth * np.log2(1 + sinr)
            else:
                rate_mbs = netcfg.tera_bandwidth * np.log2(1 + sinr)
            rate_list_mbs.append(rate_mbs)
            #print('a',rate_list_mbs)
        #print('bs user',bs_g_obj.served_user)
        for serv_usr in bs_m_obj.served_user:
            serv_usr_obj = nt_obj.get_netelmt(serv_usr) 
            sinr = serv_usr_obj.sinr
            if serv_usr_obj.oper_freq == 'micro':
                rate_gbs = netcfg.micro_bandwidth * np.log2(1 + sinr)
            elif serv_usr_obj.oper_freq == 'milli': 
                rate_gbs = netcfg.milli_bandwidth * np.log2(1 + sinr)
            else:
                rate_gbs = netcfg.tera_bandwidth * np.log2(1 + sinr)
            rate_list_gbs.append(rate_gbs)
            #print('b',rate_list_gbs)
        #print('a',rate_list)
        rate_mbs = sum(rate_list_mbs)
        rate_gbs = sum(rate_list_gbs)
        #print('c',rate_mbs)
        #print('d',rate_gbs)
        rate_list_for_plot_gbs.append(rate_gbs)
        rate_list_for_plot_mbs.append(rate_mbs)
        current_coord = bs_obj.get_coord()
        new_coord = current_coord
        #print('a',new_coord)
        x = x_coord[i]
        y = y_coord[i]
        z = z_coord
        new_coord['x'] = x
        new_coord['y'] = y
        new_coord['z'] = z  
        bs_obj.set_coord(new_coord)
        #print('b',new_coord)
        nt_obj.ini_dist()
        nt_obj.update_association()
        nt.update_association_mbs_bs_link()
        nt_obj.updt_band_association()
        #print('c',bs_obj.served_user)
        for user in nt_obj.get_node_list(net_name.lte_ue):
            #print('1')
            user_obj = nt_obj.get_netelmt(user)
            #print('2')
            user_obj.blk_detection()
            #print('3')
            user_obj.set_noise()
            #print('4')
            user_obj.sinr_calc()
            #print('5')
    #print(x_coord)
    #print(y_coord)
    #print(z_coord)
    #print(rate_list_for_plot)
    mpl.rcParams['legend.fontsize'] = 10
    fig = plt.figure(1)
    ax = fig.add_subplot(111, projection='3d')
    
    x =x_coord
    y =y_coord
    z1 = rate_list_for_plot_gbs
    z2 = rate_list_for_plot_mbs
    z3 = np.add(z1,z2)
    ax.plot(x, y, z1, 'r',marker = 'o', label='Rate for GBS')
    #ax.plot(x,y,z1, color='r')
    ax.plot(x, y, z2, 'b',marker = 'o', label='Rate for MBS')
    #ax.plot(x,y,z2, color='b')
    ax.plot(x, y, z3, 'g',marker = '^', label='Sum Rate')
    #ax.plot(x,y,z3, color='g')
    ax.set_xlabel('X Coord')
    ax.set_ylabel('Y Coord')
    ax.set_zlabel('Rate in Mbps')
    ax.legend()
    # fig = plt.figure(2)
    # plt.plot(x,z1,label='Rate for GBS')
    # plt.plot(x,z2,label='Rate for MBS')
    # plt.plot(x,z3,label='Sum Rate')
    # plt.xlabel('Index')
    # plt.ylabel('Rate')
    # plt.legend()
    plt.show()

    
        
    