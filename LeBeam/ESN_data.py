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

import flytera_cfg

import FlyTera

import numpy as np

import net_ntwk

import statistics 

import ESN_data_format

import matplotlib

#import beam_plot

import distribution_plot

def data_for_esn():
    #plot_ang_v_cap_diff_bai()
    #plot_ang_v_cap_diff_mob()
    #exit()
    capa_list = []
    data_angle_time = np.array([])
    data_distance = np.array([])
    beam_almt_itvl = 100
    
    for angle in range(1,11):
        flytera_cfg.data_tr_xyz = []
        flytera_cfg.data_rx_xyz = []
        flytera_cfg.data_tr_rpy = []
        flytera_cfg.data_rx_rpy = []
        print('angle',angle)
        flytera_cfg.angle = angle
        FlyTera.run_net(beam_almt_itvl) 
        flytera_cfg.sim_index = 1  
        data_list = flytera_cfg.data2 
        #print(data_list)
        distance_list = flytera_cfg.distance
        #print(distance_list)
        #print('data list', data_list)
        #print('min capacity', min(data_list))
        #print('max capacity', max(data_list))
        #print('data array', np.asarray(data_list))
        if angle == 1:
            data_angle_time = np.hstack((data_angle_time, np.asarray(data_list)))
            data_distance = np.hstack((data_distance, np.asarray(distance_list)))
        else:
            data_angle_time = np.vstack((data_angle_time, np.asarray(data_list)))
            data_distance = np.vstack((data_distance, np.asarray(distance_list)))
        print('------------------------')   
        flytera_cfg.data2 = []
        flytera_cfg.distance = []
    #exit()
    #print(data_angle_time)
   
    #print(data_distance)
    distance_data = data_distance[0]
    #print(len(distance_data))
    #exit()
    optimal_angle, op_ang_list = optimal_angle_calc(data_angle_time)
    #plot_angle_capacity(data_angle_time)
    #exit()
    distance_tr_xyz_list, distance_rx_xyz_list, distance_tr_rpy_list, distance_rx_rpy_list = distance()
    #distance_tr_xyz_list, distance_rx_xyz_list, distance_tr_rpy_list, distance_rx_rpy_list = distance(1)
    
    #print("A", len(distance_tr_xyz_list)
    #print("B", distance_rx_xyz_list)
    #print("C", distance_tr_rpy_list)
    #print("D", distance_rx_rpy_list)
    #exit()
    #print("AA", len(distance_tr_xyz_list))
    #print("BB", len(distance_rx_xyz_list))
    #print("CC", len(distance_tr_rpy_list))
    #print("DD", len(distance_rx_rpy_list))
    #distribution_plot.plots_loc(distance_tr_xyz_list)
    #distribution_plot.plots_loc(distance_rx_xyz_list)
    #distribution_plot.plots_ang(distance_tr_rpy_list)
    #distribution_plot.plots_ang(distance_rx_rpy_list)
    #exit()
    N=int(flytera_cfg.sim_tick/2)
    
    var_tr_xyz_1, var_rx_xyz_1, var_tr_rpy_1, var_rx_rpy_1 = variance_calc(distance_tr_xyz_list[0:N], distance_rx_xyz_list[0:N], distance_tr_rpy_list[0:N], distance_rx_rpy_list[0:N])
    var_tr_xyz_2, var_rx_xyz_2, var_tr_rpy_2, var_rx_rpy_2 = variance_calc(distance_tr_xyz_list[N:2*N], distance_rx_xyz_list[N:2*N], distance_tr_rpy_list[N:2*N], distance_rx_rpy_list[N:2*N])
    mean_tr_xyz_1, mean_rx_xyz_1, mean_tr_rpy_1, mean_rx_rpy_1 = mean_calc(distance_tr_xyz_list[0:N], distance_rx_xyz_list[0:N], distance_tr_rpy_list[0:N], distance_rx_rpy_list[0:N])
    mean_tr_xyz_2, mean_rx_xyz_2, mean_tr_rpy_2, mean_rx_rpy_2 = mean_calc(distance_tr_xyz_list[N:2*N], distance_rx_xyz_list[N:2*N], distance_tr_rpy_list[N:2*N], distance_rx_rpy_list[N:2*N])
    
    #print(var_tr_xyz_1, var_rx_xyz_1, var_tr_rpy_1, var_rx_rpy_1)
    #print(var_tr_xyz_2, var_rx_xyz_2, var_tr_rpy_2, var_rx_rpy_2)
    #print(mean_tr_xyz_1, mean_rx_xyz_1, mean_tr_rpy_1, mean_rx_rpy_1)
    #print(mean_tr_xyz_2, mean_rx_xyz_2, mean_tr_rpy_2, mean_rx_rpy_2)
    
    #exit()
    
    angles = ESN_data_format.esn_data_prep(distance_data, var_tr_xyz_1, var_rx_xyz_1, var_tr_rpy_1, var_rx_rpy_1, var_tr_xyz_2, var_rx_xyz_2, var_tr_rpy_2, var_rx_rpy_2,\
    mean_tr_xyz_1, mean_rx_xyz_1, mean_tr_rpy_1, mean_rx_rpy_1, mean_tr_xyz_2, mean_rx_xyz_2, mean_tr_rpy_2, mean_rx_rpy_2, optimal_angle) 
    
    #print('xxx', angles)
    #exit()
    plots(data_angle_time, angles)
    
    
    exit()
    
    
