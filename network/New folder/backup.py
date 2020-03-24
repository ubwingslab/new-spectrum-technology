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

        data_prediction_old = np.hstack((data_prediction_old, 0))
        data_prediction_new = np.hstack((data_prediction_new, 0))
        print(data_prediction_new)
        
        for bs in nt.list_lte_bs_mobile:
            #print(data_prediction_new)
            bs_obj = nt.get_netelmt(bs)
            #print('data 1',data_prediction_new)
            idx = nt.list_lte_bs.index(bs)
            idx = idx - netcfg.num_lte_bs
            #print(idx)
            a = data_prediction_new[idx*3+1:(idx+1)*3+1] 
            #print('idx',idx,'data',a)
            #exit(0)
            x_coord = nt.grid_x_coord
            y_coord = nt.grid_y_coord
            z = 50
            utility = 0
            length = len(x_coord)
            for i in range(length):
                
                xyz_coord = np.array([1])
                for num in range(netcfg.num_lte_bs_mobile):
                    #print(i)
                    #print(length)
                    j = i+num
                    #print(j)
                    if j<length:
                        #print(j)
                        x = x_coord[j]
                        y = y_coord[j]
                        xy = np.hstack((x,y))
                        xyz = np.hstack((xy,z))
                        #xyz_coord = np.hstack((xyz_coord,xyz))
                        #print('a',xyz_coord)
                    else:
                        #print('j',j)
                        j = j - length
                        #print('j',j)
                        x = x_coord[j]
                        y = y_coord[j]
                        xy = np.hstack((x,y))
                        xyz = np.hstack((xy,z))
                        #xyz_coord = np.hstack((xyz_coord,xyz))
                        #print('b',xyz_coord)

                    if num == 0:
                        #print(xyz_coord)
                        xyz = np.hstack((1,xyz))
                        data_xyz = xyz
                        #print(data_xyz)
                    else:
                        data_xyz = np.hstack((data_xyz,xyz))
                        #print(data_xyz)
                
                
                data_xyz = np.hstack((data_xyz,utility))
                #print(data_xyz)
                #compare = data_xyz[idx+1*3+1:(idx+1+1)*3+1]
                
                
                #print('i-',i,'...','data 2-',compare)
                # if np.array_equal(a, compare):
                   # print('a',data_xyz,'\n')

                    
                #else:
                    #print('b',data_xyz)
            #exit(0)

        iter+=1
        
        yield env.timeout(1)
    