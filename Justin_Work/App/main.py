import sys
import os
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QGridLayout, QMessageBox, QFileDialog,
    QComboBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Setup paths and imports
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))  # two levels up
sys.path.append(root_dir)
from Justin_Work.ray import Write_RAY, Read_RAY
from Justin_Work.tl import Write_TL, Read_TL
from pyat.pyat.readwrite import *
from Justin_Work.bathymetry import *

class Bathy_Canvas(FigureCanvas):
    def __init__(self, parent=None, file_path=None, width=8, height=6, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)
    
    def update_plot(self, x, y):
        self.plot_canvas.ax.clear()
        self.plot_canvas.ax.plot(x, y)
        self.plot_canvas.draw()

class TLViewerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transmission Loss App")
        self.setGeometry(100, 100, 1600, 800)
        self.setup_ui()

    def setup_ui(self):
        self.layout = QGridLayout()

        # Field labels and entries
        self.fields = {
            "Bellhop Executable": QLineEdit(),
            "SSP File": QLineEdit(),
            "Bathymetry File": QLineEdit(),
            "Altimetry File": QLineEdit(),
            "Filename": QLineEdit(),
            "Data File Directory": QLineEdit(),
            "Save File Directory": QLineEdit(),
            "Source Longitude": QLineEdit(),
            "Source Latitude": QLineEdit(),
            "Receiver Longitude": QLineEdit(),
            "Receiver Latitude": QLineEdit(),
            "Frequency": QLineEdit(),
            "SSPOPT(1)": QComboBox(),
            "SSPOPT(2)": QComboBox(),
            "SSPOPT(3)": QComboBox(),
            "SSPOPT(4)": QComboBox(),
            "SSPOPT(5)": QComboBox(),
            "Surface Height": QLineEdit(),
            "Surface Compressional Speed": QLineEdit(),
            "Surface Shear Speed": QLineEdit(),
            "Surface Density": QLineEdit(),
            "Surface Attenuation": QLineEdit(),
            "Bottom Type": QLineEdit(),
            "Include Bathymetry": QLineEdit(),
            "Roughness": QLineEdit(),
            "Bottom Height": QLineEdit(),
            "Bottom Compressional Speed": QLineEdit(),
            "Bottom Shear Speed": QLineEdit(),
            "Bottom Density": QLineEdit(),
            "Bottom Attenuation": QLineEdit(),
            "Number of Source Depths": QLineEdit(),
            "Source Depths": QLineEdit(),
            "Number of Receiver Depths": QLineEdit(),
            "Receiver Depths": QLineEdit(),
            "Number of Receiver Ranges": QLineEdit(),
            "Receiver Ranges": QLineEdit(),
            "Ray Compute Type": QLineEdit(),
            "Number of Beams": QLineEdit(),
            "Launch Angles": QLineEdit(),
            "Step Size": QLineEdit()
        }
        line = -1
        for i, (label_text, line_edit) in enumerate(self.fields.items()):
            # Ordering the rows and columns
            j = i % 14
            if i % 14 == 0:
                line += 1
            # Custom buttons for each option
            if label_text == "Bellhop Executable":
                browse_button = QPushButton("Browse")
                browse_button.clicked.connect(self.browse_bellhop_executable)
                bellhop_layout = QGridLayout()
                label = QLabel(label_text)
                bellhop_layout.addWidget(label, 0, 0)
                bellhop_layout.addWidget(line_edit, 0, 1)
                bellhop_layout.addWidget(browse_button, 0, 2)
                self.layout.addLayout(bellhop_layout, j, 2 * line, 1, 2) 
            elif label_text == "SSP File":
                ssp_browse = QPushButton("Browse")
                ssp_browse.clicked.connect(self.browse_ssp_mat)
                ssp_layout = QGridLayout()
                label = QLabel(label_text)
                ssp_layout.addWidget(label, 0, 0)
                ssp_layout.addWidget(line_edit, 0, 1)
                ssp_layout.addWidget(ssp_browse, 0, 2)
                self.layout.addLayout(ssp_layout, j, 2 * line, 1, 2)
            elif label_text == "Bathymetry File":
                bty_browse = QPushButton("Browse")
                bty_browse.clicked.connect(self.browse_bty_mat)
                bty_layout = QGridLayout()
                label = QLabel(label_text)
                bty_layout.addWidget(label, 0, 0)
                bty_layout.addWidget(line_edit, 0, 1)
                bty_layout.addWidget(bty_browse, 0, 2)
                self.layout.addLayout(bty_layout, j, 2 * line, 1, 2)
            elif label_text == "Altimetry File":
                alt_browse = QPushButton("Browse")
                alt_browse.clicked.connect(self.browse_alt_mat)
                alt_layout = QGridLayout()
                label = QLabel(label_text)
                alt_layout.addWidget(label, 0, 0)
                alt_layout.addWidget(line_edit, 0, 1)
                alt_layout.addWidget(alt_browse, 0, 2)
                self.layout.addLayout(alt_layout, j, 2 * line, 1, 2)
            elif label_text == "Filename":
                filename_layout = QGridLayout()
                label = QLabel(label_text)
                filename_layout.addWidget(label, 0, 0)
                filename_layout.addWidget(line_edit, 0, 1)
                filename_layout.addWidget(QLabel("(no extensions included)"), 0, 2)
                self.layout.addLayout(filename_layout, j, 2 * line, 1, 2) 
            elif label_text == "Data File Directory":
                df_browse = QPushButton("Browse")
                df_browse.clicked.connect(self.browse_df_dir)
                df_layout = QGridLayout()
                label = QLabel(label_text)
                df_layout.addWidget(label, 0, 0)
                df_layout.addWidget(line_edit, 0, 1)
                df_layout.addWidget(df_browse, 0, 2)
                self.layout.addLayout(df_layout, j, 2 * line, 1, 2)
            elif label_text == "Save File Directory":
                sf_browse = QPushButton("Browse")
                sf_browse.clicked.connect(self.browse_sf_dir)
                sf_layout = QGridLayout()
                label = QLabel(label_text)
                sf_layout.addWidget(label, 0, 0)
                sf_layout.addWidget(line_edit, 0, 1)
                sf_layout.addWidget(sf_browse, 0, 2)
                self.layout.addLayout(sf_layout, j, 2 * line, 1, 2)
            elif label_text == "Source Longitude":
                slong_layout = QGridLayout()
                label = QLabel(label_text)
                slong_layout.addWidget(label, 0, 0)
                slong_layout.addWidget(line_edit, 0, 1)
                self.layout.addLayout(slong_layout, j, 2 * line, 1, 2)
            elif label_text == "Source Latitude": 
                slat_layout = QGridLayout()
                label = QLabel(label_text)
                slat_layout.addWidget(label, 0, 0)
                slat_layout.addWidget(line_edit, 0, 1)
                self.layout.addLayout(slat_layout, j, 2 * line, 1, 2)
            elif label_text == "Receiver Longitude":
                rlong_layout = QGridLayout()
                label = QLabel(label_text)
                rlong_layout.addWidget(label, 0, 0)
                rlong_layout.addWidget(line_edit, 0, 1)
                self.layout.addLayout(rlong_layout, j, 2 * line, 1, 2)
            elif label_text == "Receiver Latitude":
                rlat_layout = QGridLayout()
                label = QLabel(label_text)
                rlat_layout.addWidget(label, 0, 0)
                rlat_layout.addWidget(line_edit, 0, 1)
                self.layout.addLayout(rlat_layout, j, 2 * line, 1, 2)
            elif label_text == "Frequency":
                freq_layout = QGridLayout()
                label = QLabel(label_text)
                freq_layout.addWidget(label, 0, 0)
                freq_layout.addWidget(line_edit, 0, 1)
                freq_layout.addWidget(QLabel("(Hz)"), 0, 2)
                self.layout.addLayout(freq_layout, j, 2 * line, 1, 2)
            elif label_text == "SSPOPT(1)":
                sspopt1_layout = QGridLayout()
                sspopt1_dropdown = QComboBox()
                sspopt1_dropdown.addItems(["S: Cubic Spline Interpolation", "C: C-linear interpolation", "N: N2-line Interpolation", "A: Analytic Interpolation", "Q: Quadratic Approximation"])
                self.fields[label_text] = sspopt1_dropdown
                widget = self.fields[label_text]
                label = QLabel(label_text)
                sspopt1_layout.addWidget(label, 0, 0)
                sspopt1_layout.addWidget(widget, 0, 1)
                sspopt1_layout.setColumnStretch(1, 1)
                self.layout.addLayout(sspopt1_layout, j, 2 * line, 1, 2)
            elif label_text == "SSPOPT(2)":
                sspopt2_layout = QGridLayout()
                sspopt2_dropdown = QComboBox()
                sspopt2_dropdown.addItems(["V: Vacuum above surface (SURFACE-LINE not required)", "R: Perfectly rigid media above surface", "A: Acoustic half-space (Surface information required)", "F: Read a list of reflection coefficients from *.irc file"])
                self.fields[label_text] = sspopt2_dropdown
                widget = self.fields[label_text]
                label = QLabel(label_text)
                sspopt2_layout.addWidget(label, 0, 0)
                sspopt2_layout.addWidget(widget, 0, 1)
                sspopt2_layout.setColumnStretch(1, 1)
                self.layout.addLayout(sspopt2_layout, j, 2 * line, 1, 2)
            elif label_text == "SSPOPT(3)":
                sspopt3_layout = QGridLayout()
                sspopt3_dropdown = QComboBox()
                sspopt3_dropdown.addItems(["F: attenuation corresponds to (dB/m)kHz", "L: attenuation corresponds to parameter loss", "M: attenuation corresponds to dB/m", "N: attenuation corresponds to Nepers/m", "Q: attenuation corresponds to a Q-factor", "W: attenuation corresponds to dB/wavelength"])
                self.fields[label_text] = sspopt3_dropdown
                widget = self.fields[label_text]
                label = QLabel(label_text)
                sspopt3_layout.addWidget(label, 0, 0)
                sspopt3_layout.addWidget(widget, 0, 1)
                sspopt3_layout.setColumnStretch(1, 1)
                self.layout.addLayout(sspopt3_layout, j, 2 * line, 1, 2)
            elif label_text == "SSPOPT(4)":
                sspopt4_layout = QGridLayout()
                sspopt4_dropdown = QComboBox()
                sspopt4_dropdown.addItems(["' ': Default parameter", "T: Opptional parameter for Thorpe volume attenuation"])
                self.fields[label_text] = sspopt4_dropdown
                widget = self.fields[label_text]
                label = QLabel(label_text)
                sspopt4_layout.addWidget(label, 0, 0)
                sspopt4_layout.addWidget(widget, 0, 1)
                sspopt4_layout.setColumnStretch(1, 1)
                self.layout.addLayout(sspopt4_layout, j, 2 * line, 1, 2)
            elif label_text == "SSPOPT(5)":
                sspopt5_layout = QGridLayout()
                sspopt5_dropdown = QComboBox()
                sspopt5_dropdown.addItems(["*: Use if including an *.ati file for surface shape", "' ': No Altimetry"])
                self.fields[label_text] = sspopt5_dropdown
                widget = self.fields[label_text]
                label = QLabel(label_text)
                sspopt5_layout.addWidget(label, 0, 0)
                sspopt5_layout.addWidget(widget, 0, 1)
                sspopt5_layout.setColumnStretch(1, 1)
                self.layout.addLayout(sspopt5_layout, j, 2 * line, 1, 2)
            elif label_text == "Surface Height":
                sh_layout = QGridLayout()
                label = QLabel(label_text)
                sh_layout.addWidget(label, 0, 0)
                sh_layout.addWidget(line_edit, 0, 1)
                sh_layout.addWidget(QLabel("(m)"), 0, 2)
                self.layout.addLayout(sh_layout, j, 2 * line, 1, 2) 
            elif label_text == "Surface Compressional Speed":
                scs_layout = QGridLayout()
                label = QLabel(label_text)
                scs_layout.addWidget(label, 0, 0)
                scs_layout.addWidget(line_edit, 0, 1)
                scs_layout.addWidget(QLabel("(m/s)"), 0, 2)
                self.layout.addLayout(scs_layout, j, 2 * line, 1, 2) 
            elif label_text == "Surface Shear Speed": 
                sss_layout = QGridLayout()
                label = QLabel(label_text)
                sss_layout.addWidget(label, 0, 0)
                sss_layout.addWidget(line_edit, 0, 1)
                sss_layout.addWidget(QLabel("(m/s)"), 0, 2)
                self.layout.addLayout(sss_layout, j, 2 * line, 1, 2) 
            elif label_text == "Surface Density":
                sp_layout = QGridLayout()
                label = QLabel(label_text)
                sp_layout.addWidget(label, 0, 0)
                sp_layout.addWidget(line_edit, 0, 1)
                sp_layout.addWidget(QLabel("(g/cm^3)"), 0, 2)
                self.layout.addLayout(sp_layout, j, 2 * line, 1, 2) 
            elif label_text == "Surface Attenuation":
                sa_layout = QGridLayout()
                label = QLabel(label_text)
                sa_layout.addWidget(label, 0, 0)
                sa_layout.addWidget(line_edit, 0, 1)
                sa_layout.addWidget(QLabel("(units specified with SSPOPT(3))"), 0, 2)
                self.layout.addLayout(sa_layout, j, 2 * line, 1, 2) 
            elif label_text == "Bottom Type": 
                bt_layout = QGridLayout()
                bt_dropdown = QComboBox()
                bt_dropdown.addItems(["V: Vacuum below water column", "R: rigid below water column", "A: acoustic half-space below water column (need BOTTOM-LINE)", "F: read list of reflection coefficients from *.brc file"])
                self.fields[label_text] = bt_dropdown
                widget = self.fields[label_text]
                label = QLabel(label_text)
                bt_layout.addWidget(label, 0, 0)
                bt_layout.addWidget(widget, 0, 1)
                bt_layout.setColumnStretch(1, 1)
                self.layout.addLayout(bt_layout, j, 2 * line, 1, 2)
            elif label_text == "Include Bathymetry":
                bt_layout2 = QGridLayout()
                bt_dropdown2 = QComboBox()
                bt_dropdown2.addItems(["' ': No bathymetry file", "*: include if wanting to use a *.bty file"])
                self.fields[label_text] = bt_dropdown2
                widget = self.fields[label_text]
                label = QLabel(label_text)
                bt_layout2.addWidget(label, 0, 0)
                bt_layout2.addWidget(widget, 0, 1)
                bt_layout2.setColumnStretch(1, 1)
                self.layout.addLayout(bt_layout2, j, 2 * line, 1, 2)
            elif label_text == "Roughness": 
                rough_layout = QGridLayout()
                label = QLabel(label_text)
                rough_layout.addWidget(label, 0, 0)
                rough_layout.addWidget(line_edit, 0, 1)
                self.layout.addLayout(rough_layout, j, 2 * line, 1, 2)
            elif label_text == "Bottom Height":
                bh_layout = QGridLayout()
                label = QLabel(label_text)
                bh_layout.addWidget(label, 0, 0)
                bh_layout.addWidget(line_edit, 0, 1)
                self.layout.addLayout(bh_layout, j, 2 * line, 1, 2)
            elif label_text == "Bottom Compressional Speed":
                bcs_layout = QGridLayout()
                label = QLabel(label_text)
                bcs_layout.addWidget(label, 0, 0)
                bcs_layout.addWidget(line_edit, 0, 1)
                self.layout.addLayout(bcs_layout, j, 2 * line, 1, 2)
            elif label_text == "Bottom Shear Speed":
                bss_layout = QGridLayout()
                label = QLabel(label_text)
                bss_layout.addWidget(label, 0, 0)
                bss_layout.addWidget(line_edit, 0, 1)
                self.layout.addLayout(bss_layout, j, 2 * line, 1, 2)
            elif label_text == "Bottom Density":
                bp_layout = QGridLayout()
                label = QLabel(label_text)
                bp_layout.addWidget(label, 0, 0)
                bp_layout.addWidget(line_edit, 0, 1)
                self.layout.addLayout(bp_layout, j, 2 * line, 1, 2)
            elif label_text == "Bottom Attenuation":
                ba_layout = QGridLayout()
                label = QLabel(label_text)
                ba_layout.addWidget(label, 0, 0)
                ba_layout.addWidget(line_edit, 0, 1)
                self.layout.addLayout(ba_layout, j, 2 * line, 1, 2)
            elif label_text == "Number of Source Depths":
                nsd_layout = QGridLayout()
                label = QLabel(label_text)
                nsd_layout.addWidget(label, 0, 0)
                nsd_layout.addWidget(line_edit, 0, 1)
                self.layout.addLayout(nsd_layout, j, 2 * line, 1, 2)
            elif label_text == "Source Depths":
                sd_layout = QGridLayout()
                label = QLabel(label_text)
                sd_layout.addWidget(label, 0, 0)
                sd_layout.addWidget(line_edit, 0, 1)
                self.layout.addLayout(sd_layout, j, 2 * line, 1, 2)
            elif label_text == "Number of Receiver Depths":
                nrd_layout = QGridLayout()
                label = QLabel(label_text)
                nrd_layout.addWidget(label, 0, 0)
                nrd_layout.addWidget(line_edit, 0, 1)
                self.layout.addLayout(nrd_layout, j, 2 * line, 1, 2)
            elif label_text == "Receiver Depths":
                rd_layout = QGridLayout()
                label = QLabel(label_text)
                rd_layout.addWidget(label, 0, 0)
                rd_layout.addWidget(line_edit, 0, 1)
                self.layout.addLayout(rd_layout, j, 2 * line, 1, 2)
            elif label_text == "Number of Receiver Ranges":
                nrr_layout = QGridLayout()
                label = QLabel(label_text)
                nrr_layout.addWidget(label, 0, 0)
                nrr_layout.addWidget(line_edit, 0, 1)
                self.layout.addLayout(nrr_layout, j, 2 * line, 1, 2)
            elif label_text == "Receiver Ranges": 
                rr_layout = QGridLayout()
                label = QLabel(label_text)
                rr_layout.addWidget(label, 0, 0)
                rr_layout.addWidget(line_edit, 0, 1)
                self.layout.addLayout(rr_layout, j, 2 * line, 1, 2)
            elif label_text == "Ray Compute Type": 
                rct_layout = QGridLayout()
                rct_dropdown = QComboBox()
                rct_dropdown.addItems(["A: Write amplitude and travel times", "E: Write Eigenray coordinates", "R: Write ray coordinates", "C: Write coherent acoustic pressure", "I: Write incoherent acoustic pressure", "S: Write semi-coherent acoustic pressure"])
                self.fields[label_text] = rct_dropdown
                widget = self.fields[label_text]
                label = QLabel(label_text)
                rct_layout.addWidget(label, 0, 0)
                rct_layout.addWidget(widget, 0, 1)
                rct_layout.setColumnStretch(1, 1)
                self.layout.addLayout(rct_layout, j, 2 * line, 1, 2)
            elif label_text == "Number of Beams": 
                nb_layout = QGridLayout()
                label = QLabel(label_text)
                nb_layout.addWidget(label, 0, 0)
                nb_layout.addWidget(line_edit, 0, 1)
                self.layout.addLayout(nb_layout, j, 2 * line, 1, 2)
            elif label_text == "Launch Angles": 
                la_layout = QGridLayout()
                label = QLabel(label_text)
                la_layout.addWidget(label, 0, 0)
                la_layout.addWidget(line_edit, 0, 1)
                self.layout.addLayout(la_layout, j, 2 * line, 1, 2)
            elif label_text == "Step Size": 
                ss_layout = QGridLayout()
                label = QLabel(label_text)
                ss_layout.addWidget(label, 0, 0)
                ss_layout.addWidget(line_edit, 0, 1)
                ss_layout.addWidget(QLabel("(m)"), 0, 2)
                self.layout.addLayout(ss_layout, j, 2 * line, 1, 2)
            else:
                continue

        # Default Options Button
        default_label = QLabel("Default Options:")
        default_layout = QGridLayout()
        self.default_dropdown = QComboBox()
        self.default_dropdown.addItems([
            "Eigenrays",
            "Transmission Loss"
        ])
        default_button = QPushButton("Set Default")
        default_layout.addWidget(default_label, 0, 0)
        default_layout.addWidget(self.default_dropdown, 0, 1)
        default_layout.addWidget(default_button, 0, 2)
        default_layout.setColumnStretch(1, 1)
        self.layout.addLayout(default_layout, len(self.fields), 2, 1, 2)
        default_button.clicked.connect(self.set_default_options)

        # Run Button
        run_button = QPushButton("Run")
        run_button.clicked.connect(self.run)
        self.layout.addWidget(run_button, len(self.fields), 4, 1, 2)

        self.setLayout(self.layout)

    def browse_bellhop_executable(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Bellhop Executable")
        if file_path:
            self.fields["Bellhop Executable"].setText(file_path)
    
    def browse_ssp_mat(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select SSP .mat File")
        if file_path:
            self.fields["SSP File"].setText(file_path)

    def browse_bty_mat(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select BTY .mat File")
        if file_path:
            self.fields["Bathymetry File"].setText(file_path)

    def browse_alt_mat(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select ALT .mat File")
        if file_path:
            self.fields["Altimetry File"].setText(file_path)

    def browse_df_dir(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Data File Directory")
        if directory:
            self.fields["Data File Directory"].setText(directory)

    def browse_sf_dir(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Save File Directory")
        if directory:
            self.fields["Save File Directory"].setText(directory)

    def set_default_options(self):
        # Set default options based on the selected default
        default_option = self.default_dropdown.currentText()
        if default_option == "Eigenrays":
            self.fields["Bellhop Executable"].setText(os.path.join(os.getcwd(), "Justin_Work/App/bellhop_exe/bellhopcxx"))
            self.fields["SSP File"].setText(os.path.join(os.getcwd(), "Justin_Work/App/bty_ssp_ati/ssp.mat"))
            self.fields["Bathymetry File"].setText(os.path.join(os.getcwd(), "Justin_Work/App/bty_ssp_ati/bty.mat"))
            self.fields["Altimetry File"].setText(os.path.join(os.getcwd(), "Justin_Work/App/bty_ssp_ati/ati.mat"))
            self.fields["Filename"].setText("run_eigenrays_3500")
            self.fields["Data File Directory"].setText(os.path.join(os.getcwd(), "Justin_Work/App/runs/"))
            self.fields["Save File Directory"].setText(os.path.join(os.getcwd(), "Justin_Work/App/run_saves/"))
            self.fields["Source Longitude"].setText("-122.83")
            self.fields["Source Latitude"].setText("47.77")
            self.fields["Receiver Longitude"].setText("-122.85")
            self.fields["Receiver Latitude"].setText("47.71")
            self.fields["Frequency"].setText("3500.0")
            self.fields["SSPOPT(1)"].setCurrentText("S: Cubic Spline Interpolation")
            self.fields["SSPOPT(2)"].setCurrentText("V: Vacuum above surface (SURFACE-LINE not required)")
            self.fields["SSPOPT(3)"].setCurrentText("F: attenuation corresponds to (dB/m)kHz")
            self.fields["SSPOPT(4)"].setCurrentText("' ': Default parameter")   
            self.fields["SSPOPT(5)"].setCurrentText("*: Use if including an *.ati file for surface shape")
            self.fields["Surface Height"].setText("0.0")
            self.fields["Surface Compressional Speed"].setText("343.0")
            self.fields["Surface Shear Speed"].setText("0.0")
            self.fields["Surface Density"].setText("1.2")
            self.fields["Surface Attenuation"].setText("0.0")
            self.fields["Bottom Type"].setCurrentText("A: acoustic half-space below water column (need BOTTOM-LINE)")
            self.fields["Include Bathymetry"].setCurrentText("*: include if wanting to use a *.bty file")
            self.fields["Roughness"].setText("0.0")
            self.fields["Bottom Height"].setText("0.0")
            self.fields["Bottom Compressional Speed"].setText("1600.0")
            self.fields["Bottom Shear Speed"].setText("0.0")
            self.fields["Bottom Density"].setText("1.8")
            self.fields["Bottom Attenuation"].setText("0.0")
            self.fields["Number of Source Depths"].setText("1")
            self.fields["Source Depths"].setText("20.0")
            self.fields["Number of Receiver Depths"].setText("1")
            self.fields["Receiver Depths"].setText("20.0")
            self.fields["Number of Receiver Ranges"].setText("1")
            self.fields["Receiver Ranges"].setText("0.0")
            self.fields["Ray Compute Type"].setCurrentText("E: Write Eigenray coordinates")
            self.fields["Number of Beams"].setText("1001")
            self.fields["Launch Angles"].setText("-89.0, 89.0")
            self.fields["Step Size"].setText("10.0")
            # Plot bathymetry
            file_path = self.fields["Bathymetry File"].text()
            if file_path:
                try:
                    # self.plot_canvas = Bathy_Canvas(self, file_path=file_path, width=8, height=6, dpi=300)
                    # self.layout.addWidget(self.plot_canvas, 0, 6, 24, 10)
                    # self.plot_canvas.update_plot(np.linspace(0, 10, 100), np.random.rand(100))  # Example data
                    return
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to plot bathymetry: {e}")
        elif default_option == "Transmission Loss":
            self.fields["Bellhop Executable"].setText(os.path.join(os.getcwd(), "Justin_Work/App/bellhop_exe/bellhopcxx"))
            self.fields["SSP File"].setText(os.path.join(os.getcwd(), "Justin_Work/App/bty_ssp_ati/ssp.mat"))
            self.fields["Bathymetry File"].setText(os.path.join(os.getcwd(), "Justin_Work/App/bty_ssp_ati/bty.mat"))
            self.fields["Altimetry File"].setText(os.path.join(os.getcwd(), "Justin_Work/App/bty_ssp_ati/ati.mat"))
            self.fields["Filename"].setText("run_tl_3500")
            self.fields["Data File Directory"].setText(os.path.join(os.getcwd(), "Justin_Work/App/runs/"))
            self.fields["Save File Directory"].setText(os.path.join(os.getcwd(), "Justin_Work/App/run_saves/"))
            self.fields["Source Longitude"].setText("-122.83")
            self.fields["Source Latitude"].setText("47.77")
            self.fields["Receiver Longitude"].setText("-122.85")
            self.fields["Receiver Latitude"].setText("47.71") 
            self.fields["Frequency"].setText("3500.0")
            self.fields["SSPOPT(1)"].setCurrentText("S: Cubic Spline Interpolation")
            self.fields["SSPOPT(2)"].setCurrentText("V: Vacuum above surface (SURFACE-LINE not required)")
            self.fields["SSPOPT(3)"].setCurrentText("F: attenuation corresponds to (dB/m)kHz")
            self.fields["SSPOPT(4)"].setCurrentText("' ': Default parameter")   
            self.fields["SSPOPT(5)"].setCurrentText("*: Use if including an *.ati file for surface shape")
            self.fields["Surface Height"].setText("0.0")
            self.fields["Surface Compressional Speed"].setText("343.0")
            self.fields["Surface Shear Speed"].setText("0.0")
            self.fields["Surface Density"].setText("1.2")
            self.fields["Surface Attenuation"].setText("0.0")
            self.fields["Bottom Type"].setCurrentText("A: acoustic half-space below water column (need BOTTOM-LINE)")
            self.fields["Include Bathymetry"].setCurrentText("*: include if wanting to use a *.bty file")
            self.fields["Roughness"].setText("0.0")
            self.fields["Bottom Height"].setText("0.0")
            self.fields["Bottom Compressional Speed"].setText("1600.0")
            self.fields["Bottom Shear Speed"].setText("0.0")
            self.fields["Bottom Density"].setText("1.8")
            self.fields["Bottom Attenuation"].setText("0.0")
            self.fields["Number of Source Depths"].setText("1")
            self.fields["Source Depths"].setText("20.0")
            self.fields["Number of Receiver Depths"].setText("201")
            self.fields["Receiver Depths"].setText("0.0, 200.0")
            self.fields["Number of Receiver Ranges"].setText("501")
            self.fields["Receiver Ranges"].setText("0.0, 7.0")
            self.fields["Ray Compute Type"].setCurrentText("C: Write coherent acoustic pressure")
            self.fields["Number of Beams"].setText("0")
            self.fields["Launch Angles"].setText("-89.0, 89.0")
            self.fields["Step Size"].setText("0.0")
            # Plot bathymetry
            file_path = self.fields["Bathymetry File"].text()
            if file_path:
                try:
                    # self.plot_canvas = Bathy_Canvas(self, file_path=file_path, width=8, height=6, dpi=300)
                    # self.plot_canvas.update_plot(np.linspace(0, 10, 100), np.random.rand(100))  # Example data
                    # self.layout.addWidget(self.plot_canvas, 0, 6, 24, 10)
                    return
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to plot bathymetry: {e}")
    
    def plot_bathymetry(self, file_path):
        return

    def run(self):
        # Read and convert input values
        values = {
            name: line_edit.text()
            for name, line_edit in self.fields.items()
        }

        bellhop_executable = self.fields["Bellhop Executable"].text()
        ssp_file = self.fields["SSP File"].text()
        bathy_file = self.fields["Bathymetry File"].text()
        alt_file = self.fields["Altimetry File"].text()
        filename = self.fields["Filename"].text()
        data_dir = self.fields["Data File Directory"].text()
        save_dir = self.fields["Save File Directory"].text()   
        lon_start = values["Start Longitude"]
        lat_start = values["Start Latitude"]
        lon_end   = values["End Longitude"]
        lat_end   = values["End Latitude"]
        freq      = values["Frequency"]
        sspopt1 = self.fields["SSPOPT(1)"].currentText().split(":")[0].strip()
        sspopt2 = self.fields["SSPOPT(2)"].currentText().split(":")[0].strip()
        sspopt3 = self.fields["SSPOPT(3)"].currentText().split(":")[0].strip()
        sspopt4 = self.fields["SSPOPT(4)"].currentText().split(":")[0].strip()
        sspopt5 = self.fields["SSPOPT(5)"].currentText().split(":")[0].strip()
        surface_height = values["Surface Height (m)"]
        surface_compressional_speed = values["Surface Compressional Speed"]
        surface_shear_speed = values["Surface Shear Speed"]
        surface_density = values["Surface Density"]
        surface_attenuation = values["Surface Attenuation"]
        bottom_type = self.fields["Bottom Type"].currentText().split(":")[0].strip()
        include_bathymetry = self.fields["Include Bathymetry"].currentText().split(":")[0].strip()
        roughness = values["Roughness"]
        bottom_height = values["Bottom Height"]
        bottom_compressional_speed = values["Bottom Compressional Speed"]
        bottom_shear_speed = values["Bottom Shear Speed"]             
        bottom_density = values["Bottom Density"]
        bottom_attenuation = values["Bottom Attenuation"]
        num_source_depths = int(values["Number of Source Depths"])
        source_depths = np.array([float(x) for x in self.fields["Source Depths"].text().split(",")])
        num_receiver_depths = int(values["Number of Receiver Depths"])
        receiver_depths = np.array([float(x) for x in self.fields["Receiver Depths"].text().split(",")])
        num_receiver_ranges = int(values["Number of Receiver Ranges"])
        receiver_ranges = np.array([float(x) for x in self.fields["Receiver Ranges"].text().split(",")])
        ray_compute_type = self.fields["Ray Compute Type"].currentText().split(":")[0].strip()
        num_beams = int(values["Number of Beams"])
        launch_angles = np.array([float(x) for x in self.fields["Launch Angles"].text().split(",")])
        step_size = values["Step Size"]



        shot_1_ray = Write_RAY(dir=data_dir, 
                               filename=filename, 
                               ssp_depths=ssp_depths,
                               ssp=ssp,
                               bath_ranges=bath_ranges,
                               bath_depths=bath_depths,
                               ati_depths=ati_depths,
                               freq=freq,
                               nmedia=1,
                               sspopt=[sspopt1, 
                                       sspopt2, 
                                       sspopt3, 
                                       sspopt4, 
                                       sspopt5],
                               surface_opt=[float(surface_height),
                                            float(surface_compressional_speed),
                                            float(surface_shear_speed),
                                            float(surface_density),
                                            float(surface_attenuation)],
                               bottom_type=[bottom_type,
                                            include_bathymetry],
                               roughness=roughness,
                               bottom_opt=[float(bottom_height),
                                           float(bottom_compressional_speed),
                                           float(bottom_shear_speed),
                                           float(bottom_density),
                                           float(bottom_attenuation)],
                               nsd=nsd,
                               sd=sd,
                               nrd=nrd,
                               rd=rd,
                               nrr=nrr, 
                               rr=rr,
                               ray_compute=ray_compute,
                               num_beams=num_beams,
                               launch_angles=launch_angles,
                               step_size=step_size,
                               max_depth=max_depth,
                               max_range=max_range,
                               opt4=opt4,
                               pair=pair)
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TLViewerApp()
    window.show()
    sys.exit(app.exec_())