def distance():
    '''
    Calculate distance between the current loc and past loc of tr and rx
    '''
    distance_tr_xyz_list = []
    distance_rx_xyz_list = []
    distance_tr_rpy_list = []
    distance_rx_rpy_list = []
    #exit()
    # print('data_tr_xyz', flytera_cfg.data_tr_xyz)
    # print(np.shape( flytera_cfg.data_tr_xyz))
    # print('data_tr_xyz', flytera_cfg.data_rx_xyz)
    # print(np.shape(flytera_cfg.data_rx_xyz))
    # print(np.shape(flytera_cfg.data_tr_xyz))
    # print('data_rx_xyz', flytera_cfg.data_rx_xyz)
    # print('data_tr_rpy', flytera_cfg.data_tr_rpy)
    # print(np.shape(flytera_cfg.data_tr_rpy))
    # print('data_rx_rpy', flytera_cfg.data_rx_rpy)
    # print(np.shape(flytera_cfg.data_rx_rpy))
    
    data_tr_xyz = np.asarray(flytera_cfg.data_tr_xyz)
    data_rx_xyz = np.asarray(flytera_cfg.data_rx_xyz)
    data_tr_rpy = np.asarray(flytera_cfg.data_tr_rpy)
    data_rx_rpy = np.asarray(flytera_cfg.data_rx_rpy)
    #print('data_tr_xyz', data_tr_xyz)
    #print('data_tr_xyz', np.shape(data_tr_xyz))
    #print('data_rx_xyz', data_rx_xyz)
    #print('data_rx_xyz', np.shape(data_rx_xyz))
    #print('data_tr_rpy', data_tr_rpy)
    #print('data_tr_rpy', np.shape(data_tr_rpy))
    #print('data_rx_rpy', data_rx_rpy)
    #print('data_rx_rpy', np.shape(data_rx_rpy))
    #exit()
    for i in range(flytera_cfg.sim_tick):
        distance_tr_xyz = distance_calculation(data_tr_xyz[i+0], data_tr_xyz[i+1])
        distance_rx_xyz = distance_calculation(data_rx_xyz[i+0], data_rx_xyz[i+1])
        distance_tr_rpy = distance_calculation(data_tr_rpy[i+0], data_tr_rpy[i+1])
        distance_rx_rpy = distance_calculation(data_rx_rpy[i+0], data_rx_rpy[i+1])
        
        distance_tr_xyz_list.append(distance_tr_xyz)
        distance_rx_xyz_list.append(distance_rx_xyz)
        distance_tr_rpy_list.append(distance_tr_rpy)
        distance_rx_rpy_list.append(distance_rx_rpy)
    return distance_tr_xyz_list, distance_rx_xyz_list, distance_tr_rpy_list, distance_rx_rpy_list   
    
        
