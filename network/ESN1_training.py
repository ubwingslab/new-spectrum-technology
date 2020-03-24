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

import numpy as np
import netcfg
import net_ntwk
import net_name, net_channel
#import ESN1_training
import unittest
from pyESN import ESN
from matplotlib import pyplot as pp
import threading 
import random


def get_data_tick(tick_number, num_bs, coord, rate):
    '''Get data for each tick'''
    #print('a',num_bs)
    #print('b',coord)
    #print('c',rate)
    data_coord = coord[tick_number*num_bs: (tick_number+1)*num_bs,  :]
    data_rate = rate[tick_number*num_bs: (tick_number+1)*num_bs,  :]
    #print('daco',data_coord)
    #print('dara',data_rate)
    # exit(0)
    return data_coord, data_rate


def append_training_data(number_bs, train_data_coord, train_data_rate):
    '''Append Training data for each tick'''
    #print(number_bs)
    #print(train_data_coord)
    #print(train_data_rate)
    training_data_bs = np.array([1])
    training_data_mbs = np.array([1])
    #np.set_printoptions(suppress=True)
    rate = np.array([])
    i=0
 
    for i in range(0, number_bs):
        #print(train_data_coord)
        #print(train_data_coord[i,:])
        #print(train_data_rate)
        #print(train_data_rate[i,:])
        #print(train_data_coord[i,:])
        training_data_bs = np.hstack((training_data_bs,train_data_coord[i,:]))
        #print('aaa',train_data_coord[i,:])
        #print('yyy',training_data_bs)
        rate = np.hstack((rate,train_data_rate[i,:]))
    #print('yyy',training_data_bs)
    #print('zzz',rate)
    #print(sum_num)
    

    training_data_bs = np.hstack((training_data_bs,rate))
    #print(training_data_bs)
    num = number_bs - netcfg.num_lte_bs
    #print(num)
    #print('fff',training_data_bs)
    #exit(0)
    #print('tdmbs',training_data_bs)
    coord_mbs =training_data_bs[1+ (3*netcfg.num_lte_bs): 1+ (3*netcfg.num_lte_bs)+netcfg.num_lte_bs_mobile*3+netcfg.num_lte_bs+netcfg.num_lte_bs_mobile]
    #print('cmbs',coord_mbs)
    training_data_mbs = np.hstack((training_data_mbs, coord_mbs))
    # user_mbs = training_data_bs[num + num*number_bs: num*netcfg.num_lte_bs + num*number_bs]
    # print(user_mbs)
    # training_data_mbs = np.hstack((training_data_mbs, user_mbs))
    #training_data_mbs = np.hstack((training_data_mbs, np.sum(user_mbs)))
    #print('xxx',training_data_mbs)
    #exit(0)
    #print(num,'\n')
    #exit(0)
        
    return training_data_mbs
    
