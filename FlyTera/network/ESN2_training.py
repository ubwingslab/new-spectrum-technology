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

import netcfg
import net_ntwk
import net_name, net_channel
#import ESN1_training
import unittest
from pyESN import ESN
from matplotlib import pyplot as pp
import threading 
import random
import simpy, numpy as np




def data_prep(object,index):
    data_esn2 = object.reinforcement_final_data
    #print(data_esn2)
    #print(data_esn2.shape)
    #print(bs_obj.best_loc_index)
    #print(data_esn2[:,10])# = bs_obj.best_loc_index[i]
    #print(data_esn2)
    data_esn2[:,3*netcfg.num_lte_bs_mobile+1] = object.best_loc_index
    #print(data_esn2)
    object.reinforcement_final_data = data_esn2
    #print(object.reinforcement_final_data)
    #print(data_esn2)
    esn2_training(data_esn2,index)   
    
def esn2_training(data,index2):
    #print('a',data)
    N = np.size(data,0)
    #print(N)
    rng = np.random.RandomState(42) 
    traintest_cutoff = int(np.ceil(0.8*N))
    data_index = data[:,3*netcfg.num_lte_bs_mobile+1]
    #print(np.transpose(np.array([data_index])))
    #print('a',data_index)
    data_index_max = max(data_index)
    data_index = data_index/data_index_max/2
    data_index = np.transpose(np.array([data_index]))
    #print(data_index)
    train_data, train_data_index = data[:traintest_cutoff], data_index[:traintest_cutoff]
    test_data, test_data_index = data[traintest_cutoff:], data_index[traintest_cutoff:]
    #print(test_data)
    col_mbs = 1 + 3*netcfg.num_lte_bs_mobile +1
    zeros = np.zeros(col_mbs)
    #print('zeros', zeros)
    ones = np.ones(col_mbs)
    
    esn = ESN(n_inputs=col_mbs,
              n_outputs=1,
              n_reservoir=14,
              spectral_radius=0.25,
              sparsity=0.25,
              noise=0.001,
              input_shift = zeros,
              input_scaling = ones,
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
     
    print('----------------------------------------------------------------')
    print ('esn {}'.format(index2+1))	
    print('----------------------------------------------------------------')	 
     
    print ('n_inputs=', esn.n_inputs)
    print ('n_outputs=', esn.n_outputs)
    print ('n_reservoir=', esn.n_reservoir)
    print ('spectral radius=', esn.spectral_radius)
    print ('sparsity=', esn.sparsity)
    print ('noise=', esn.noise)
    print ('input_shift=', esn.input_shift)
    print ('input_scaling=', esn.input_scaling)
    print ('teacher_forcing=', esn.teacher_forcing)
    # print ('feedback_scaling=' , esn1.feedback_scaling)
    print ('teacher_scaling=', esn.teacher_scaling)
    print ('teacher_shift=', esn.teacher_shift)
    print ('out_activation=', esn.out_activation)
    print ('inverse_out=', esn.inverse_out_activation)
    print ('random_state=', esn.random_state)
    print ('silent=', esn.silent)
    
    
    pred_train = esn.fit(train_data, train_data_index)
    pred_test = esn.predict(test_data)
    #print('b',pred_test*2*data_index_max)
    predicted_index = pred_test*2*data_index_max
    #print(predicted_index)
    pp.figure(2)
    axis = (netcfg.num_lte_bs_mobile * 100) + 10 + (index2 + 1)
    pp.subplot(axis)
    #pp.title('MBS {}'.format (index2+1))
    #pp.title('ESN Performance for Predicting Next Best Location Index')
    pp.xlabel('Number of iterations')
    pp.ylabel('Next Location Index Value')
    pp.ylim(0,400)
    #pp.plot(range(len(test_data)), test_data_index*2*data_index_max, range(len(pred_test)), pred_test*2*data_index_max)
    pp.plot(range(len(test_data_index)), test_data_index*2*data_index_max, c='r', marker ='o',label='Exhaustive Search')
    pp.plot(range(len(test_data_index)), predicted_index, c='g', linestyle='--',label='ESN-Opt')
    pp.xlabel('Network Run Time (slot)')
    pp.ylabel('Location Index')
    pp.grid(True)
    pp.legend()