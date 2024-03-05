import numpy as np
import pyqtgraph as pg
import pandas as pd
from PyQt5.QtWidgets import QDialog, QFileDialog
from scipy.interpolate import interp1d
import os
import scipy.signal

x_values = 1.0
amplitude = 1.0
y_values = 1.0
plot_iteration = 0
mag_sine_waves = []
Phase2 = []
wave_names = []
max_frequency_hz = 1
fmaxslider_value = 1
Ttime = np.linspace(0, 1, 1000)
signal = []
output_magnitude = []
wave_names = []
waves = {}
SNR = False


def plot_composer_to_viewer(self, combobox):
    global wave_names, waves
    if len(wave_names) > 0:
        last_name = wave_names[len(wave_names)-1]
        wave_name = f"Signal {len(wave_names)}"
        if wave_name == last_name:
            wave_name = f"Signal {len(wave_names)+1}"
    else:
        wave_name = f"Signal {len(wave_names)}"

    frequency = self.freq_slider.value()
    wave_names.append(wave_name)
    combobox.addItem(wave_name)
    global x_values, y_values
    # Get the data from the composergraph
    x_values, y_values = self.composergraph.plotItem.listDataItems()[
        0].getData()
    waves[wave_name] = y_values

    # Check if there's a signal on the viewergraph
    if self.viewergraph.plotItem.listDataItems():
        # If there's a signal on the viewergraph, get its data
        x_values, y_viewer = self.viewergraph.plotItem.listDataItems()[
            0].getData()
        # Add the new signal to the existing one
        y_combined = y_values + y_viewer
        self.viewergraph.clear()  # Clear the viewergraph
        # Plot the combined signal
        self.viewergraph.plot(x_values, y_combined, pen='r', name=frequency)
    else:
        # If there's no signal on the viewergraph, simply plot the new signal
        self.viewergraph.plot(x_values, y_values, pen='r', name=frequency)


def save_csv_file(self):
    global x_values, y_values, fmaxslider_value, Ttime, signal
    if not self.viewergraph.plotItem.listDataItems():
        # Check if there's any data on the viewergraph
        return
    x_values, y_values = self.viewergraph.plotItem.listDataItems()[0].getData()
    # Create a DataFrame with the data
    data = {'x': x_values, 'y': y_values}
    df = pd.DataFrame(data)
    # Generate a unique file name
    file_count = 1
    while True:
        file_name = f'viewer_data_{file_count}.csv'
        if not os.path.exists(file_name):
            break
        file_count += 1
    # Save the data to a CSV file
    df.to_csv(file_name, index=False)
    # Clear the signalgraph
    # self.signalgraph.clear()
    # self.signalgraph.plot(x_values, y_values, pen='g')
    signal = [x_values, y_values]


def Transfer_and_plot(self):
    global y_normal
    if not self.viewergraph.plotItem.listDataItems():
        # Check if there's any data on the viewergraph
        return
    x_values, y_values = self.viewergraph.plotItem.listDataItems()[0].getData()

    self.signalgraph.clear()
    self.signalgraph.plot(x_values, y_values, pen='g')
    y_normal = y_values
    signal = [x_values, y_values]


def increase_snr(self, snr):
    # global x_values, y_values
    global SNR, y_normal
    if self.viewergraph.plotItem.listDataItems():
        x_values, y_values = self.viewergraph.plotItem.listDataItems()[
            0].getData()
    else:
        x_values, y_values = self.signalgraph.plotItem.listDataItems()[
            0].getData()

    if snr == 0:
        # Handle the case when SNR is zero, set noise_level to a default value
        noise_level = 0
        self.SNR_label.setText(f"SNR: {snr}")

    else:
        noise_level = amplitude / snr
    noise = np.random.normal(0, noise_level, len(x_values))
    noisy_signal = y_values + noise
    # y_normal=y_values

    if snr == 1:
        self.signalgraph.clear()
        self.signalgraph.plot(x_values, y_values, pen='g')
        self.SNR_label.setText(f"SNR: {snr}")
    else:
        self.signalgraph.clear()
        self.signalgraph.plot(x_values, noisy_signal, pen='g')
        self.SNR_label.setText(f"SNR: {snr}")
        SNR = True
        print('SNR IS TRUE')


