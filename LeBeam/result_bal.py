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
import matplotlib.pyplot as plt

font = {'family' : 'sans', 'size'   : 20}	
plt.rc('font', **font)
plt.figure(2)

barWidth = 0.15
 
# bal1 = [4430, 4906, 10102, 8422]

# bal5 = [4430, 4906, 9456, 8377]

# bal10 = [4430, 4781, 6989, 6903]

# bal15 = [4409, 4318, 5792, 5378]

# bal20 = [4041, 3911, 5142, 4295]

bal1 = [185, 141, 42, 71]

bal10 = [185, 141, 42, 71]

bal25 = [185, 141, 42, 71]

bal50 = [82, 139, 42, 65]   #56, 1.4, 0, 8

bal75 = [80, 94, 41, 52]   #57, 33, 2.4, 27
 
yer1 = [0.5, 0.4, 0.5, 0.4, 0.5, 0.4, 0.5, 0.4, 0.5, 0.4, 0.5, 0.4, 0.5, 0.4, 0.5, 0.4, 0.5, 0.4, 0.5, 0.4]

yer2 = [1, 0.7, 1, 0.7, 1, 0.7, 1, 0.7, 1, 0.7, 1, 0.7, 1, 0.7, 1, 0.7, 1, 0.7, 1, 0.7]
 
r1 = np.arange(len(bal1))
r2 = [x + barWidth for x in r1]
r3 = [x + barWidth for x in r2]
r4 = [x + barWidth for x in r3]
r5 = [x + barWidth for x in r4]
 
plt.bar(r1, bal1, width = barWidth, color = 'wheat', hatch = '/', edgecolor = 'black', label='Optimal Beam Control') #, yerr=yer1, capsize=7,
 
plt.bar(r2, bal10, width = barWidth, color = 'tan', hatch = '//', edgecolor = 'black',  label='Beam Alignment Latency = 10') #yerr=yer2, capsize=7,

plt.bar(r3, bal25, width = barWidth, color = 'silver', hatch = '\\', edgecolor = 'black',  label='Beam Alignment Latency = 25') #yerr=yer2, capsize=7,

plt.bar(r4, bal50, width = barWidth, color = 'beige', hatch = '-', edgecolor = 'black',  label='Beam Alignment Latency = 50') #yerr=yer2, capsize=7,

plt.bar(r5, bal75, width = barWidth, color = 'grey', hatch = '.', edgecolor = 'black',  label='Beam Alignment Latency = 75') #yerr=yer2, capsize=7,
 
plt.xticks([r + 2*barWidth for r in range(len(bal1))], ['Small-scale\nnon-windy', 'Large-scale\nnon-windy', 'Small-scale\nwindy', 'Large-scale\nwindy'])#, 130, 140, 150, 160, 170, 180, 190, 200])
plt.xlabel('Mobility Uncertainities') 
plt.ylabel('Capacity (Mbps)')
plt.legend()

#plt.rcParams['axes.axisbelow'] = True
plt.grid(True)

plt.show()
