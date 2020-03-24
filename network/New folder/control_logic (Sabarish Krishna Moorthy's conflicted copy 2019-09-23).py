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

import net_ntwk
import net_name, net_channel

# network configuration
import netcfg

# discrete simulations
import simpy, numpy as np
import random
import sys, os
os.system('cls')

import random
import ESN1_training

def ctl_operation(env, nt):
    '''
    Move the MBS to a new grid location 
    '''
    iter=1
    while True:
        print('Iteration Number',iter)
        #print('...')
        data_prediction_old = np.array([1])
        data_prediction_new = np.array([1])
        utility = 0
        for bs in nt.list_lte_bs_mobile:
            #print(bs)
            bs_obj = nt.get_netelmt(bs)
            x_c = bs_obj.coord_x
            y_c = bs_obj.coord_y
            z_c = bs_obj.coord_z
            esn = bs_obj.esn
            #print(esn)
            #print('old x',x_c)
            #print('old y',y_c)
            #print('old z',z_c)
            z_coord = 50
            x_coord = nt.grid_x_coord
            y_coord = nt.grid_y_coord
            x_c_new = random.choice(x_coord)
            y_c_new = random.choice(y_coord)
            z_c_new = z_coord
            x_idx = x_coord.index(x_c_new)
            y_idx = y_coord.index(y_c_new)
            #print('x index',x_idx)
            #print('y index',y_idx)
            #print('new x',x_c_new)
            #print('new y',y_c_new)
            #print('new z',z_coord)
            bs_obj.coord_x = x_c_new
            bs_obj.coord_y = y_c_new
            bs_obj.coord_z = z_coord
            data_prediction_old = np.hstack((data_prediction_old, x_c))
            data_prediction_old = np.hstack((data_prediction_old, y_c))
            data_prediction_old = np.hstack((data_prediction_old, z_c))
            data_prediction_new = np.hstack((data_prediction_new, x_c_new))
            data_prediction_new = np.hstack((data_prediction_new, y_c_new))
            data_prediction_new = np.hstack((data_prediction_new, z_c_new))

        data_prediction_old = np.hstack((data_prediction_old, utility))
        data_prediction_new = np.hstack((data_prediction_new, utility))
        print('dpo',data_prediction_old)
        print('dpn',data_prediction_new)
        xxx = data_prediction_new
        yyy = data_prediction_new
        z = 50

        length = len(x_coord)
        remove_array = np.array([])
        data_array = np.array([])
        final_data = np.array([])
        for num in range(netcfg.num_lte_bs_mobile):
            #print('...........................................')
            #print(num)
            #print('...........................................')
            xyz_coord = np.array([1])
            for i in range(length):
            
                current = data_prediction_new[num*3+1:num*3+3+1]
                #print(current)
                #print(num)
                #print(length)
                j = i+num
                #print(j)
                if j<length:
                    #print(j)
                    x = x_coord[j]
                    y = y_coord[j]
                    xy = np.hstack((x,y))
                    xyz = np.hstack((xy,z))
                    if num == 0 and i == 0:
                        data_array = np.hstack((data_array,xyz))
                    else:
                        data_array = np.vstack((data_array,xyz))
                    if (xyz == current).all():
                        #print(num,'Removed the current location coord',xyz)
                        if num == 0:
                            remove_array = np.hstack((remove_array,xyz))
                        else:
                            remove_array = np.vstack((remove_array,xyz))
                        #print(remove_array)
                    else:  
                        xyz = xyz
                        #print(xyz)
                        

                else:
                    #print('j',j)
                    j = j - length
                    #print('j',j)
                    x = x_coord[j]
                    y = y_coord[j]
                    xy = np.hstack((x,y))
                    xyz = np.hstack((xy,z))
                    if num == 0 and i == 0:
                        data_array = np.hstack((data_array,xyz))
                    else:
                        data_array = np.vstack((data_array,xyz))
                    if (xyz== current).all():
                        print(num,'Removed the current location coord',xyz)
                        if num == 0:
                            remove_array = np.hstack((remove_array,xyz))
                        else:
                            remove_array = np.vstack((remove_array,xyz))
                        #print(remove_array)
                    else:
                        xyz = xyz
                        #print(num,xyz)
                        
        #print('remove','\n',remove_array)
        #print('rem shape','\n',remove_array.shape)
        #print('data','\n',data_array)
        #print('data shape','\n',data_array.shape)
        data_needed = data_array[0:length]
        #print('data needed','\n',data_needed)
        #print('data needed shape','\n',data_needed.shape)
        size_remove = np.size(remove_array,0)
        size_data_needed = np.size(data_needed,0)
        #print('size remove','\n',size_remove)
        #print('size data','\n',size_data_needed)  
        remove_index = []
        for r in range(size_remove):
            for d in range(size_data_needed):
                if (remove_array[r] == data_needed[d]).all():
                    #print(d)
                    remove_index.append(d)
        #print(remove_index)
        data_needed = np.delete(data_needed,remove_index,0)
        #print(data_needed)
        #print(data_needed.shape)
        dns = np.size(data_needed,0)
        #print(dns)
        for bs in range(netcfg.num_lte_bs_mobile):
            print('............................................................................')
            print(bs)
            print('............................................................................')
            for dn in range(dns):
                change = data_needed[dn]
                #print('change',change)
                #print('dpn',data_prediction_new)
                #print('dpnn',data_prediction_new[1:4])
                yyy[bs*netcfg.num_lte_bs_mobile+1:bs*netcfg.num_lte_bs_mobile+4] = change
                print('dpn after change',yyy)
                                
            
            
        exit(0)
        iter+=1
        
        yield env.timeout(1)
    