def distance_calculation(data1,data2): 
    '''
    Return the distance value
    '''
    
    distance = np.sqrt(np.power(data1[0] - data2[0], 2) + np.power(data1[1] - data2[1], 2) + np.power(data1[2] - data2[2], 2))
    #print(distance)
    
    return distance
    
def variance_calc(data1, data2, data3, data4):
    '''
    Calculate variance for xyz and rpy at both tr and rx side
    '''
    var_tr_xyz = statistics.variance(data1)
    var_rx_xyz = statistics.variance(data2)
    var_tr_rpy = statistics.variance(data3)
    var_rx_rpy = statistics.variance(data4)
    
    #print(var_tr_xyz, var_rx_xyz, var_tr_rpy, var_rx_rpy)
    return var_tr_xyz, var_rx_xyz, var_tr_rpy, var_rx_rpy
    
def mean_calc(data1, data2, data3, data4):
    '''
    Calculate variance for xyz and rpy at both tr and rx side
    '''
    mean_tr_xyz = statistics.mean(data1)
    mean_rx_xyz = statistics.mean(data2)
    mean_tr_rpy = statistics.mean(data3)
    mean_rx_rpy = statistics.mean(data4)
    
    #print(mean_tr_xyz, mean_rx_xyz, mean_tr_rpy, mean_rx_rpy)
    return mean_tr_xyz, mean_rx_xyz, mean_tr_rpy, mean_rx_rpy
    
def optimal_angle_calc(data):
    optimal_angle_list = []
    #print('xxx', data)
    
    transposed_data = np.transpose(data)
    #print(transposed_data)
    
    shape_for_data = transposed_data.shape
    #print(shape_for_data[0])
    for i in range(shape_for_data[0]):
        #print(transposed_data[i])
        loction_max_value = np.where(transposed_data[i] == np.amax(transposed_data[i]))
        indices = loction_max_value[0]
        indices = indices[0]
        #print(indices)
        optimal_angle_list.append(indices+1)
    #print(optimal_angle_list)
    #exit()
    optimal_angle = np.asarray(optimal_angle_list)
    #print(optimal_angle)
    #exit()
    return optimal_angle, optimal_angle_list
    
def plot_angle_capacity(data):
    #print('AAAAA', data)
    
    size_data = data.shape[0]
    #print('BBBBB', size_data)
    capacity_y_axis = []
    for i in range(size_data):
        #print('CCCCC', i)
        #print('DDDDD', data[i])
        #print('EEEEE', statistics.mean(data[i]))
        cap_avg = statistics.mean(data[i])
        #print('FFFFF', cap_avg)
        capacity_y_axis.append(cap_avg)
    #print('GGGGG', capacity_y_axis)
    #exit()
    font = {'family' : 'sans',
        'size'   : 14}	
    matplotlib.rc('font', **font)

    
    #matplotlib.pyplot.errorbar(range(1,size_data+1), capacity_y_axis, yerr=5, c='b', ecolor='b', capsize=2)
    matplotlib.pyplot.plot(range(1, 75), capacity_y_axis, c='b', marker='o')
    matplotlib.pyplot.xlabel('Beam Steering Angle (degrees)') 
    matplotlib.pyplot.ylabel('THz Link Capacity (Mbps)') 

    matplotlib.pyplot.grid(True)
  
    #matplotlib.pyplot.show()
    #exit()

