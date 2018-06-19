"""
Author: Eric Brown
radar.py is a module that contains the radar class and connected functions. Code and
comment style is meant to follow the conventions of the pyART library where possible.

References:
"Radar Handbook", Merrill Skolnik
"Radar Analysis and Design Using MATLAB", Bassem Mahafza
"Fundamentals of Radar Signal Processing", Mark Richards

This is the structure of the radar class. When an instance is created the constructor
will default to the values listed. Optionally the class may be declared with custom
parameters. A parsing library will be written to read params from CSV or text.
Values for each attribute are stored in the dictionary under the 'value' key.
Pulse data and RDMap details is stored as a numpy structured array
in the 'data' attribute.

Attributes
----------
data : structured array
    contains the derivative radar attributes and raw pulse returns
pt : float64
    Power transmitted by radar
freq : float64
    Center frequency of the waveform
gain : float64
    gain of the transmitter/receiver
bandw : float64
    bandwidth of the pulse waveform
nf : float64
    noise factor
loss : float64
    system loss
temp_o : int
    base temperature, usually 290K
range_max : float
    max calculable range, limiter to prevent funky behavior at extreme ranges
hr : float
    height of the radar above surface (same as altitude for now)
ncpi :

"""
import scipy as sp
import envconst as const


class Radar:
    # instantiate objects
    def __init__(self, pt, freq, gain, bandw, nf, loss, range_max, hr,
                 ncpi, nprf, nfft, prf, npri, target_rcs, target_radvel,
                 target_range, duty,

                 target_pow=1, pulse_type='lfm', temp_o=290, data=None,
                 pulse=None, fs=None, tbp=None, ts=None):

        self.pt = pt
        self.freq = freq
        self.gain = gain
        self.bandw = bandw
        self.nf = nf
        self.loss = loss
        self.temp_o = temp_o
        self.range_max = range_max
        self.hr = hr
        self.ncpi = ncpi
        self.nprf = nprf
        self.nfft = nfft
        self.prf = prf
        self.npri = npri
        self.pulse_type = pulse_type
        self.target_rcs = target_rcs  # Will need to become array of targets
        self.target_radvel = target_radvel
        self.target_range = target_range
        self.target_pow = target_pow
        self.duty = duty
        self.data = data
        self.pulse = pulse
        self.fs = fs
        self.tbp = tbp
        self.ts = ts

    # GENERATORS
    def gen_pulse(self):
        if self.pulse_type is 'lfm':
            tau = self.duty / self.prf

            # Time Bandwidth Product
            self.tbp = tau * self.bandw

            # Sampling Rate
            self.fs = 2 * self.bandw

            # LFM Pulse (up/down)
            self.ts = sp.arange(-tau / 2, tau / 2, 1 / self.freq)
            ramp = sp.pi * self.bandw / tau
            self.pulse = sp.exp(1j * ramp * self.ts ** 2)
            return self.tbp, self.fs, self.pulse

    def gen_data(self, add_noise=False):
        cpi_start = 0
        time = 0
        prf = self.prf  # will become vector
        range_unam = const.c0 / prf / 2
        tcpi = 1 / prf
        rng_window = sp.array([0., range_unam])
        fast_time = rng_window // const.c0 * 2
        ft_axis = sp.arange(fast_time[0], fast_time[1], 1 / (2 * self.bandw))
        numbins = ft_axis.size
        rng_axis = sp.linspace(0, numbins, rng_window[1])
        p_data = sp.zeros((numbins, self.npri))
        self.data = sp.zeros((self.ncpi, numbins, self.npri))
        for i in range(1, self.ncpi):
            '''
            This will loop to create data for each CPI, the first section will
            create vectors for the radar attributes that aligns with the data 
            it is collected from
            '''

            for p in range(0, self.npri):
                time = (p) * tcpi
                # itarget in range(0,len(target_range)): # this when I get to multiple targets
                range_new = self.target_range + self.target_radvel
                # The '1' will be replaced with a power calculation in future
                tmp_array = 1 * self.pulse * sp.exp(
                    sp.sqrt(-1) * 2 * sp.pi * (sp.arange(0, len(self.pulse)) / self.fs + time) * 2 *
                    self.target_radvel / (const.c0 / self.freq))
                '''
                Insert generated data into appropriate 'bins'
                Each i loop goes into it's own MxN matrix and is stacked in a 3rd dim
                making it (rng x dop x cpi). The tmp_array calculates the value of the target
                while the indexing below slots it into the correct dopper bins. The range binning is taken care of by the 
                the pri loop.
                '''
                index1 = round(sp.mod(range_new, rng_window[1] / (rng_window[1] * (numbins)) + 1))
                print(index1)
                index2 = index1 + min(len(self.ts - 1), numbins - index1)
                print(index2)
                index_size = sp.arange(index1, index2 + 1)
                print(index_size)
                rev_tmp = tmp_array[0:len(index_size)]
                print(rev_tmp)
                p_data[p, index_size] = p_data[p, index_size] + rev_tmp[:: -1]
                # add noise here
                #if add_noise is True:
                #    p_data[p, :] = p_data[p, :]
            cpi_start = cpi_start + time + tcpi + 1 / self.fs
            # Save a map for RDMap for every CPI. Structured Array
            self.data[i-1] = p_data
            return self.data
