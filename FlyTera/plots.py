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

import matplotlib.pyplot as plt
import numpy as np
import random
import confidence_interval

x_ue = list(range(0,16))#[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
x_bs = list(range(0,9))#[1, 2, 3, 4, 5, 6, 7]
rate_ue_ue_fixed = [0, 118, 142, 146, 244, 279, 357, 398, 401, 426, 444, 503, 513, 690, 795, 1020]
rate_ue_ue_random = [0, 241, 261, 313, 325, 344, 432, 473, 483, 500, 530, 560, 580, 800, 939, 1242]
rate_ue_ue_rlearning = [0, 458, 463, 485, 498, 542, 553, 573, 579, 612, 656, 690, 792, 895, 1025, 1293]
# rate_ue_bs_random = [2125, 2384, 2689, 3020, 3763, 4265, 4682]
# rate_ue_bs_rlearning = [2380, 2601, 3086, 3607, 4139, 4751, 5020]


font = {'family' : 'sans',
        'size'   : 16}	
plt.rc('font', **font)

plt.errorbar(x_ue, rate_ue_ue_fixed, yerr=50, c='r', ecolor='r', capsize=5)
plt.errorbar(x_ue, rate_ue_ue_random, yerr=50, c='b', ecolor='b', capsize=5)
plt.errorbar(x_ue, rate_ue_ue_rlearning, yerr=50,c='k', ecolor='k', capsize=5)


plt.figure(1)
plt.xlim(0,15)
plt.ylim(0,1400)
plt.plot(x_ue, rate_ue_ue_fixed, c='r', marker='o', linestyle=':',label='Fixed FBS')
plt.plot(x_ue, rate_ue_ue_random, c='b', marker='v',linestyle='--',label='Random Movement of FBS')
plt.plot(x_ue, rate_ue_ue_rlearning, c='k', marker='s',linestyle='-',label='FlyTera')
plt.xlabel('Number of Users')
plt.ylabel('Sum Rate (Mbps)')
plt.legend()
plt.grid(True)


###############################static_user_moves####################################
font = {'family' : 'sans',
        'size'   : 16}	
plt.rc('font', **font)

plt.figure(2)
plt.xlim(0,8)
plt.ylim(0,1100)
x_bs = list(range(0,9))#[1, 2, 3, 4, 5, 6, 7, 8]
rate_micro_only = [0, 17, 47, 59, 72, 93, 98, 149, 185]
rate_miilli_only = [0, 104, 186, 210, 282, 311, 349, 421, 496]
rate_tera_only = [0, 11, 33, 89, 151, 221, 266, 339, 372]
rate_milli_tera = [0, 149, 161, 322, 469, 573, 589, 794, 855]
rate_micro_tera = [0, 45, 76, 142, 220, 300, 352, 458, 514]
rate_micro_milli = [0, 65, 150, 169, 387, 452, 539, 643, 776]
rate_micro_milli_tera = [0, 249, 350, 528, 550, 734, 789, 834, 981]

plt.errorbar(x_bs, rate_micro_only, yerr=50, c='r', ecolor='r', capsize=5, fmt=".r")
plt.errorbar(x_bs, rate_miilli_only, yerr=50, c='r', ecolor='r', capsize=5, fmt=".r")
plt.errorbar(x_bs, rate_tera_only, yerr=50,c='r', ecolor='r', capsize=5, fmt=".r")
plt.errorbar(x_bs, rate_micro_milli, yerr=50, c='b', ecolor='b', capsize=5)
plt.errorbar(x_bs, rate_micro_tera, yerr=50, c='b', ecolor='b', capsize=5)
plt.errorbar(x_bs, rate_milli_tera, yerr=50,c='b', ecolor='b', capsize=5)
plt.errorbar(x_bs, rate_micro_milli_tera, yerr=50,c='k', ecolor='k', capsize=5)

plt.plot(x_bs, rate_micro_only, c='r', marker='o',linestyle=':',label='Microwave band only')
plt.plot(x_bs, rate_miilli_only, c='r', marker='v',linestyle=':',label='Millimeter wave band only')
plt.plot(x_bs, rate_tera_only, c='r', marker='^',linestyle=':',label='Terahertz band only')
plt.plot(x_bs, rate_micro_milli, c='b', marker='<',linestyle='--',label='Microwave and Millimeter bands')
plt.plot(x_bs, rate_micro_tera, c='b', marker='>',linestyle='--',label='Microwave and Terahertz band')
plt.plot(x_bs, rate_milli_tera, c='b', marker='D',linestyle='--',label='Millimeter wave and Terahertz band')
plt.plot(x_bs, rate_micro_milli_tera, c='k', marker='s',linestyle='-',label='FlyTera')
plt.xlabel('Number of FBS')
plt.ylabel('Sum Rate (Mbps)')
plt.grid(True)
plt.legend()