def plots(data1, data2):
    y_axis = []
    pass_data = []
    #print('a', data1)
    #print('b', data2)
    #exit()
    # print(len(data2))
    # print(data1.shape)
    data2.tolist()
    # print(int(data2[0]))
    # print(data1[2])
    N = int(flytera_cfg.sim_tick/4)
    #interval = int(np.ceil(0.9*flytera_cfg.sim_tick))
    

    ang_1 = data1[0][3*N:]
    #ang_5 = ang_5/5
    #print(ang_1)
    ang_2 = data1[1][3*N:]
    #print(ang_5)
    ang_5 = data1[4][3*N:]
    #print(ang_10)
    ang_10 = data1[9][3*N:]
    #print(ang_20)
    #exit()
  
    for i in range(len(data2)):
        index1 = int(data2[i-1])
        #print('c', index1)
        index2 = index1 - 1
        #print('d', index2)
        data = data1[index2]
        data = data[3*N:]
        #print('e', data)
        data_num = data[i]
        #print('ee', data_num)
        pass_data.append(data_num)
        #print('f', pass_data)
        #print(data[5:7])
        #data = statistics.mean(data)
        #y_axis.append(data)
        #print('g', y_axis)
    #exit()
    #print(y_axis)    ##Data for beam alignment plot##
    print('MEAN', statistics.mean(pass_data))    ##Data for beam alignment plot##
    #print(pass_data)
    #exit()
    font = {'family' : 'sans',
    'size'   : 20}	
    matplotlib.rc('font', **font)
    
    matplotlib.pyplot.figure()
    
    #print('Lebeam', statistics.mean(y_axis))
    print('angle 1', statistics.mean(ang_1))
    #print('angle 2', statistics.mean(ang_2))
    print('angle 5', statistics.mean(ang_5))
    #print('angle 10', statistics.mean(ang_10))
    
    
    #matplotlib.pyplot.xlim(0,100)
    #matplotlib.pyplot.ylim(0,1800)
    matplotlib.pyplot.plot(range(len(pass_data)), pass_data, c='k', linestyle = '-',  label='LeBeam')
    #matplotlib.pyplot.plot(range(len(y_axis)), ang_1, c='b', linestyle = '--',linewidth=2.0, label='Directivity Angle = 1\xB0')
    matplotlib.pyplot.plot(range(len(pass_data)), ang_1, c='r', linestyle = '--', label='Directivity Angle = 1\xB0')
    matplotlib.pyplot.plot(range(len(pass_data)), ang_5, c='b', linestyle = '-.', label='Directivity Angle = 5\xB0')
    #matplotlib.pyplot.plot(range(len(pass_data)), ang_10, c='b', linestyle = '-.',linewidth=2.0, label='Directivity Angle = 10\xB0')
    matplotlib.pyplot.ylim(0,(max(pass_data)+1))
    matplotlib.pyplot.xlim(0,1000)
    matplotlib.pyplot.xlabel('Network Run Time (slot)') 
    matplotlib.pyplot.ylabel('Capacity (Mbps)') 
    matplotlib.pyplot.legend()
    matplotlib.pyplot.grid(True)

    matplotlib.pyplot.show()
    exit()
    
    

    #print(y_axis)

