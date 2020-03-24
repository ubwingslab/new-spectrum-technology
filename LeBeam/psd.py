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

from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
fs = 10e10
print('fs',fs)
N = 1e8
print('N',N)
amp = 4*np.sqrt(2)
print('amp',amp)
freq = 30e9
print('freq',freq)
noise_power = 1e-13 * fs / 2
print('noise_power',noise_power)
time = np.arange(N) / fs
print('time',time)
x = amp*np.sin(2*np.pi*freq*time)
print('x',x)
x += np.random.normal(scale=np.sqrt(noise_power), size=time.shape)
print('x',x)
f, Pxx_den = signal.periodogram(x, fs)
print('f, Pxx_den',f, Pxx_den)
print('f',f)
print('Pxx_den',Pxx_den)
print('max Pxx_den',max(Pxx_den))
plt.semilogy(f, Pxx_den)
plt.ylim([1e-13, 1e-1])
plt.xlim([28e9,32e9])
plt.xlabel('frequency [Hz]')
plt.ylabel('PSD [V**2/Hz]')
plt.show()