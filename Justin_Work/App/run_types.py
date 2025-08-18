import os
import numpy as np
from PyQt5.QtWidgets import QMessageBox, QLineEdit, QComboBox
from Justin_Work.ray import Write_RAY, Read_RAY
from Justin_Work.tl import Write_TL, Read_TL
from pyat.pyat.readwrite import *
from Justin_Work.bathymetry import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


def plot_bathy(self):
    values = {}
    for name, widget in self.fields.items():
        if isinstance(widget, QLineEdit):
            values[name] = widget.text()
        elif isinstance(widget, QComboBox):
            values[name] = widget.currentText()
        else:
            values[name] = None
    
    # Extract Bathymetry File and coordinates
    bathy_file = self.fields["Bathymetry File"].text()
    lon_start = np.float64(values["Source Longitude"])
    lat_start = np.float64(values["Source Latitude"])
    lon_end   = np.float64(values["Receiver Longitude"])
    lat_end   = np.float64(values["Receiver Latitude"])
    bty_data = io.loadmat(bathy_file)
    bath_map = np.array(bty_data["bath_map"], dtype=np.float64)
    lon_range = np.squeeze(np.array(bty_data["lon_range"], dtype=np.float64), axis=0)
    lat_range = np.squeeze(np.array(bty_data["lat_range"], dtype=np.float64), axis=0)

    if  lon_start >= min(lon_range) and lon_start <= max(lon_range) and lat_start >= min(lat_range) and lat_start <= max(lat_range) and lon_end >= min(lon_range) and lon_end <= max(lon_range) and lat_end >= min(lat_range) and lat_end <= max(lat_range):
        bath_depths, bath_ranges = map_1D(bath_map=bath_map, 
                                          lon_range=lon_range, 
                                          lat_range=lat_range, 
                                          lon_start=lon_start, 
                                          lon_end=lon_end, 
                                          lat_start=lat_start, 
                                          lat_end=lat_end,
                                          num_points=500)
        try:
            plot_all(bath_map=bath_map, 
                     lon_range=lon_range,
                     lat_range=lat_range, 
                     profile=bath_depths, 
                     distances=bath_ranges, 
                     lon_start=lon_start, 
                     lon_end=lon_end, 
                     lat_start=lat_start, 
                     lat_end=lat_end, 
                     save_dir = os.path.join(os.getcwd(), "Justin_Work", "App", "Runs", "Bathymetry", f"{lon_start}_{lon_end}_{lat_start}_{lat_end}_bathy"))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to plot bathymetry: {e}")