def plot_ang_v_cap_diff_mob():

    beam1 = [0, 140.08874998071076, 191.3175943843502, 287.9405923467535, 339.5549245017162, 366.46046873003706, 478.1679012196474, 510.7275084527535, 623.5812746772004, 695.3376656225639, 887.6393959938431, 704.5641326680235, 685.2873424171918, 406.95222022255666, 345.69513850829264, 296.9059015325126, 257.4270064266785, 225.03837915855695, 198.1429189154662, 175.5683235910422, 156.43861690375525,  126.00655348121495, 113.79248223105189, 103.1311896063699, 93.77112374288048, 85.50966165868057, 78.1821294668511, 71.6535906569518, 65.81263338165392, 60.56661978647734, 55.838017281024165, 51.56153923625755, 47.68189739952415, 44.15202100048003, 40.93163506391065, 37.9861174982986, 35.28557422653037, 32.80408610770443, 30.519092145379798, 28.410881520840142, 26.462173059288563, 24.657765352179236, 22.984244294181824, 21.429737520117676, 19.983707344305802, 18.636775458783173, 17.380573946790843, 16.20761819536663, 15.111198107369862, 14.08528466545224, 13.124449424040629, 12.223794927642224, 11.37889439590405, 10.585739294239565, 9.840693636310812, 9.140454051272403, 8.482014802382974, 7.862637070629321, 7.279821922407161, 6.731286468037627, 6.214942791172704, 5.728879290544202, 5.271344127112263, 4.840730513178686, 4.435563616809851, 4.054488886104737, 3.6962616243607886, 3.359737669797091, 3.043865052820127, 2.747676520379034, 2.4702828311824487, 2.2108667378148583, 1.9686775823622655, 1.743026441333263, 1.5332817636050904]
    
    beam2 = [0, 1003.258950951794, 1323.0477253043846, 1498.2989009439946, 2033.6446163480744, 1089.2388052136301, 628.7322254924961, 507.53263615999737, 412.91130124902463, 343.34872639854336, 290.9478346454287, 250.44324256834184, 218.33679300348726, 192.63224682370304, 172.17772348391037, 155.73061649385295, 142.0725873807267, 131.04850586238848, 122.84052604337849, 117.7265033443198, 126.67844573111645, 125.73890863761181, 118.61285770013602, 107.5021695408851, 97.74717904957069, 89.1368508411612, 81.49965946693085, 74.69504345582943, 68.6069388032343, 63.13883360146871, 58.20994852041112, 53.75225967997838, 49.70815823333945, 46.02859576321757, 42.67160364123333, 39.60110264182978, 36.78593959549141, 34.19910293546767, 31.817080175432633, 29.619328726615457, 27.587837780293203, 25.706763785883233, 23.962125735279155, 22.34154930306364, 20.834051096573823, 19.429855992077485, 18.12024188699322, 16.897407268062462, 15.754357845718278, 14.684809184153556, 13.683102801893318, 12.744133657501406, 11.863287291401495, 11.036385184793959, 10.259637133605912, 9.529599629830196, 8.843139402724349, 8.197401404700948, 7.589780636545284, 7.017897298008929, 6.479574826172942, 5.972820447947475, 5.495807926846208, 5.046862229505516, 4.624445875745181, 4.227146768468662, 3.8536673273303332, 3.5028147736616075, 3.173492434278356, 2.864691949056009, 2.5754862819851336, 2.3050234481940546, 2.05252088045524, 1.8172603682425266, 1.5985835106935486]
    
    beam3 = [0, 1811.5663399893647, 2232.5891262850687, 1850.7144444680375, 1291.9163367518076, 933.1387903572105, 724.7248058465378, 571.1849720351101, 460.7605296149072, 380.230302199133, 318.7974009944075, 271.2861445284824, 234.11768641576802, 203.99589100765567, 179.67730288174172, 159.6689384918548, 143.3718501637312, 129.82321537499183, 118.57825072255119, 109.41682290811967, 102.35716509763817, 96.9931192772304, 92.31800892484296, 88.18275076794205, 89.50212187416707, 91.24970104451388, 83.43227304056487, 76.46694456667542, 70.23495060027673, 64.63752927398006, 59.59201509726305, 55.0287936099271, 50.88890719094988, 47.1221577386796, 43.68559185207158, 40.542282911484314, 37.66034540943799, 35.01213228987332, 32.57357748987526, 30.323654438302757, 28.243927726498576, 26.318180079889686, 24.53210052366663, 22.87302253961505, 21.329703266023326, 19.89213655441564, 18.551394081661115, 17.299489810639386, 16.129263962596767, 15.034283359287937, 14.0087555509146, 13.04745459588373, 12.145656723039764, 11.299084403744832, 10.503857603656963, 9.756451182996063, 9.05365757793065, 8.39255403116905, 7.77047375220273, 7.1849804811959865, 6.633846008647033, 6.115030268419062, 5.626663676760501, 5.1670314363347645, 4.734559563501574, 4.327802430356752, 3.9454316413129584, 3.586226088121586, 3.2490630478435847, 2.932910205938993, 2.6368185018274493, 2.3599157073405923, 2.1014006597807406, 1.860538081072213, 1.6366539229770105]    
    
    
    #print(len(beam1))
    #print(len(beam50))
    #print(len(beam1000))
    font = {'family' : 'sans',
    'size'   : 14}	
    matplotlib.rc('font', **font)
    
    matplotlib.pyplot.figure()
    
    matplotlib.pyplot.plot(range(0,75), beam1, c='k', linestyle = '-', marker = 'o',  label='Tx and Rx with Large Windy Mobility')
    matplotlib.pyplot.plot(range(0,75), beam2, c='b', linestyle = ':', marker = 'v',   label='Tx and Rx with Large Mobility')
    matplotlib.pyplot.plot(range(0,75), beam3, c='g', linestyle = '--', marker = '<', label='Tx with Large Windy and Rx with Large Outdoor')
    
    matplotlib.pyplot.xlim(0,75)
    matplotlib.pyplot.xlabel('Beam Steering Angle (degrees)') 
    matplotlib.pyplot.ylabel('THz Link Capacity (Mbps)') 
    matplotlib.pyplot.legend()
    matplotlib.pyplot.grid(True)

    matplotlib.pyplot.show()
    
