import sys
import os
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QGridLayout, QFileDialog,
    QComboBox
)

# Setup paths and imports
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))  # two levels up
sys.path.append(root_dir)

# Personal Files
from Justin_Work.App.caas import run_caas
from Justin_Work.App.default_cases import get_default_options, set_default_options
from Justin_Work.App.run_types import plot_bathy, run_bellhop

# UI Class
class TLViewerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bellhop UI")
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(screen.x() + 100, screen.y() + 100, screen.width() - 200, screen.height() - 200)
        self.setup_ui()

    # Import member functions
    run_caas = run_caas
    get_default_options = get_default_options
    set_default_options = set_default_options
    plot_bathy = plot_bathy
    run_bellhop = run_bellhop


    def setup_ui(self):
        self.layout = QGridLayout(self)

        # Field labels and entries
        self.fields = {
            "Bellhop Executable": QLineEdit(),
            "SSP File": QLineEdit(),
            "Bathymetry File": QLineEdit(),
            "Altimetry File": QLineEdit(),
            "Filename": QLineEdit(),
            "Data File Directory": QLineEdit(),
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
        txt_files = [os.path.splitext(f)[0] for f in os.listdir(os.path.join(os.getcwd(), "Justin_Work", "App", "default_runs")) if f.endswith(".txt")]
        self.default_dropdown.addItems(txt_files)
        default_button = QPushButton("Set Default")
        default_layout.addWidget(default_label, 0, 0)
        default_layout.addWidget(self.default_dropdown, 0, 1)
        default_layout.addWidget(default_button, 0, 2)
        default_layout.setColumnStretch(1, 1)
        self.layout.addLayout(default_layout, len(self.fields), 1, 1, 2)
        default_button.clicked.connect(self.get_default_options)

        # Run Button
        run_label = QLabel("Run Type:")
        run_layout = QGridLayout()
        self.run_type_dropdown = QComboBox()
        self.run_type_dropdown.addItems([
            "Run Bellhop",
            "Plot Bathymetry"
        ])
        run_button = QPushButton("Run")
        run_layout.addWidget(run_label, 0, 0)
        run_layout.addWidget(self.run_type_dropdown, 0, 1)
        run_layout.addWidget(run_button, 0, 2)
        run_layout.setColumnStretch(1, 1)
        self.layout.addLayout(run_layout, len(self.fields), 3, 1, 2)
        run_button.clicked.connect(self.select_run_type)


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


    def select_run_type(self):
        run_option = self.run_type_dropdown.currentText()
        if run_option == "Run Bellhop":
            self.run_bellhop()
        elif run_option == "Plot Bathymetry":
            self.plot_bathy()
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TLViewerApp()
    window.show()
    sys.exit(app.exec_())