###############################static_user_static####################################
font = {'family' : 'sans',
        'size'   : 16}	
plt.rc('font', **font)

plt.figure(3)
plt.xlim(0,8)
plt.ylim(0,700)
x_bs = list(range(0,9))#[1, 2, 3, 4, 5, 6, 7, 8]
rate_micro_only = [0, 10, 35, 42, 50, 59, 68, 79, 85]
rate_miilli_only = [0, 34, 46, 60, 82, 101, 149, 221, 296]
rate_tera_only = [0, 7, 23, 29, 31, 41, 66, 89, 92]
rate_milli_tera = [0, 74, 80, 120, 149, 273, 389, 394, 487]
rate_micro_tera = [0, 29, 48, 72, 114, 170, 183, 298, 358]
rate_micro_milli = [0, 32, 78, 98, 147, 259, 326, 343, 367]
rate_micro_milli_tera = [0, 78, 122, 258, 350, 398, 455, 482, 592]

plt.errorbar(x_bs, rate_micro_only, yerr=50, c='r', ecolor='r', capsize=5, fmt=".r")
plt.errorbar(x_bs, rate_miilli_only, yerr=50, c='r', ecolor='r', capsize=5, fmt=".r")
plt.errorbar(x_bs, rate_tera_only, yerr=50,c='r', ecolor='r', capsize=5, fmt=".r")
plt.errorbar(x_bs, rate_micro_milli, yerr=50, c='b', ecolor='b', capsize=5)
plt.errorbar(x_bs, rate_micro_tera, yerr=50, c='b', ecolor='b', capsize=5)
plt.errorbar(x_bs, rate_milli_tera, yerr=50,c='b', ecolor='b', capsize=5)
plt.errorbar(x_bs, rate_micro_milli_tera, yerr=50,c='k', ecolor='k', capsize=5)

plt.plot(x_bs, rate_micro_only, c='r', marker='o',linestyle=':',label='Microwave band only')
plt.plot(x_bs, rate_miilli_only, c='r', marker='v',linestyle=':',label='Millimeter wave band only')
plt.plot(x_bs, rate_tera_only, c='r', marker='^',linestyle=':',label='Terahertz band only')
plt.plot(x_bs, rate_micro_milli, c='b', marker='<',linestyle='--',label='Microwave and Millimeter bands')
plt.plot(x_bs, rate_micro_tera, c='b', marker='>',linestyle='--',label='Microwave and Terahertz band')
plt.plot(x_bs, rate_milli_tera, c='b', marker='D',linestyle='--',label='Millimeter wave and Terahertz band')
plt.plot(x_bs, rate_micro_milli_tera, c='k', marker='s',linestyle='-',label='FlyTera')
plt.xlabel('Number of FBS')
plt.ylabel('Sum Rate (Mbps)')
plt.grid(True)
plt.legend()

###############################mobile####################################

font = {'family' : 'sans',
        'size'   : 16}	
plt.rc('font', **font)

plt.figure(4)
plt.xlim(0,8)
plt.ylim(0,1800)
x_bs = list(range(0,9))#[1, 2, 3, 4, 5, 6, 7]
rate_micro_only = [0, 24, 106, 112, 138, 146, 158, 244, 274]
rate_miilli_only = [0, 110, 188, 239, 314, 333, 421, 440, 581]
rate_tera_only = [0, 16, 89, 132, 176, 299, 336, 421, 477]
rate_milli_tera = [0, 356, 386, 579, 717, 859, 930, 1021, 1252]
rate_micro_tera = [0, 207, 287, 304, 374, 502, 533, 698, 778]
rate_micro_milli = [0, 104, 245, 265, 401, 577, 651, 730, 872]
rate_micro_milli_tera = [0, 602, 687, 797, 1024, 1297, 1481, 1537, 1664]

plt.errorbar(x_bs, rate_micro_only, yerr=50, c='r', ecolor='r', capsize=5, fmt=".r")
plt.errorbar(x_bs, rate_miilli_only, yerr=50, c='r', ecolor='r', capsize=5, fmt=".r")
plt.errorbar(x_bs, rate_tera_only, yerr=50,c='r', ecolor='r', capsize=5, fmt=".r")
plt.errorbar(x_bs, rate_micro_milli, yerr=50, c='b', ecolor='b', capsize=5)
plt.errorbar(x_bs, rate_micro_tera, yerr=50, c='b', ecolor='b', capsize=5)
plt.errorbar(x_bs, rate_milli_tera, yerr=50,c='b', ecolor='b', capsize=5)
plt.errorbar(x_bs, rate_micro_milli_tera, yerr=50,c='k', ecolor='k', capsize=5)

