from pyqtgraph import PlotWidget
from PyQt5 import QtCore, QtGui, QtWidgets
import Functions


def initConnectors(self):
    self.SNRSlider = self.findChild(QtWidgets.QSlider, "SNRSlider")
    self.HzSampSlider = self.findChild(QtWidgets.QSlider, "HzSampSlider")
    self.fmaxSampSlider = self.findChild(QtWidgets.QSlider, "fmaxSampSlider")
    self.LoadButton = self.findChild(QtWidgets.QPushButton, "LoadButton")
    self.signalgraph = self.findChild(PlotWidget, "signalgraph")
    self.reconstructedsg = self.findChild(PlotWidget, "samplesg")
    self.samplesg = self.findChild(PlotWidget, "reconstructedsg")
    self.composergraph = self.findChild(PlotWidget, "composergraph")
    self.viewergraph = self.findChild(PlotWidget, "viewergraph")
    self.freq_slider = self.findChild(QtWidgets.QSlider, "freq_slider")
    self.mag_slider = self.findChild(QtWidgets.QSlider, "mag_slider")
    self.phase_slider = self.findChild(QtWidgets.QSlider, "phase_slider")
    self.viewbutton = self.findChild(QtWidgets.QPushButton, "viewbutton")
    self.deletebutton = self.findChild(QtWidgets.QPushButton, "deletebutton")
    self.savebutton = self.findChild(QtWidgets.QPushButton, "savebutton")
    self.transferbutton = self.findChild(
        QtWidgets.QPushButton, "transferbutton")
    self.signal_combobox = self.findChild(
        QtWidgets.QComboBox, "signal_combobox")
    self.FMax = self.findChild(QtWidgets.QRadioButton, "FMax")
    self.Hz = self.findChild(QtWidgets.QRadioButton, "Hz")

    graph_1_control = self.signalgraph.addLegend()
    graph_4_control = self.viewergraph.addLegend()

    graph_2_control = self.samplesg.addLegend()
    graph_3_control = self.reconstructedsg.addLegend()

    # self.viewbutton.clicked.connect(lambda: Functions.plot_composer_to_viewer(self))

    self.savebutton.clicked.connect(lambda: Functions.save_csv_file(self))
    self.savebutton.clicked.connect(
        lambda: Functions.calculate_max_frequency(self))
    self.transferbutton.clicked.connect(
        lambda: Functions.Transfer_and_plot(self))
    self.transferbutton.clicked.connect(
        lambda: Functions.calculate_max_frequency(self))
    # self.savebutton.clicked.connect(lambda: Functions.sample_and_plot(self,))

    self.SNRSlider.setRange(1, 20)
    self.SNRSlider.setValue(1)
    self.SNRSlider.valueChanged.connect(
        lambda value: Functions.increase_snr(self, value))

    self.LoadButton.clicked.connect(lambda: Functions.load(self))

    self.freq_slider.setRange(1, 20)
    self.freq_slider.setValue(1)
    self.freq_slider.valueChanged.connect(
        lambda: Functions.plot_frequency_magnitude_phaseshift_signal(self))

    self.mag_slider.setRange(1, 20)
    self.mag_slider.setValue(1)
    self.mag_slider.valueChanged.connect(
        lambda: Functions.plot_frequency_magnitude_phaseshift_signal(self))

    self.phase_slider.setRange(1, 20)
    self.phase_slider.setValue(1)
    self.phase_slider.valueChanged.connect(
        lambda: Functions.plot_frequency_magnitude_phaseshift_signal(self))

    self.deletebutton.clicked.connect(
        lambda: Functions.Delete_Signal(self, self.signal_combobox))

    self.viewbutton.clicked.connect(
        lambda: Functions.plot_composer_to_viewer(self, self.signal_combobox))

    self.Hz.toggled.connect(lambda: Functions.Sampling(
        self, self.HzSampSlider.value()))
    self.FMax.toggled.connect(lambda: Functions.Sampling(
        self, self.HzSampSlider.value()))

    self.HzSampSlider.setRange(1, 100)
    self.HzSampSlider.setValue(1)
    self.HzSampSlider.setSingleStep(1)
    self.HzSampSlider.valueChanged.connect(
        lambda: Functions.Sampling(self, self.HzSampSlider.value()))