def load(self, channel_index=None):
    global x_values, y_values, signal, y_normal
    self.signalgraph.clear()
    file_path, _ = QFileDialog.getOpenFileName(
        None, caption='Open File', directory='Task1DSP')
    if file_path:
        self.dataframe = None
        with open(file_path, 'r') as file:
            try:
                self.dataframe = pd.read_csv(file_path)
                # print(self.dataframe.iloc[:, 0])
            except pd.errors.ParserError:
                # Handle the case when the CSV file has no header
                self.dataframe = pd.read_csv(file_path, header=None)
                # print(dataframe.iloc[:, 0])
        for i in range(len(self.dataframe)):
            x_values = self.dataframe.iloc[0:1000, 0].to_numpy()
            y_values = self.dataframe.iloc[0:1000, 1].to_numpy()
        y_normal = y_values
        signal = [x_values, y_values]
        if channel_index is None or channel_index == i:
            # Create a pen for the channel.
            pen = pg.mkPen('g')
            # Plot only up to x1 = 1
            mask = x_values <= 10.1
            x_values = x_values[mask]
            y_values = y_values[mask]
            # print(len(x_values))
            self.signalgraph.plot(x_values, y_values, pen=pen)

        # Plot the first 1000 points
        # self.signalgraph.plot(x_values,y_values, 'g')
        # value=get_HzSampSlider_value
        # sample_and_plot(self, value)


def calculate_max_frequency(self):
    global max_frequency_hz, Ttime
    if not self.viewergraph.plotItem.listDataItems():
        # Check if there's any data on the viewergraph
        return
    x_values, y_values = self.viewergraph.plotItem.listDataItems()[0].getData()
    signal_fft = np.fft.fft(y_values)
    n = len(y_values)
    # total_time = x_values[-1] - x_values[0]
    frequencies = np.fft.fftfreq(n, Ttime / n)
    max_frequency_index = np.argmax(np.abs(signal_fft[1:])) + 1

# Calculate the corresponding frequency in Hertz
    max_frequency_hz = np.abs(frequencies[max_frequency_index])
    print("Maximum Frequency (Hz):", max_frequency_hz)


def Sampling(self, value):
    if self.Hz.isChecked():
        # value = self.HzSampSlider.value()
        sample_plot_Hz(self, value)
    else:
        # value = self.fmaxSampSlider.value()
        sample_and_plot(self, value)


def sample_and_plot(self, sample_rate):
    global SNR, y_normal, max_frequency_hz, Ttime, signal
    if not self.signalgraph.plotItem.listDataItems():
        return
    x_values, y_values = self.signalgraph.plotItem.listDataItems()[0].getData()
    fsamp = int(sample_rate * max_frequency_hz)
    print(max_frequency_hz)
    sampling_interval = 1 / fsamp

    # Create an array of time points for sampling
    sampled_arr = np.arange(x_values[0], x_values[-1], sampling_interval)

    samp_pts = np.interp(sampled_arr, x_values, y_values)
    reconst = ShannonInterpolation(samp_pts, sampled_arr, Ttime)
    if SNR == True:
        difference = y_normal - reconst
    else:
        difference = y_values - reconst

    self.samplesg.clear()
    self.signalgraph.clear()
    self.signalgraph.plot(x_values, y_values, pen='g')
    self.samplesg.plot(x_values, difference, pen='b', name=x_values)
    self.signalgraph.plot(sampled_arr, samp_pts, pen=None,
                          symbol='x', symbolPen='r', symbolBrush='b', symbolSize=10)
    self.reconstructedsg.clear()
    self.reconstructedsg.plot(reconst, pen='r', name=fsamp)
    # self.fmaxSampSlider_label.setText(f"fmaxSampSlider: {value}")


