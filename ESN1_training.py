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

import xlrd
import numpy as np
import netcfg
#import ESN1_training
import unittest
from pyESN import ESN
from matplotlib import pyplot as pp
import threading 

def get_data_tick(tick_number, number_bs, coord, rate):
    '''Get data for each tick'''
    
    data_coord = xyz_coord[tick_number*num_bs: (tick_number+1)*num_bs,  :]
    data_rate = rate[tick_number*num_bs: (tick_number+1)*num_bs,  :]
    # print(data_coord)
    # print(data_num)
    # exit(0)
    return data_coord, data_rate


def append_training_data(number_bs, train_data_coord, train_data_rate):
    '''Append Training data for each tick'''
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
        training_data_bs = np.hstack((training_data_bs,train_data_coord[i,:]))
        rate = np.hstack((rate,train_data_rate[i,:]))
    #print(sum_num)
    

    training_data_bs = np.hstack((training_data_bs,rate))
    #print(training_data_bs)
    num = number_bs - netcfg.num_lte_bs
    coord_mbs =training_data_bs[1 + num*netcfg.num_lte_bs : 1 + num*number_bs]
    #print(coord_mbs)
    training_data_mbs = np.hstack((training_data_mbs, coord_mbs))
    user_mbs = training_data_bs[num + num*number_bs: num*netcfg.num_lte_bs + num*number_bs]
    #print(user_mbs)
    training_data_mbs = np.hstack((training_data_mbs, user_mbs))
    #training_data_mbs = np.hstack((training_data_mbs, np.sum(user_mbs)))
    #print(training_data_mbs)
    #print(num,'\n')
    #exit(0)
        
    return training_data_mbs
    
def esn_training(index,data_mbs):
    '''ESN Training for each MBS'''
    
    col_mbs = 3 * netcfg.num_lte_bs_mobile + index
    data_mbs = data_mbs[:,col_mbs]    
    #print(data_rate,'\n')
    data_mbs_max = max(data_mbs)
    #print(data_mbs_1_rate_max,'\n')

    data_mbs = data_mbs/data_mbs_max/2
    #print(data_mbs_1_rate,'\n')

    data_mbs = np.transpose(np.array([data_mbs]))
    #print(data_mbs_1_rate,'\n')

    N=10000
    rng = np.random.RandomState(42)   
    traintest_cutoff = int(np.ceil(0.6 * N))
    train_data, train_data_mbs = data[:traintest_cutoff], data_mbs[:traintest_cutoff]
    test_data, test_data_mbs = data[traintest_cutoff:], data_mbs[traintest_cutoff:]
    col_mbs = col_mbs +  1 
    #print('n = ', col_mbs)
    zeros = np.zeros(col_mbs)
    #print('zeros', zeros)
    ones = np.ones(col_mbs)
    #print('ones', ones)
    #exit(0)
    # create an echo state network
    esn = ESN(n_inputs=col_mbs,
              n_outputs=1,
              n_reservoir=200,
              spectral_radius=0.25,
              sparsity=0.25,
              noise=0.001,
              input_shift = zeros,
              input_scaling = ones,
              #input_scaling=[1, 1],
              teacher_scaling=2.0,
              #teacher_scaling=1,
              teacher_shift=-0.9,
              #teacher_shift=0,
              # teacher_scaling = None,
              # teacher_shift = None,
              out_activation=np.tanh,
              inverse_out_activation=np.arctanh,
              random_state=rng,
              silent=False)
              
    print('----------------------------------------------------------------')
    print ('esn {}'.format(i+1))	
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

    #print('1')
    # fitting  
    pred_train = esn.fit(train_data, train_data_mbs)
    #print('2')
    # prediction
    pred_test = esn.predict(data)
    #print('3')
    pp.plot(range(len(data)), data_mbs, range(len(pred_test)), pred_test)
    #print('4')
    pp.title('MBS no. {}'.format (i+1))
    #print('5')
    pp.show()
    #print('6')
    
    
