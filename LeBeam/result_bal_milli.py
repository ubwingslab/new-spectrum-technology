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

bal1 = [23, 7, 11, 3]

bal10 = [23, 7, 11, 3]

bal25 = [23, 7, 11, 3]

bal50 = [9, 6, 10, 2] #61,14,9,33 

bal75 = [7, 5, 9, 1] #70, 29, 18, 67
 
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
