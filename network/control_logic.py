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

import time

from ESN1_training import esn_training

def ctl_operation(env, nt):
    '''
    Move the MBS to a new grid location 
    '''
    iter=1
    execution_time_total = 0
    
    print('---------------------------------------------------------------')
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
            #print(bs_obj.coord_x,bs_obj.coord_y,bs_obj.coord_z,bs_obj.served_user)
            data_prediction_old = np.hstack((data_prediction_old, x_c))
            data_prediction_old = np.hstack((data_prediction_old, y_c))
            data_prediction_old = np.hstack((data_prediction_old, z_c))
            data_prediction_new = np.hstack((data_prediction_new, x_c_new))
            data_prediction_new = np.hstack((data_prediction_new, y_c_new))
            data_prediction_new = np.hstack((data_prediction_new, z_c_new))
            #print(bs_obj.name,bs_obj.coord_x,bs_obj.coord_y,bs_obj.coord_z)
        #print('dpo',data_prediction_old)
        #print('dpn',data_prediction_new)
        data_prediction_new = data_prediction_old
        #print('dpo',np.hstack((data_prediction_old,utility)))
        #print('dpn',np.hstack((data_prediction_new,utility)))
        #print('c',nds,'-',data_prediction_new,ue_obj.sinr)
        #print(bs_obj.name,bs_obj.coord_x,bs_obj.coord_y,bs_obj.coord_z,bs_obj.served_user)
        #print('\n')
        #data_current_mbs_location = np.hstack((data_prediction_new,sinr_column))
        #data_prediction_new = np.hstack((data_prediction_new,a))
        #print(data_prediction_new)

            
        z = 50
        length = len(x_coord)
        remove_array = np.array([])
        data_array = np.array([])
        for num in range(netcfg.num_lte_bs_mobile):
            # print('...........................................')
            # print(num)
            # print('...........................................')
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
                        #print(num,'Removed the current location coord',xyz)
                        if num == 0:
                            remove_array = np.hstack((remove_array,xyz))
                        else:
                            remove_array = np.vstack((remove_array,xyz))
                        #print(remove_array)
                    else:
                        xyz = xyz
                        #print(num,xyz)
                        
        #print('remove',remove_array)
        #print('rem shape',remove_array.shape)
        # print('data',data_array)
        # print('data shape',data_array.shape)
        # print('size remove',np.size(remove_array,0))
        # print('size data',np.size(data_array,0))
        #print(length)
        needed_data = data_array[0:length]
        #print(needed_data)
        #print(needed_data.shape)
        rem_idx_list = []
        for ril in range(np.size(remove_array,0)):
            for da in range(np.size(needed_data,0)):
                if (remove_array[ril] == needed_data[da]).all():
                    rem_idx_list.append(da)
        #print(rem_idx_list)  
        needed_data = data_array[0:length]
        data_needed = needed_data.copy()
        needed_data = np.delete(needed_data,rem_idx_list,0)
        #print(needed_data)
        #print(needed_data.shape)
        data_before_change = np.array([])
        for bs in range(netcfg.num_lte_bs_mobile):
            
            abc = data_prediction_new[bs*3+1: bs*3+4]
            if bs == 0:
                data_before_change = np.hstack((data_before_change,abc))
            else:
                data_before_change = np.vstack((data_before_change,abc))
            #print('a',data_before_change)
         
        max_loc_for_mbs = np.array([])
        data_pred = np.array([1])
        indices_list = []
        iesn = 0
       
        for bs in range(netcfg.num_lte_bs_mobile):
            #print(bs)
            
            curr_coordinates = np.array([])
            data_for_esn = np.array([])
            bs_name = nt.list_lte_bs_mobile[bs]
            #print(bs_name)
            bs_obj = nt.get_netelmt(bs_name)
            #print('a',bs_obj.served_user)
            #print('before change',data_prediction_new)
            #print('a',bs_obj.served_user)#,'...',bs_obj.coord_y,'...',bs_obj.coord_z)
            current_coord = bs_obj.get_coord()
            new_coord = current_coord
           
            curr_x = current_coord['x']
            curr_y = current_coord['y']
            curr_z = 50
            curr_coordinates = np.hstack((curr_coordinates,curr_x))
            curr_coordinates = np.hstack((curr_coordinates,curr_y))
            curr_coordinates = np.hstack((curr_coordinates,curr_z))
            for nds in range(np.size(needed_data,0)):
                data_prediction_new[bs*3+1: bs*3+4] = needed_data[nds]
                #print(nds,'-',np.hstack((data_prediction_new,utility)))
                if nds == 0:
                    data_for_esn = np.hstack((data_for_esn,np.hstack((data_prediction_new,utility)))) 
                else:
                    data_for_esn = np.vstack((data_for_esn,np.hstack((data_prediction_new,utility))))
            #print(bs_name)       
            #print(data_for_esn,'\n')
            start_time = time.time()
            #print('start time', start_time)
            prediction_data_esn = esn.predict(data_for_esn)
            end_time = time.time()
            #print('end time', end_time)
            execution_time = end_time - start_time
         
            #print('execution time', "%s seconds" % execution_time)
            execution_time_total = execution_time_total + execution_time
            #print('execution time total', execution_time_total, 'seconds')
            #print(prediction_data_esn.shape)
            #print(prediction_data_esn)
            max_sinr = max(prediction_data_esn)
            #print(max_sinr)
            loction_max_value = np.where(prediction_data_esn == np.amax(prediction_data_esn))
            indices = loction_max_value[0]
            indices = indices[0]
            #print(indices)
            bs_obj.next_best_loc_index.append(indices)
            bs_obj.data_needed_array = data_needed
            #print(bs_obj.next_best_loc_index)
            indices_list = np.hstack((indices_list,indices))
            loc_for_esn = data_for_esn[loction_max_value[0]]
            #print('a',loc_for_esn)
            #print(loc_for_esn.shape)
            #print(data_for_esn.shape)
            #print('\n')
            max_loc =  loc_for_esn[0,bs*3+1: bs*3+4]
            #print('aaaa',max_loc)
            #print('b',max_loc[0])
            #print('c',max_loc[1])
            max_loc_for_mbs = np.hstack((max_loc_for_mbs,max_loc))
            location = bs_obj.reinforcement_learning_data(data_array[0:length],loc_for_esn,indices,curr_coordinates,max_sinr)
            #print('b',location)
            #print(nt.max_data)
            data_prediction_new[bs*3+1: bs*3+4] = data_before_change[bs]
            data_pred = np.hstack((data_pred,max_loc))
        data_pred = np.hstack((data_pred,0))
        data_pred = np.reshape(data_pred,(1,(3*netcfg.num_lte_bs_mobile+2)))
        #print(data_pred.shape)
        
        if iter == 1:
            data_max_sinr_locations = np.array([])
            data_max_sinr_locations = np.reshape(data_max_sinr_locations,(1,0))
            data_max_sinr_locations = np.hstack((data_max_sinr_locations,data_pred))
        else:
            data_max_sinr_locations = np.vstack((data_max_sinr_locations,data_pred))
        
        #print(data_max_sinr_locations)
        
        
        iter+=1
        if iter == (netcfg.reinforcement_total_tick+1):
            #print('---------------------------------------------------------------')
            #print(data_max_sinr_locations)
            #print(data_max_sinr_locations.shape)
            print('execution time total', execution_time_total, 'seconds')
            for bs in nt.list_lte_bs_mobile:
                 bs_obj = nt.get_netelmt(bs)
                 bs_obj.reinforcement_final_data = data_max_sinr_locations
            #print('---------------------------------------------------------------')
        #exit(0)    
        yield env.timeout(1)
        

        
    