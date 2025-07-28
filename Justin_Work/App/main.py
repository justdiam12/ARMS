import sys
import os
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QGridLayout, QMessageBox, QFileDialog
)

# Setup paths and imports
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))  # two levels up
sys.path.append(root_dir)

from Justin_Work.tl import Write_TL, Read_TL
from pyat.pyat.readwrite import *
from Justin_Work.bathymetry import *

# Run function (simulate pressure field)
def run(filepath, lon_start, lat_start, lon_end, lat_end, freq, ssp, ssp_depths):
    bath_map, lon_range, lat_range = map_2D()
    profile, distances = map_1D(bath_map, lon_range, lat_range, lon_start, lon_end, lat_start, lat_end, num_points=1000)

    run_tl = Write_TL(
        dir="/Users/justindiamond/Documents/Documents/UW-APL/Research/ARMS/Justin_Work/App/runs/",
        filename="run_" + str(int(freq)),
        ssp_depths=ssp_depths,
        ssp=ssp,
        bath_ranges=distances,
        bath_depths=profile,
        freq=freq,
        nmedia=1,
        sspopt="CVW",
        bottom_type="A*",
        roughness=0.0,
        bottom_depth=max(profile),
        bottom_ss=1600.0,
        bottom_alpha=0.0,
        bottom_rho=1.8,
        bottom_shear=0.0,
        nsd=1,
        sd=[20.0],
        nrd=201,
        rd=[0.0, 200.0],
        nrr=501,
        rr=[0.0, max(profile)],
        ray_compute="C",
        num_beams=0,
        launch_angles=[-89.0, 89.0],
        step_size=0.0,
        max_depth=max(profile) + 5,
        max_range=max(distances) + 1
    )

    run_tl.write_files()

    os.system(
        "/Users/justindiamond/Documents/Documents/UW-APL/Research/ARMS/bellhopcuda/bin/bellhopcxx -2D /Users/justindiamond/Documents/Documents/UW-APL/Research/ARMS/App/runs/run_"
        + str(int(freq))
    )

    run_tl_plot = Read_TL(
        directory="/Users/justindiamond/Documents/Documents/UW-APL/Research/ARMS/Justin_Work/App/runs/",
        output_directory="/Users/justindiamond/Documents/Documents/UW-APL/Research/ARMS/Justin_Work/App/run_saves/",
        tl_file="run_" + str(int(freq)),
        freq=freq,
        bath_ranges=distances
    )

    [_, _, _, _, _, pressure] = run_tl_plot.read_shd()
    return pressure


class TLViewerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transmission Loss App")
        self.setGeometry(100, 100, 1400, 600)
        self.setup_ui()

    def setup_ui(self):
        layout = QGridLayout()

        # Field labels and entries
        self.fields = {
            "Bellhop Executable": QLineEdit(),
            "Source Longitude": QLineEdit(),
            "Source Latitude": QLineEdit(),
            "Receiver Longitude": QLineEdit(),
            "Receiver Latitude": QLineEdit(),
            "Frequency (Hz)": QLineEdit(),
            "SSPOPT(1)": QLineEdit(),
            "SSPOPT(2)": QLineEdit(),
            "SSPOPT(3)": QLineEdit(),
            "SSPOPT(4)": QLineEdit(),
            "SSPOPT(5)": QLineEdit(),
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
            "Step Size (m)": QLineEdit()
        }
        line = -1
        for i, (label_text, line_edit) in enumerate(self.fields.items()):
            # Ordering the rows and columns
            j = i % 10
            if i % 10 == 0:
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
                layout.addLayout(bellhop_layout, j, 2 * line, 1, 2) 
            elif label_text == "Source Longitude":
                continue
            elif label_text == "Source Latitude": 
                continue
            elif label_text == "Receiver Longitude":
                continue
            elif label_text == "Receiver Latitude":
                continue
            elif label_text == "Frequency (Hz)":
                continue
            elif label_text == "SSPOPT(1)":
                continue
            elif label_text == "SSPOPT(2)":
                continue
            elif label_text == "SSPOPT(3)":
                continue
            elif label_text == "SSPOPT(4)":
                continue
            elif label_text == "SSPOPT(5)":
                continue
            elif label_text == "Surface Height":
                continue
            elif label_text == "Surface Compressional Speed":
                continue 
            elif label_text == "Surface Shear Speed": 
                continue
            elif label_text == "Surface Density":
                continue
            elif label_text == "Surface Attenuation":
                continue
            elif label_text == "Bottom Type": 
                continue
            elif label_text == "Include Bathymetry":
                continue
            elif label_text == "Roughness": 
                continue
            elif label_text == "Bottom Height":
                continue
            elif label_text == "Bottom Compressional Speed":
                continue
            elif label_text == "Bottom Shear Speed":
                continue
            elif label_text == "Bottom Density":
                continue
            elif label_text == "Bottom Attenuation":
                continue
            elif label_text == "Number of Source Depths":
                continue
            elif label_text == "Source Depths":
                continue
            elif label_text == "Number of Receiver Depths":
                continue
            elif label_text == "Receiver Depths":
                continue
            elif label_text == "Number of Receiver Ranges":
                continue
            elif label_text == "Receiver Ranges": 
                continue
            elif label_text == "Ray Compute Type": 
                continue
            elif label_text == "Number of Beams": 
                continue
            elif label_text == "Launch Angles": 
                continue
            elif label_text == "Step Size (m)": 
                continue
            else:
                label = QLabel(label_text)
                layout.addWidget(label, j, 2 * line)
                layout.addWidget(line_edit, j, 2 * line + 1)

        # Run button
        run_button = QPushButton("Run")
        run_button.clicked.connect(self.run)
        layout.addWidget(run_button, len(self.fields), 0, 1, 2)

        self.setLayout(layout)

    def browse_bellhop_executable(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Bellhop Executable")
        if file_path:
            self.fields["Bellhop Executable"].setText(file_path)

    def run(self):
        try:
            # Read and convert input values
            values = {
                name: float(line_edit.text())
                for name, line_edit in self.fields.items()
            }

            lon_start = values["Start Longitude"]
            lat_start = values["Start Latitude"]
            lon_end   = values["End Longitude"]
            lat_end   = values["End Latitude"]
            freq      = values["Frequency (Hz)"]

            bath_map, lon_range, lat_range = map_2D()
            profile, distances = map_1D(bath_map, lon_range, lat_range, lon_start, lon_end, lat_start, lat_end, num_points=1000)

            track_dir = "/Users/justindiamond/Documents/Documents/UW-APL/Research/ARMS/Justin_Work/Data/"
            track_info = io.loadmat(os.path.join(track_dir, "track_info.mat"))
            ssp_data = io.loadmat(os.path.join(track_dir, "ARMS_firstDay_CTD_info.mat"))
            ssp_ = np.squeeze(np.array(ssp_data["Sound_velocity"]), axis=1) # Meters per second
            ssp_depths_ = np.squeeze(np.array(ssp_data["Depth"]), axis=1) # Meters per second
            ssp = np.append(ssp_, 1500.0)
            ssp_depths = np.append(ssp_depths_, 200.0)

            run_tl = Write_TL(
                dir="/Users/justindiamond/Documents/Documents/UW-APL/Research/ARMS/Justin_Work/App/runs/",
                filename="run_" + str(int(freq)),
                ssp_depths=ssp_depths,
                ssp=ssp,
                bath_ranges=distances,
                bath_depths=profile,
                freq=freq,
                nmedia=1,
                sspopt="CVW",
                bottom_type="A*",
                roughness=0.0,
                bottom_depth=max(profile),
                bottom_ss=1600.0,
                bottom_alpha=0.0,
                bottom_rho=1.8,
                bottom_shear=0.0,
                nsd=1,
                sd=[20.0],
                nrd=201,
                rd=[0.0, 200.0],
                nrr=501,
                rr=[0.0, max(profile)],
                ray_compute="C",
                num_beams=0,
                launch_angles=[-89.0, 89.0],
                step_size=0.0,
                max_depth=max(profile) + 5,
                max_range=max(distances) + 1
            )

            run_tl.write_files()

            os.system(
                "/Users/justindiamond/Documents/Documents/UW-APL/Research/ARMS/bellhopcuda/bin/bellhopcxx -2D /Users/justindiamond/Documents/Documents/UW-APL/Research/ARMS/App/runs/run_" + str(int(freq))
            )

            run_tl_plot = Read_TL(
                directory="/Users/justindiamond/Documents/Documents/UW-APL/Research/ARMS/Justin_Work/App/runs/",
                output_directory="/Users/justindiamond/Documents/Documents/UW-APL/Research/ARMS/Justin_Work/App/run_saves/",
                tl_file="run_",
                freqs=[freq],
                bath_ranges=distances
            )

            [_, _, _, _, _, pressure] = run_tl_plot.read_shd(freq)
            
            run_tl_plot.plot_tl(pressure)

        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter valid numeric values.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TLViewerApp()
    window.show()
    sys.exit(app.exec_())