def data_train():
    workbook = xlrd.open_workbook('tracking_data_5.xlsx')
    worksheet = workbook.sheet_by_name('tracking_data_5')
    num_rows = worksheet.nrows - 1
    #print(worksheet.nrows)

    curr_row = 1
    x_coord = []
    while curr_row <= num_rows:
        row = worksheet.row(curr_row)
        #print(type(row))
        #print(type(row[0]))
        row_value = row[0].value
        #print ('x', row)
        x_coord.append(row_value)
        curr_row += 5
        #print(row_value)
       
    #print(np.array(x_coord),'\n')
    x_coord = np.array(x_coord)
    #print(x_coord)
    #print(np.transpose(np.array(x_coord)))
    #bb = np.transpose(x_coord)
    #print(bb)
    #print(type(bb))
    #print(x_coord)
    #print((int(worksheet.nrows/5)))
    #print(int(worksheet.nrows/5))
    #print(np.ones((1,int(worksheet.nrows/5))))
    #x_coord = np.vstack([np.ones((1,(int(worksheet.nrows/5)))), x_coord])
    x_coord = np.vstack([x_coord])

    #print(x_coord)

    x_coord = np.transpose(x_coord)
    #x_coord_t = np.transpose(x_coord_t)
    #print(x_coord_t)

    curr_row = 2
    y_coord = []
    while curr_row <= num_rows:
        row = worksheet.row(curr_row)
        row_value = row[0].value
        #print ('y', row)
        y_coord.append(row_value)
        curr_row += 5
        
    y_coord = np.array([y_coord])
    #print('y_coord::::::',y_coord,'\n \n')
    #print(np.transpose(y_coord))
    y_coord = np.vstack([y_coord])

    y_coord = np.transpose(y_coord)
    xy_coord = np.hstack([x_coord, y_coord])
    #print(xy_coord)

    curr_row = 3
    z_coord = []
    while curr_row <= num_rows:
        row = worksheet.row(curr_row)
        row_value = row[0].value
        #print ('z', row)
        z_coord.append(row_value)
        curr_row += 5
        
    z_coord = np.array([z_coord]) 
    z_coord = np.vstack([z_coord])
    z_coord = np.transpose(z_coord)
    #print(z_coord)
    xyz_coord = np.hstack([xy_coord, z_coord])
    #print(xyz_coord)
    #print('z_coord::::::',z_coord,'\n \n')
    #print(np.transpose(z_coord))

    curr_row = 4
    rate = []
    while curr_row <= num_rows:
        row = worksheet.row(curr_row)
        row_value = row[0].value
        #print ('z', row)
        rate.append(row_value)
        curr_row += 5
       
    rate = np.array([rate])
    #print(rate)
    rate = np.vstack([rate])  
    rate = np.transpose(rate)
    #print('aa',xyz_coord.shape)
    #print('bb',rate.shape)
    xyz_coord_rate = np.hstack([xyz_coord, rate])
    #print(xyz_coord_num,'\n')

    num_bs = netcfg.num_lte_bs + netcfg.num_lte_bs_mobile
    training_data_list = []
    data_mbs = np.array([])

    for i in range(int(netcfg.total_tick/1)):
        data_1,data_2 = get_data_tick(i, num_bs, xyz_coord, rate)
        training_data_mbs = append_training_data(num_bs, data_1, data_2)
        #training_data_list.append(training_data)
        # print(training_data_mbs)
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
        data_mbs_curr_row = np.hstack((training_data_mbs[0 : col_mbs],training_data_mbs[col_mbs : (col_mbs + netcfg.num_lte_bs_mobile)]))  #data for all 3 MBS
        if i == 0:
            data_mbs = data_mbs_curr_row
            #print(data_mbs_1)
        else:
            data_mbs = np.vstack((data_mbs,data_mbs_curr_row))
    #print('xxxx',data_mbs,'\n')    
    return data_mbs
    
    #print(training_data_mbs)        

    #exit(0)

    #print(netcfg.num_lte_bs_mobile)
    #exit(0)
    
# if __name__ == "__main__":
    # i = 0
    # col_mbs = 3 * netcfg.num_lte_bs_mobile + 1 
    # for i in range(netcfg.num_lte_bs_mobile): 
        # data_rate = data_mbs[:,col_mbs]    
        # #print(data_rate,'\n')
        # col_mbs = col_mbs + 1
        
        # # creating thread 
        # thread = threading.Thread(target=esn_training, args=(data_mbs,data_rate))  

        # # starting thread 1 
        # print('starting thread {}'.format(i+1))
        # thread.start() 
        
        # # wait until thread is completely executed 
        # thread.join() 
        
    # for i in range(netcfg.num_lte_bs_mobile): 
        
            
        



    
    

   
