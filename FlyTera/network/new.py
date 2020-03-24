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
        
        #print('xc',x_coord)
        #print('yc',y_coord)
        
        #print(netcfg.num_lte_bs_mobile)
        #for h in range(netcfg.num_lte_bs_mobile):
         #  print(h)
            
        z = 50

        length = len(x_coord)
        data = []
        for num in range(netcfg.num_lte_bs_mobile):
            print(num)
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
                    if (xyz == current).all():
                        print(num,'Removed the current location coord',xyz)
                    else:  
                        xyz = xyz
                        #print(num,xyz)
                        data = np.hstack((data,xyz))
                        
                    
                    #print(data)
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
                    if (xyz== current).all():
                        print(num,'Removed the current location coord',xyz)
                    else:
                        #xyz = xyz
                        #print(num,xyz)
                        data = np.hstack((data,xyz))
                    #print(data)
        
        idx_list = []
        for bs in nt.list_lte_bs_mobile:
            idx = nt.list_lte_bs_mobile.index(bs)
            idx_list.append(idx)
        #print(idx_list)
        for bs in nt.list_lte_bs_mobile:  
            print('....................................................')
            print(bs)
            print('....................................................')
            idx = nt.list_lte_bs_mobile.index(bs)
            lendat = len(data)
            #print(lendat)
            lendat = int(lendat/netcfg.num_lte_bs_mobile)
            #print(lendat)
            for ld in range(lendat): 
                #print(ld)
                #print(bs)
                idx = nt.list_lte_bs_mobile.index(bs)
                #print(idx)
                #print(data)
                #print(len(data))
                bs_obj = nt.get_netelmt(bs)
                x_c = bs_obj.coord_x
                y_c = bs_obj.coord_y
                z_c = bs_obj.coord_z
                esn = bs_obj.esn
                #print('old x:',x_c,'...','old y:',y_c,'...','old z:',z_c)
                #print('old dict',bs_obj.__dict__)
                #print(data[0:3])
                x_c_new_coord = data[(2*ld)+ld+0]
                y_c_new_coord = data[(2*ld)+ld+1]
                z_c_new_coord = data[(2*ld)+ld+2]
                xyznew = np.hstack((x_c_new_coord,y_c_new_coord))
                xyznew = np.hstack((xyznew,z_c_new_coord))
                #print(data_prediction_new)
                #print(xyznew)
                if (xyznew == data_prediction_new[3*idx+1:3*idx+4]).all():
                    print('a',ld,bs)
                    #print(ld)
                    #print(idx)
                    print('skipped', xyznew)#continue
                
                for idx1 in idx_list:
                    
                    if idx1 != idx:
                        if (xyznew == data_prediction_new[3*idx+1:3*idx+4]).all():
                            print(idx1,nt.list_lte_bs_mobile[idx1])
                            #print(ld)
                            #print(idx)
                            print('skipped', xyznew)#continue
                        else:
                            bs_obj.coord_x = x_c_new_coord
                            bs_obj.coord_y = y_c_new_coord
                            bs_obj.coord_z = z_c_new_coord
                            #print('new x:',bs_obj.coord_x,'...','new y:',bs_obj.coord_y,'...','new z:',bs_obj.coord_z)
                            #print('new dict',bs_obj.__dict__)
   
            print('xxxx')
        exit(0)
        iter+=1
        
        yield env.timeout(1)
    