def run_bellhop(self):
    try:
        # Read and convert input values
        values = {}
        for name, widget in self.fields.items():
            if isinstance(widget, QLineEdit):
                values[name] = widget.text()
            elif isinstance(widget, QComboBox):
                values[name] = widget.currentText()
            else:
                values[name] = None

        bellhop_executable = self.fields["Bellhop Executable"].text()
        ssp_file = self.fields["SSP File"].text()
        bathy_file = self.fields["Bathymetry File"].text()
        ati_file = self.fields["Altimetry File"].text()
        filename = self.fields["Filename"].text()
        data_dir = self.fields["Data File Directory"].text() 
        lon_start = np.float64(values["Source Longitude"])
        lat_start = np.float64(values["Source Latitude"])
        lon_end   = np.float64(values["Receiver Longitude"])
        lat_end   = np.float64(values["Receiver Latitude"])
        freq      = values["Frequency"]
        sspopt1 = self.fields["SSPOPT(1)"].currentText().split(":")[0].strip()
        sspopt2 = self.fields["SSPOPT(2)"].currentText().split(":")[0].strip()
        sspopt3 = self.fields["SSPOPT(3)"].currentText().split(":")[0].strip()
        sspopt4 = self.fields["SSPOPT(4)"].currentText().split(":")[0].strip()
        sspopt5 = self.fields["SSPOPT(5)"].currentText().split(":")[0].strip()
        surface_height = values["Surface Height"]
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
        ray_compute_type = np.array(self.fields["Ray Compute Type"].currentText().split(":")[0].strip())
        num_beams = int(values["Number of Beams"])
        launch_angles = np.array([float(x) for x in self.fields["Launch Angles"].text().split(",")])
        step_size = int(float(values["Step Size"]))

        # SSP
        ssp_data = io.loadmat(ssp_file)
        ssp = np.squeeze(np.array(ssp_data["ssp"], dtype=np.float64), axis=0)
        ssp_depths = np.squeeze(np.array(ssp_data["ssp_depths"], dtype=np.float64), axis=0)
    
        # BTY
        bty_data = io.loadmat(bathy_file)
        bath_map = np.array(bty_data["bath_map"], dtype=np.float64)
        lon_range = np.squeeze(np.array(bty_data["lon_range"], dtype=np.float64), axis=0)
        lat_range = np.squeeze(np.array(bty_data["lat_range"], dtype=np.float64), axis=0)

        if  lon_start >= min(lon_range) and lon_start <= max(lon_range) and lat_start >= min(lat_range) and lat_start <= max(lat_range) and lon_end >= min(lon_range) and lon_end <= max(lon_range) and lat_end >= min(lat_range) and lat_end <= max(lat_range):
            bath_depths, bath_ranges = map_1D(bath_map=bath_map, 
                                            lon_range=lon_range, 
                                            lat_range=lat_range, 
                                            lon_start=lon_start, 
                                            lon_end=lon_end, 
                                            lat_start=lat_start, 
                                            lat_end=lat_end,
                                            num_points=200)
        else:
            QMessageBox.critical(self, "Error", "Source and receiver coordinates are outside the bathymetry range. Please check your inputs.")
            return

        # ATI
        ati_data = io.loadmat(ati_file)
        ati_depths = np.squeeze(np.array(ati_data["ati"], dtype=np.float64), axis=0)

        # Fix ray_compute
        ray_compute_type = np.append(ray_compute_type, ['', '', '', ''])

        # Create new data directory
        data_dir = os.path.join(data_dir, f"{ray_compute_type[0]}_{freq}_{lon_start}_{lon_end}_{lat_start}_{lat_end}")
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        else:
            QMessageBox.warning(self, "Warning", f"Directory {data_dir} already exists. Files may be overwritten.")

        if ray_compute_type[0] == 'E':
            ray_shot = Write_RAY(dir=data_dir, 
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
                                surface_opt=[min(ati_depths),
                                            float(surface_compressional_speed),
                                            float(surface_shear_speed),
                                            float(surface_density),
                                            float(surface_attenuation)],
                                bottom_type=[bottom_type,
                                            include_bathymetry],
                                roughness=roughness,
                                bottom_opt=[max(bath_depths),
                                            float(bottom_compressional_speed),
                                            float(bottom_shear_speed),
                                            float(bottom_density),
                                            float(bottom_attenuation)],
                                nsd=num_source_depths,
                                sd=source_depths,
                                nrd=num_receiver_depths,
                                rd=receiver_depths,
                                nrr=num_receiver_ranges, 
                                rr=receiver_ranges,
                                ray_compute=ray_compute_type,
                                num_beams=num_beams,
                                launch_angles=launch_angles,
                                step_size=step_size,
                                max_depth=max(bath_depths)+1,
                                max_range=max(bath_ranges)+1,
                                opt4=None,
                                pair='L')
            
            # Write the .env, .bty, and .ati files
            ray_shot.write_files()
            
            # Run Bellhop
            os.system(bellhop_executable + " -2D " + os.path.join(data_dir, filename))

            # Plot the results
            ray_shot_plot = Read_RAY(directory=data_dir, 
                                    ray_file=filename, 
                                    ray_compute_type=ray_compute_type[0],
                                    ssp_depths=ssp_depths, 
                                    ssp=ssp,
                                    bath_ranges=bath_ranges, 
                                    bath_depths=bath_depths, 
                                    ati_depths=ati_depths, 
                                    s_depth=source_depths, 
                                    r_depth=receiver_depths, 
                                    r_range=receiver_ranges,
                                    precision=1,
                                    bottom_opt=[max(bath_depths),
                                                float(bottom_compressional_speed),
                                                float(bottom_shear_speed),
                                                float(bottom_density),
                                                float(bottom_attenuation)],
                                    surface_opt=[min(ati_depths),
                                                float(surface_compressional_speed),
                                                float(surface_shear_speed),
                                                float(surface_density),
                                                float(surface_attenuation)])
                
            ray_shot_plot.plot_ray_profile()
            plt.show()
        
        elif ray_compute_type[0] == 'R':
            ray_shot = Write_RAY(dir=data_dir, 
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
                                surface_opt=[min(ati_depths),
                                            float(surface_compressional_speed),
                                            float(surface_shear_speed),
                                            float(surface_density),
                                            float(surface_attenuation)],
                                bottom_type=[bottom_type,
                                            include_bathymetry],
                                roughness=roughness,
                                bottom_opt=[max(bath_depths),
                                            float(bottom_compressional_speed),
                                            float(bottom_shear_speed),
                                            float(bottom_density),
                                            float(bottom_attenuation)],
                                nsd=num_source_depths,
                                sd=source_depths,
                                nrd=num_receiver_depths,
                                rd=receiver_depths,
                                nrr=num_receiver_ranges, 
                                rr=receiver_ranges,
                                ray_compute=ray_compute_type,
                                num_beams=num_beams,
                                launch_angles=launch_angles,
                                step_size=step_size,
                                max_depth=max(bath_depths)+1,
                                max_range=max(bath_ranges),
                                opt4=None,
                                pair='L')
            
            # Write the .env, .bty, and .ati files
            ray_shot.write_files()
            
            # Run Bellhop
            os.system(bellhop_executable + " -2D " + os.path.join(data_dir, filename))

            # Plot the results
            ray_shot_plot = Read_RAY(directory=data_dir, 
                                    ray_file=filename, 
                                    ray_compute_type=ray_compute_type[0],
                                    ssp_depths=ssp_depths, 
                                    ssp=ssp,
                                    bath_ranges=bath_ranges, 
                                    bath_depths=bath_depths, 
                                    ati_depths=ati_depths, 
                                    s_depth=source_depths, 
                                    r_depth=receiver_depths, 
                                    r_range=receiver_ranges,
                                    precision=1,
                                    bottom_opt=[max(bath_depths),
                                                float(bottom_compressional_speed),
                                                float(bottom_shear_speed),
                                                float(bottom_density),
                                                float(bottom_attenuation)],
                                    surface_opt=[min(ati_depths),
                                                float(surface_compressional_speed),
                                                float(surface_shear_speed),
                                                float(surface_density),
                                                float(surface_attenuation)])
                
            ray_shot_plot.plot_ray_profile()
            plt.show()

        elif ray_compute_type[0] == 'C':
            tl_shot = Write_TL(dir=data_dir, 
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
                               surface_opt=[min(ati_depths),
                                            float(surface_compressional_speed),
                                            float(surface_shear_speed),
                                            float(surface_density),
                                            float(surface_attenuation)],
                               bottom_type=[bottom_type,
                                            include_bathymetry],
                               roughness=roughness,
                               bottom_opt=[max(bath_depths),
                                           float(bottom_compressional_speed),
                                           float(bottom_shear_speed),
                                           float(bottom_density),
                                           float(bottom_attenuation)],
                               nsd=num_source_depths,
                               sd=source_depths,
                               nrd=num_receiver_depths,
                               rd=receiver_depths,
                               nrr=num_receiver_ranges, 
                               rr=receiver_ranges,
                               ray_compute=ray_compute_type,
                               num_beams=num_beams,
                               launch_angles=launch_angles,
                               step_size=step_size,
                               max_depth=max(bath_depths)+1,
                               max_range=max(bath_ranges)+1,
                               opt4=None,
                               pair='L')
            
            # Write the .env, .bty, and .ati files
            tl_shot.write_files()
            
            # Run Bellhop
            os.system(bellhop_executable + " -2D " + os.path.join(data_dir, filename))

            # Plot the results
            tl_shot_plot = Read_TL(directory=data_dir, 
                                   tl_file=filename, 
                                   freqs=[int(float(freq))],
                                   bath_ranges=bath_ranges)
                
            pressure = tl_shot_plot.read_shd(freq=int(float(freq)))
            tl_shot_plot.plot_tl(pressure)
            
    except Exception as e:
        QMessageBox.critical(self, "Error", f"{e}")