def esn_training(index, data, ntwk_obj):
    '''ESN Training for each MBS'''
    #print(index)
    num = netcfg.num_lte_bs_mobile - netcfg.num_lte_bs
    
    #print(num)
    index = index - (netcfg.num_lte_bs_mobile - num)
    #print(index)
    col_mbs = 3 * netcfg.num_lte_bs_mobile + 1 + index
    #print('a',col_mbs)
    #print('all data',data)

    data_rate = data[:,col_mbs :col_mbs+1]
    #print('data_rate',data_rate)
    
    data = data[:,0:col_mbs - index]
    #print('intermediate',data)
    
    data = np.hstack((data,data_rate))
    
    #print('data',data)
    
    coord_x = ntwk_obj.grid_x_coord
    #print(coord_x,'\n')
    coord_y = ntwk_obj.grid_y_coord
    #print(coord_y,'\n')
    
    #data_rate = np.transpose(data_rate)
    #print(data_rate)
    #print('data',data)
    data_rate = data[:,col_mbs-index]
    #print(data_rate)
    data_rate_max = max(data_rate)
    #print('max',data_rate_max)
    #exit(0)
    ntwk_obj.max_data = data_rate_max
    #print(ntwk_obj.max_data)
    data_rate = data_rate/data_rate_max/2
    #print(data_rate)
    data_rate = np.transpose(np.array([data_rate]))
    #print('data rate',data_rate)

    N=netcfg.total_tick
    
    rng = np.random.RandomState(42)   
    traintest_cutoff = int(np.ceil(0.8*N))
    train_data, train_data_rate = data[:traintest_cutoff], data_rate[:traintest_cutoff]
    #print('train data',train_data)
    #print('train data rate',train_data_rate)
    #print('train data',train_data.shape)
    #print('train data rate',train_data_rate.shape)
    test_data, test_data_rate = data[traintest_cutoff:], data_rate[traintest_cutoff:]
    #print('test data',test_data)
    #print('test data rate',test_data_rate)
    p1 = sum(test_data_rate)
    print('p1', p1)
    #print('test data',test_data.shape)
    #print('test data rate',test_data_rate.shape)
    col_mbs = col_mbs + 1 - index
    zeros_row = np.zeros(col_mbs)
    #print('zeros', zeros)
    ones_row = np.ones(col_mbs)
    #print('ones', ones)
    #print(col_mbs)
    # create an echo state network
    esn = ESN(n_inputs=col_mbs,
              n_outputs=1,
              n_reservoir=21,
              spectral_radius=0.25,
              sparsity=0.25,
              noise=0.001,
              input_shift = zeros_row,
              input_scaling = ones_row,
              #input_scaling=[1, 1],
              teacher_scaling=0.5,
              #teacher_scaling=1,
              teacher_shift=-0,
              #teacher_shift=0,
              # teacher_scaling = None,
              # teacher_shift = None,
              out_activation=np.tanh,
              inverse_out_activation=np.arctanh,
              random_state=rng,
              silent=False)
     
    # print('----------------------------------------------------------------')
    # print ('esn {}'.format(index+1))	
    # print('----------------------------------------------------------------')	 
     
    # print ('n_inputs=', esn.n_inputs)
    # print ('n_outputs=', esn.n_outputs)
    # print ('n_reservoir=', esn.n_reservoir)
    # print ('spectral radius=', esn.spectral_radius)
    # print ('sparsity=', esn.sparsity)
    # print ('noise=', esn.noise)
    # print ('input_shift=', esn.input_shift)
    # print ('input_scaling=', esn.input_scaling)
    # print ('teacher_forcing=', esn.teacher_forcing)
    # # print ('feedback_scaling=' , esn1.feedback_scaling)
    # print ('teacher_scaling=', esn.teacher_scaling)
    # print ('teacher_shift=', esn.teacher_shift)
    # print ('out_activation=', esn.out_activation)
    # print ('inverse_out=', esn.inverse_out_activation)
    # print ('random_state=', esn.random_state)
    # print ('silent=', esn.silent)

    #print('1')
    # fitting  
    
    pred_train = esn.fit(train_data, train_data_rate)
    
    #print(pred_train)
    #print('2')
    # prediction
    #print(data.shape)
    
    
    pred_test = esn.predict(test_data)
    
    
    # print('data rate',data_rate)
    # print('pred test',pred_test,'\n')
    # print('3')
    pp.figure(1)
    font = {'family' : 'sans',
        'size'   : 16}	
    pp.rc('font', **font)
    axis = (netcfg.num_lte_bs_mobile * 100) + 10 + (index + 1)
    pp.subplot(axis)
    #pp.title('MBS {}'.format (index+1))
    #pp.title('ESN Performance for Rate Prediction')
    pp.xlabel('Network Run Time (slot)')
    pp.ylabel('FBS Rate (Mbps)') 
    # print(data_rate)
    # print(pred_test)

    pp.plot(range(len(test_data_rate)), test_data_rate*2*data_rate_max,c='r',marker = 'o', label='Measured Rate')
    pp.plot(range(len(test_data_rate)), pred_test*2*data_rate_max,c='g', linestyle='--',label='ESN-Pdt Prediction')
    pp.legend()
    pp.grid(True)
    return esn
    
def data_train(data_coord, data_rate):
    #print('dc',data_coord)
    #print('dr',data_rate)
    num_bs = netcfg.num_lte_bs + netcfg.num_lte_bs_mobile
    #print(num_bs)
    for i in range(int(netcfg.total_tick)):
        data_1,data_2 = get_data_tick(i, num_bs, data_coord, data_rate)
        #print('d1',data_1)
        #print('d2',data_2)
        #print('nb',num_bs)
        training_data_mbs = append_training_data(num_bs, data_1, data_2)
        #training_data_list.append(training_data)
        #print('tdm',training_data_mbs)
        # exit(0)
        #print(training_data_mbs,'\n')
        #print(data_mbs_1_curr_row,'\n')
        #print(data_mbs_1)
        # a= np.array([data_mbs_1])
        # print(a.shape)
        # b = np.array([data_mbs_1_curr_row])
        # print(b.shape)
        # data_mbs_1 = np.vstack((a,b))
        # print(data_mbs_1)
        
        col_mbs = (3 * netcfg.num_lte_bs_mobile) + 1 # total number of columns for all MBS(coordinate values)
        #print(col_mbs)
        #print('a',training_data_mbs)
        #print('b',training_data_mbs[0 : col_mbs])
        #print('ab',training_data_mbs[col_mbs + netcfg.num_lte_bs : (col_mbs + netcfg.num_lte_bs_mobile)+ netcfg.num_lte_bs])
        data_mbs_curr_row = np.hstack((training_data_mbs[0 : col_mbs],training_data_mbs[col_mbs + netcfg.num_lte_bs : (col_mbs + netcfg.num_lte_bs_mobile)+ netcfg.num_lte_bs]))  #data for all 3 MBS
        #print('xxxxx',data_mbs_curr_row)
        if i == 0:
            data_mbs = data_mbs_curr_row
            #print(data_mbs_1)
        else:
            data_mbs = np.vstack((data_mbs,data_mbs_curr_row))
        #print('c',training_data_mbs)   
    #exit(0)
    #print('dmbs',data_mbs)
    return data_mbs

    #print(training_data_mbs)        
    #print(data_mbs,'\n')
    #exit(0)




    
    

   