def plot_ang_v_cap_diff_bai():

    beam_1 = [0, 591.3175943843502, 10482.688381936288, 5600.842995369041, 3408.391677748655, 2268.302972918709, 1608.9357113430603, 1196.249668958837, 921.9260153630684, 730.784318544156, 592.4893091921421, 489.306587257663, 410.3317423622811, 348.5719933397997, 299.3808773988709, 259.5758023796321, 226.91891241474943, 199.80023175092896, 177.0379576178679, 157.7489832419105, 141.26282614850777, 127.0631192989414, 114.7470340706786, 103.99662632150633, 94.55826797465289, 86.22766073231415, 78.83876705357035, 72.25553149935945, 66.36561724439636, 61.07561649083257, 56.307351624164006, 51.99499239603266, 48.08278982471615, 44.52328060890748, 41.27585369589284, 38.305597916836746, 35.582369459109586, 33.080032545849775, 30.77583752684822, 28.649908693719418, 26.684820251270768, 24.865243530068017, 23.177652089487623, 21.61007410976729, 20.15188360609156, 18.793623665383794, 17.526856217121782, 16.34403388542189, 15.238390292859497, 14.203845844084675, 13.234926545160192, 12.32669384030508, 11.474683792672272, 10.67485421648517, 9.923538597216512, 9.217405824664247, 8.553424918748334, 7.928834055961129, 7.341113310661124, 6.7879606138840645, 6.267270506213029, 5.777115323172177, 5.315728503639686, 4.881489755636979, 4.472911850954481, 4.088628851509438, 3.727385597076429, 3.3880283068310617, 3.0694961666247966, 2.7708137906145436, 2.4910844602170776, 2.2294840557195945, 1.9852556065439813, 1.7577043954132758, 1.5461935596766156]
    
    beam_50 = [0, 725.2293939953599, 914.9644119819241, 591.3175943843502, 2707.7780687325057, 2328.6965342027793, 2185.792329329544, 1705.0904941478211, 1433.2033955704424, 1187.3017999694168,  587.9639366903821, 485.55588389376226, 407.1777513237875, 345.88694493488197, 297.0707903505393, 257.5700773489965, 225.16352599512757, 198.25316479678472, 175.66605064908128, 156.5257271184272, 140.16678004422963, 126.0767582785608, 113.85589648099779, 103.18867403578955, 93.82340013125469, 85.5573397560506, 78.2257278982824, 71.69355332213989, 65.84934244136254, 60.60040603568452, 55.86916850164, 51.59030697357193, 47.70850249847836, 44.176658158465884, 40.95447659787697, 38.00731647980633, 35.30526710502301, 32.82239491682079, 30.53612636759429, 28.42673967057993, 26.476944032885836, 24.671529583753674, 22.99707474924275, 21.441700552861796, 19.994863439945664, 18.64717987851251, 17.390277289978535, 16.216666891129357, 15.119634845675474, 14.093148776278547, 13.131777211764616, 12.23061996672999, 11.385247793048565, 10.591649921327674, 9.846188337961369, 9.145557830149814, 8.486750985037979, 7.867027456240458, 7.2838869164719116, 6.735045202785593, 6.218413234246176, 5.732078343285074, 5.274287713629624, 4.84343366122076, 4.438040531339713, 4.05675301637142, 3.6983257251596244, 3.3616138575380012, 3.0455648569455445, 2.7492109306142307, 2.471662341050978, 2.2121013847969606, 1.9697769850425988, 1.7439998338405571, 1.5341380276206382]
    
    beam_100 = [0, 140.08874998071076, 191.3175943843502, 287.9405923467535, 339.5549245017162, 366.46046873003706, 478.1679012196474, 510.7275084527535, 623.5812746772004, 695.3376656225639, 887.6393959938431, 704.5641326680235, 685.2873424171918, 406.95222022255666, 345.69513850829264, 296.9059015325126, 257.4270064266785, 225.03837915855695, 198.1429189154662, 175.5683235910422, 156.43861690375525,  126.00655348121495, 113.79248223105189, 103.1311896063699, 93.77112374288048, 85.50966165868057, 78.1821294668511, 71.6535906569518, 65.81263338165392, 60.56661978647734, 55.838017281024165, 51.56153923625755, 47.68189739952415, 44.15202100048003, 40.93163506391065, 37.9861174982986, 35.28557422653037, 32.80408610770443, 30.519092145379798, 28.410881520840142, 26.462173059288563, 24.657765352179236, 22.984244294181824, 21.429737520117676, 19.983707344305802, 18.636775458783173, 17.380573946790843, 16.20761819536663, 15.111198107369862, 14.08528466545224, 13.124449424040629, 12.223794927642224, 11.37889439590405, 10.585739294239565, 9.840693636310812, 9.140454051272403, 8.482014802382974, 7.862637070629321, 7.279821922407161, 6.731286468037627, 6.214942791172704, 5.728879290544202, 5.271344127112263, 4.840730513178686, 4.435563616809851, 4.054488886104737, 3.6962616243607886, 3.359737669797091, 3.043865052820127, 2.747676520379034, 2.4702828311824487, 2.2108667378148583, 1.9686775823622655, 1.743026441333263, 1.5332817636050904]
    #print(len(beam1))
    #print(len(beam50))
    #print(len(beam1000))
    font = {'family' : 'sans',
    'size'   : 14}	
    matplotlib.rc('font', **font)
    
    matplotlib.pyplot.figure()
    
    matplotlib.pyplot.plot(range(0,75), beam_1, c='k', linestyle = '--', marker = 'o',  label='Beam Alignment Interval = 1 ')
    matplotlib.pyplot.plot(range(0,75), beam_50, c='b', linestyle = '--', marker = 'v',   label='Beam Alignment Inteval = 100')
    matplotlib.pyplot.plot(range(0,75), beam_100, c='g', linestyle = '--', marker = '<', label='Beam Alignment Interval = 1000')
    #matplotlib.pyplot.plot(range(0,75), beam4, c='r', linestyle = '--', marker = '>', label='Tr with Large Outdoor and Rx with Large Windy')
    
    matplotlib.pyplot.xlabel('Beam Steering Angle (degrees)') 
    matplotlib.pyplot.ylabel('THz Link Capacity (Mbps)') 
    matplotlib.pyplot.legend()
    matplotlib.pyplot.grid(True)

    matplotlib.pyplot.show()
    
    