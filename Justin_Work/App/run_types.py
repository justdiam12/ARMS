import os
import glob
import numpy as np
from PyQt5.QtWidgets import QMessageBox, QLineEdit, QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Personal files
from Justin_Work.ray import Write_RAY, Read_RAY
from Justin_Work.tl import Write_TL, Read_TL
from Justin_Work.bathymetry import *


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
    environmental_file = self.fields["Environmental Files Directory"].text()
    lon_start = np.float64(values["Source Longitude"])
    lat_start = np.float64(values["Source Latitude"])
    lon_end   = np.float64(values["Receiver Longitude"])
    lat_end   = np.float64(values["Receiver Latitude"])
    try:
        bty_data = io.loadmat(os.path.join(environmental_file, "bty.mat"))
    except:
        QMessageBox.critical(self, "Error", "Could not load bty.mat from the specified Environmental Files Directory. Please check your input.")
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


def plot_ssp(self):
    return


def run_bellhop(self):
    try:
        # Read and convert input valuess
        values = {}
        for name, widget in self.fields.items():
            if isinstance(widget, QLineEdit):
                values[name] = widget.text()
            elif isinstance(widget, QComboBox):
                values[name] = widget.currentText()
            else:
                values[name] = None

        bellhop_executable = self.fields["Bellhop Executable"].text()
        environmental_dir = self.fields["Environmental Files Directory"].text()
        env_files = os.listdir(environmental_dir)
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

        # Fix ray_compute
        ray_compute_type = np.append(ray_compute_type, ['', '', '', ''])        

        # Create new data directory
        data_dir = os.path.join(data_dir, f"{ray_compute_type[0]}_{freq}_{lon_start}_{lon_end}_{lat_start}_{lat_end}")
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        else:
            QMessageBox.warning(self, "Warning", f"Directory {data_dir} already exists. Files may be overwritten.")   
    
        # Check directory input
        if "bty.mat" in env_files and "ssp.mat" in env_files and "ati.mat" in env_files:
            bathy_file = os.path.join(environmental_dir, "bty.mat")
            ssp_file = os.path.join(environmental_dir, "ssp.mat")
            ati_file = os.path.join(environmental_dir, "ati.mat")

            # Adjust save directory for current run
            curr_dir_name = data_dir.split(os.sep)[-1]
            data_dir_curr = os.path.join(data_dir, curr_dir_name)
            if not os.path.exists(data_dir_curr):
                os.makedirs(data_dir_curr)
            else:
                QMessageBox.warning(self, "Warning", f"Directory {data_dir_curr} already exists. Files may be overwritten.")   
        
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
                                                num_points=500)
            else:
                QMessageBox.critical(self, "Error", "Source and receiver coordinates are outside the bathymetry range. Please check your inputs.")
                return

            # ATI
            ati_data = io.loadmat(ati_file)
            ati_depths = np.squeeze(np.array(ati_data["ati"], dtype=np.float64), axis=0)

            # SSP
            ssp_data = io.loadmat(ssp_file)
            ssp = np.array(ssp_data["ssp"], dtype=np.float64)
            ssp_depths = np.array(ssp_data["ssp_depths"], dtype=np.float64)
            ssp_ranges = np.array(ssp_data["ssp_ranges"], dtype=np.float64)
            if ssp_ranges.shape[1] > 1:
                sspopt1_curr = 'Q'
            else:
                sspopt1_curr = sspopt1

            # Bellhop terminal command
            if os.name == 'posix':
                run_bh = f"{bellhop_executable} -2D {os.path.join(data_dir_curr, filename)}"
            elif os.name == 'nt':
                run_bh = f"{bellhop_executable}.exe -2D {os.path.join(data_dir_curr, filename)}"
            else:
                raise EnvironmentError("Unsupported operating system for Bellhop execution.")


            if ray_compute_type[0] == 'E':
                ray_shot = Write_RAY(dir=data_dir_curr, 
                                    filename=filename, 
                                    ssp_depths=ssp_depths,
                                    ssp=ssp,
                                    ssp_ranges=ssp_ranges,
                                    bath_ranges=bath_ranges,
                                    bath_depths=bath_depths,
                                    ati_depths=ati_depths,
                                    freq=freq,
                                    nmedia=1,
                                    sspopt=[sspopt1_curr, 
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
                
                # Write the .env, ,ssp, .bty, .ati, .mat files
                ray_shot.write_files()
                
                # Run Bellhop
                os.system(run_bh)

                # Plot the results
                ray_shot_plot = Read_RAY(directory=data_dir_curr, 
                                        ray_file=filename, 
                                        ray_compute_type=ray_compute_type[0],
                                        ssp_depths=ssp_depths, 
                                        ssp=ssp,
                                        ssp_ranges=ssp_ranges,
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
                    
                ray_shot_plot.write_mat()
                ray_shot_plot.plot_ray_profile()
            
            elif ray_compute_type[0] == 'R':
                ray_shot = Write_RAY(dir=data_dir_curr, 
                                    filename=filename, 
                                    ssp_depths=ssp_depths,
                                    ssp=ssp,
                                    ssp_ranges=ssp_ranges,
                                    bath_ranges=bath_ranges,
                                    bath_depths=bath_depths,
                                    ati_depths=ati_depths,
                                    freq=freq,
                                    nmedia=1,
                                    sspopt=[sspopt1_curr, 
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
                
                # Write the .env, ,ssp, .bty, .ati, .mat files
                ray_shot.write_files()
                
                # Run Bellhop
                os.system(run_bh)

                # Plot the results
                ray_shot_plot = Read_RAY(directory=data_dir_curr, 
                                        ray_file=filename, 
                                        ray_compute_type=ray_compute_type[0],
                                        ssp_depths=ssp_depths, 
                                        ssp=ssp,
                                        ssp_ranges=ssp_ranges,
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
                    
                ray_shot_plot.write_mat()
                ray_shot_plot.plot_ray_profile()

            elif ray_compute_type[0] == 'C' or ray_compute_type[0] == 'I' or ray_compute_type[0] == 'S':
                tl_shot = Write_TL(dir=data_dir_curr, 
                                filename=filename, 
                                ssp_depths=ssp_depths,
                                ssp=ssp,
                                ssp_ranges=ssp_ranges,
                                bath_ranges=bath_ranges,
                                bath_depths=bath_depths,
                                ati_depths=ati_depths,
                                freq=freq,
                                nmedia=1,
                                sspopt=[sspopt1_curr, 
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
                
                # Write the .env, ,ssp, .bty, .ati, .mat files
                tl_shot.write_files()
                
                # Run Bellhop
                os.system(run_bh)

                # Plot the results
                tl_shot_plot = Read_TL(directory=data_dir_curr, 
                                    tl_file=filename, 
                                    freqs=[int(float(freq))],
                                    bath_depths=bath_depths,
                                    bath_ranges=bath_ranges,
                                    ati_depths=ati_depths,
                                    ati_ranges=bath_ranges)
                    
                tl_shot_plot.read_shd_main()
                tl_shot_plot.write_mat()
                tl_shot_plot.plot_tl()

        else:
            env_folders = [f for f in os.listdir(environmental_dir) if os.path.isdir(os.path.join(environmental_dir, f))]
            for i in range(len(env_folders)):

                env_curr = env_folders[i]
                environmental_file_curr = os.path.join(environmental_dir, env_curr)
                bathy_file = os.path.join(environmental_file_curr, "bty.mat")
                ssp_file = os.path.join(environmental_file_curr, "ssp.mat")
                ati_file = os.path.join(environmental_file_curr, "ati.mat")

                # Adjust save directory for current run
                data_dir_curr = os.path.join(data_dir, env_curr)
                if not os.path.exists(data_dir_curr):
                    os.makedirs(data_dir_curr)
                else:
                    QMessageBox.warning(self, "Warning", f"Directory {data_dir_curr} already exists. Files may be overwritten.")   
            
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
                                                    num_points=500)
                else:
                    QMessageBox.critical(self, "Error", "Source and receiver coordinates are outside the bathymetry range. Please check your inputs.")
                    return

                # ATI
                ati_data = io.loadmat(ati_file)
                ati_depths = np.squeeze(np.array(ati_data["ati"], dtype=np.float64), axis=0)

                # SSP
                ssp_data = io.loadmat(ssp_file)
                ssp = np.array(ssp_data["ssp"], dtype=np.float64)
                ssp_depths = np.array(ssp_data["ssp_depths"], dtype=np.float64)
                ssp_ranges = np.array(ssp_data["ssp_ranges"], dtype=np.float64)
                if ssp_ranges.shape[1] > 1:
                    sspopt1_curr = 'Q'
                else:
                    sspopt1_curr = sspopt1

                # Bellhop terminal command
                if os.name == 'posix':
                    run_bh = f"{bellhop_executable} -2D {os.path.join(data_dir_curr, filename)}"
                elif os.name == 'nt':
                    run_bh = f"{bellhop_executable}.exe -2D {os.path.join(data_dir_curr, filename)}"
                else:
                    raise EnvironmentError("Unsupported operating system for Bellhop execution.")


                if ray_compute_type[0] == 'E':
                    ray_shot = Write_RAY(dir=data_dir_curr, 
                                        filename=filename, 
                                        ssp_depths=ssp_depths,
                                        ssp=ssp,
                                        ssp_ranges=ssp_ranges,
                                        bath_ranges=bath_ranges,
                                        bath_depths=bath_depths,
                                        ati_depths=ati_depths,
                                        freq=freq,
                                        nmedia=1,
                                        sspopt=[sspopt1_curr, 
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
                    
                    # Write the .env, ,ssp, .bty, .ati, .mat files
                    ray_shot.write_files()
                    
                    # Run Bellhop
                    os.system(run_bh)

                    # Plot the results
                    ray_shot_plot = Read_RAY(directory=data_dir_curr, 
                                            ray_file=filename, 
                                            ray_compute_type=ray_compute_type[0],
                                            ssp_depths=ssp_depths, 
                                            ssp=ssp,
                                            ssp_ranges=ssp_ranges,
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
                        
                    ray_shot_plot.write_mat()
                    ray_shot_plot.plot_ray_profile()
                
                elif ray_compute_type[0] == 'R':
                    ray_shot = Write_RAY(dir=data_dir_curr, 
                                        filename=filename, 
                                        ssp_depths=ssp_depths,
                                        ssp=ssp,
                                        ssp_ranges=ssp_ranges,
                                        bath_ranges=bath_ranges,
                                        bath_depths=bath_depths,
                                        ati_depths=ati_depths,
                                        freq=freq,
                                        nmedia=1,
                                        sspopt=[sspopt1_curr, 
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
                    
                    # Write the .env, ,ssp, .bty, .ati, .mat files
                    ray_shot.write_files()
                    
                    # Run Bellhop
                    os.system(run_bh)

                    # Plot the results
                    ray_shot_plot = Read_RAY(directory=data_dir_curr, 
                                            ray_file=filename, 
                                            ray_compute_type=ray_compute_type[0],
                                            ssp_depths=ssp_depths, 
                                            ssp=ssp,
                                            ssp_ranges=ssp_ranges,
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
                        
                    ray_shot_plot.write_mat()
                    ray_shot_plot.plot_ray_profile()

                elif ray_compute_type[0] == 'C' or ray_compute_type[0] == 'I' or ray_compute_type[0] == 'S':
                    tl_shot = Write_TL(dir=data_dir_curr, 
                                    filename=filename, 
                                    ssp_depths=ssp_depths,
                                    ssp=ssp,
                                    ssp_ranges=ssp_ranges,
                                    bath_ranges=bath_ranges,
                                    bath_depths=bath_depths,
                                    ati_depths=ati_depths,
                                    freq=freq,
                                    nmedia=1,
                                    sspopt=[sspopt1_curr, 
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
                    
                    # Write the .env, ,ssp, .bty, .ati, .mat files
                    tl_shot.write_files()
                    
                    # Run Bellhop
                    os.system(run_bh)

                    # Plot the results
                    tl_shot_plot = Read_TL(directory=data_dir_curr, 
                                        tl_file=filename, 
                                        freqs=[int(float(freq))],
                                        bath_depths=bath_depths,
                                        bath_ranges=bath_ranges,
                                        ati_depths=ati_depths,
                                        ati_ranges=bath_ranges)
                        
                    tl_shot_plot.read_shd_main()
                    tl_shot_plot.write_mat()
                    tl_shot_plot.plot_tl()

            
    except Exception as e:
        QMessageBox.critical(self, "Error", f"{e}")

    
def compare_tl(self):
    return