plt.plot(x_bs, rate_micro_only, c='r', marker='o',linestyle=':',label='Microwave band only')
plt.plot(x_bs, rate_miilli_only, c='r', marker='v',linestyle=':',label='Millimeter wave band only')
plt.plot(x_bs, rate_tera_only, c='r', marker='^',linestyle=':',label='Terahertz band only')
plt.plot(x_bs, rate_micro_milli, c='b', marker='<',linestyle='--',label='Microwave and Millimeter bands')
plt.plot(x_bs, rate_micro_tera, c='b', marker='>',linestyle='--',label='Microwave and Terahertz band')
plt.plot(x_bs, rate_milli_tera, c='b', marker='D',linestyle='--',label='Millimeter wave and Terahertz band')
plt.plot(x_bs, rate_micro_milli_tera, c='k', marker='s',linestyle='-',label='FlyTera')
plt.xlabel('Number of FBS')
plt.ylabel('Sum Rate (Mbps)')
plt.grid(True)
plt.legend()

#########################################################################################
x=list(range(0,16))
plt.figure(5)
time_10_users = (0, 3.64, 3.69, 4, 4.08, 4.67, 4.79, 4.31, 4.21, 4.19, 4.59, 4.41, 4.29, 4.50, 4.60, 4.51)
time_7_users = (0, 3.97, 3.93, 4.14, 4.27, 4.10, 4.85, 4.18, 4.02, 4.18, 4.97, 4.10, 4.02, 4.21, 4.84, 4.85)
time_5_users = (0, 3.77, 3.71, 4.13, 4.07, 4.22, 4.54, 3.79, 3.78, 4.37, 4.40, 4.44, 4.11, 4.10, 3.92, 4.23)
plt.xlim(0,15)
plt.ylim(0,6)

plt.errorbar(x, time_5_users, yerr=0.1, c='r', ecolor='r', capsize=5)
plt.errorbar(x, time_7_users, yerr=0.1, c='b', ecolor='b', capsize=5)
plt.errorbar(x, time_10_users, yerr=0.1,c='k', ecolor='k', capsize=5)

plt.plot(x, time_5_users, c='r', marker='o',linestyle='-',label='Number of Users = 5')
plt.plot(x, time_7_users, c='b', marker='v',linestyle='-',label='Number of Users = 7')
plt.plot(x, time_10_users, c='k', marker='s',linestyle='-',label='Number of Users = 10')
plt.xlabel('Number of FBS')
plt.ylabel('Computational Time (ms)')
plt.grid(True)
plt.legend()
plt.show()
exit()
##########################################################################################
plt.figure(6)
time_1_mbs = (0, 3.36, 3.59, 3.46, 3.64, 3.56, 3.82, 3.63, 3.51, 3.42, 3.28, 3.51, 3.70, 3.64, 3.46, 3.73)
time_2_mbs = (0, 3.56, 3.50, 3.61, 3.56, 3.77, 3.67, 3.75, 3.77, 3.57, 3.58, 3.64, 3.35, 3.33, 3.58, 3.52)
time_3_mbs = (0, 3.71, 3.74, 3.77, 3.73, 3.85, 3.68, 3.71, 3.91, 3.58, 3.67, 3.77, 3.94, 3.95, 3.99, 3.84)
plt.xlim(0,15)
plt.ylim(0,6)
plt.errorbar(x, time_1_mbs, yerr=5, c='r', ecolor='r', capsize=5)
plt.errorbar(x, time_2_mbs, yerr=5, c='b', ecolor='b', capsize=5)
plt.errorbar(x, time_3_mbs, yerr=5,c='k', ecolor='k', capsize=5)

plt.plot(x, time_1_mbs, c='r', marker='o',linestyle='-',label='Number of FBS = 1')
plt.plot(x, time_2_mbs, c='b', marker='v',linestyle='-',label='Number of FBS = 2')
plt.plot(x, time_3_mbs, c='k', marker='s',linestyle='-',label='Number of FBS = 3')
plt.xlabel('Number of Users')
plt.ylabel('Computational Time (ms)')
plt.grid(True)
plt.legend()