def plot_frequency_magnitude_phaseshift_signal(self):
    frequency = self.freq_slider.value()
    self.freq_label.setText(f"Frequency: {frequency}")
    magnitude = self.mag_slider.value()
    self.mag_label.setText(f"Magnitude: {magnitude}")
    phase_shift = self.phase_slider.value()*4
    self.phase_label.setText(f"Phase Shift: {phase_shift//4}")

    t = np.linspace(0, 1, num=1000)
    y = np.cos(2 * np.pi * frequency * magnitude * t + np.deg2rad(phase_shift))

    self.composergraph.clear()
    self.plotted = self.composergraph.plot(
        t, y, pen='b', name='Composer Signal')

    sine_waves = [y, frequency, phase_shift, magnitude]
    return sine_waves


def Delete_Signal(self, combobox):
    global wave_names, waves

    current_index = combobox.currentIndex()
    wave_name = wave_names[current_index]
    y_deleted = waves[wave_name]
    waves.pop(wave_name)
    wave_names.remove(wave_names[current_index])
    combobox.removeItem(current_index)

    if not wave_names:
        self.viewergraph.clear()
    else:
        x_values, y_viewer = self.viewergraph.plotItem.listDataItems()[
            0].getData()
        y_combined = y_viewer - y_deleted
        self.viewergraph.clear()
        self.viewergraph.plot(x_values, y_combined, pen='r')


def ShannonInterpolation(samp_pts, sampled_arr, Ttime):
    global output_magnitude
    # Check if the lengths of input_magnitude and input_time are not the same
    if len(samp_pts) != len(sampled_arr):
        print('not same')
        return  # If they are not the same, exit the function
    # Find the period T, assuming that input_time is equidistant (which is common)
    if len(sampled_arr) != 0:
        # Calculate the period (time difference between two adjacent samples)
        T = sampled_arr[1] - sampled_arr[0]
    # Create a matrix sincM that represents the differences between the original_time
    # and each sample time in input_time
    sincM = np.tile(Ttime, (len(sampled_arr), 1)) - \
        np.tile(sampled_arr[:, np.newaxis], (1, len(Ttime)))
    # Calculate the output_magnitude by performing dot product between input_magnitude
    # and the sinc function evaluated at sincM divided by the period T
    output_magnitude = np.dot(samp_pts, np.sinc(sincM/T))
    return output_magnitude  # Return the interpolated signal


def sample_signal(signal, frequency):
    # Get the x and y values from the plotted signal
    x = signal.xData
    y = signal.yData

    # Calculate the sampling interval based on the frequency
    sampling_interval = int(1/frequency)
    # period_length = int(len(x) / frequency)

    # Sample the signal
    sampled_x = x[::sampling_interval]
    sampled_y = y[::sampling_interval]

    return sampled_x, sampled_y


def sample_plot_Hz(self, value):
    print("dakhalet Hz")
    global sampled_x, sampled_y, frequency_HZ
    if not self.signalgraph.plotItem.listDataItems():
        return

    x_values, y_values = self.signalgraph.plotItem.listDataItems()[0].getData()

    # Get the frequency value from the slider
    frequency_HZ = value

    # Get the plotted signal
    signal = self.signalgraph.listDataItems()[0]

    # Calculate the sampling period based on the frequency
    sampling_period = frequency_HZ/1000

    # Sample the signal based on the sampling period
    sampled_x, sampled_y = sample_signal(signal, sampling_period)

    # Reconstruct the signal using the sampled points
    reconst = ShannonInterpolation(sampled_y, sampled_x, x_values)

    # Calculate the difference between the reconstructed and the original signal
    if SNR == True:
        difference = y_normal - reconst
    else:
        difference = y_values - reconst
    # Clear the plot widgets
    self.samplesg.clear()
    self.signalgraph.clear()
    self.reconstructedsg.clear()

    # Plot the difference on the second/middle graph
    self.samplesg.plot(x_values, difference, pen='b', name=difference)

    # Plot the original signal on the first graph
    self.signalgraph.plot(x_values, y_values, pen='g')

    # Plot the sampled points on the first graph
    self.signalgraph.plot(sampled_x, sampled_y, pen=None,
                          symbol='x', symbolPen='r', symbolBrush='b', symbolSize=10)

    # Plot the reconstructed signal on the last graph
    self.reconstructedsg.plot(x_values, reconst, pen='r', name=value)
