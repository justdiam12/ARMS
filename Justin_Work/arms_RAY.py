import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as io

# Add the root directory to sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # one level up
sys.path.append(root_dir)
from Justin_Work.ray import Write_RAY, Read_RAY

# Main Data Directory and Save File Name
track_dir = "/Users/justindiamond/Documents/Documents/UW-APL/Research/ARMS/Justin_Work/Data/"
directory = "/Users/justindiamond/Documents/Documents/UW-APL/Research/ARMS/Justin_Work/Data/arms_ray/"
output_directory = "/Users/justindiamond/Documents/Documents/UW-APL/Research/ARMS/Justin_Work/Output/"
arms_save_file = "arms_1_ray"

# Trackline Information
track_info = io.loadmat(os.path.join(track_dir, "track_info.mat"))

# Bathymetry (.bty file info)
bath_ranges = np.squeeze(np.array(track_info["distances"]), axis=0) # Meters
bath_depths = np.squeeze(np.array(track_info["profile"]), axis=0)
ati_depths = np.ones_like(bath_ranges) * 10 * np.sin(2*np.pi*bath_ranges)

# Sound Speed Profile (.ssp file info)
ssp_data = io.loadmat(os.path.join(track_dir, "ARMS_firstDay_CTD_info.mat"))
ssp_ = np.squeeze(np.array(ssp_data["Sound_velocity"]), axis=1) # Meters per second
ssp_depths_ = np.squeeze(np.array(ssp_data["Depth"]), axis=1) # Meters per second

# Fix SSP and Depths for Max Bathymetry Depth
ssp_extra = np.linspace(max(ssp_)+1, max(ssp_)+2, 100)
ssp_depths_extra = np.linspace(max(ssp_depths_)+1, max(bath_depths)+5, 100)
ssp = np.append(ssp_, ssp_extra)
ssp_depths = np.append(ssp_depths_, ssp_depths_extra)
ssp = np.append(1470, ssp)
ssp_depths = np.append(-10, ssp_depths)

# Environmental Information (.env file info)
freq = 100.0   # Hz
nmedia = 1   # Number of media layers (water column SSP)
sspopt = ["S",  # S: Cubic Spline Interpolation, C: C-linear interpolation, N: N2-line Interpolation, A: Analytic Interpolation, Q: Quadratic Approximation
          "A",  # V: Vacuum above surface (SURFACE-LINE not required), R: Perfectly rigid media above surface, A: Acoustic half-space, F: Read a list of reflection coefficients from *.irc file
          "F",  # F: attenuation corresponds to (dB/m)kHz, L: attenuation corresponds to parameter loss, M: attenuation corresponds to dB/m, N: attenuation corresponds to Nepers/m, Q: attenuation corresponds to a Q-factor, W: attenuation corresponds to dB/wavelength
          " ",  # T: Opptional parameter for Thorpe volume attenuation
          "*"]  # *: Use if including an *.ati file for surface shape
surface_opt = [min(ati_depths),  # Surface depth (m)
               350.0,            # Compressional Speed (m/s)
               0.0,              # Shear Speed (m/s)
               1.8,              # Density (g/cm^3)
               0.0]              # Surface Attenuation (units specified by sspopt(3))
bottom_type = ["A",  # V: Vacuum below water column, R: rigid below water column, A: acoustic half-space below water column (need BOTTOM-LINE), F: read list of reflection coefficients from *.brc file
               "*"]  # *: include if wanting to use a *.bty file
roughness = 0.0   # Roughness
bottom_opt = [max(bath_depths),  # Bottom depth (m)
              1600.0,            # Compressional Speed (m/s)
              0.0,               # Shear Speed (m/s)
              1.8,               # Density (g/cm^3)
              0.0]               # Bottom Attenuation (units specified by sspopt(3))
nsd = 1   # NSD (Number of source depths)
sd = [60.0]   # Source depth(s) (Meters)
nrd = 1   # NRD (number of receiver depths)
rd = [60.0]   # Receiver depths (Meters)
nrr = 1   # NR (number of receiver ranges)
rr = [max(bath_ranges)]   # Receiver ranges (km)
ray_compute = ["E",  # A: Write amplitude and travel times, E: Write Eigenray coordinates, R: Write ray coordinates, C: Write coherent acoustic pressure, I: Write incoherent acoustic pressure, S: Write semi-coherent acoustic pressure
               "",  # G: Use geometric beams (default), C: Use cartesian beams, R: Use ray-centered beams, B: Use Gaussian beam bundles
               "",  # ' ': Do not use beam shift effects (defualt), S: Include beam shift effects, *: Use source beam pattern file
               "",  # R: Point source in cylindrical coordinates (default), X: line source in Cartesian coordinates
               ""]  # R: Rectiliniear receiver grid, I: Irregular grid
num_beams = 10001   # Number of beams
launch_angles = [-25.0, 25.0]   # Beam launch angles
step_size = 10.0   # Step size (meters)
max_depth = bottom_opt[0]+5   # Max depth (Meters)
max_range = max(bath_ranges)+1  # Max range (Kilometers)

# Only needed if opt3 is composed of more than one character
opt4 = ["",  # C: Cerveny Type, F: Space-filling, M: Minimum width, W: WKB beams
        ""]  # D: Use curvature doubling, S: Use standard curvature, Z: Use zeroing curvature
pair = 'L'  # L: linear interpolation, C: Curvilinear interpolation
precision = 1

shot_1_ray = Write_RAY(dir=directory, 
                       filename=arms_save_file, 
                       ssp_depths=ssp_depths,
                       ssp=ssp,
                       bath_ranges=bath_ranges,
                       bath_depths=bath_depths,
                       ati_depths=ati_depths,
                       freq=freq,
                       nmedia=nmedia,
                       sspopt=sspopt,
                       surface_opt=surface_opt,
                       bottom_type=bottom_type,
                       roughness=roughness,
                       bottom_opt=bottom_opt,
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

shot_1_ray.write_files()

# Run BELLHOP
os.system("/Users/justindiamond/Documents/Documents/UW-APL/Research/ARMS/bellhopcuda/bin/bellhopcxx -2D /Users/justindiamond/Documents/Documents/UW-APL/Research/ARMS/Justin_Work/Data/arms_ray/arms_1_ray")

shot_1_ray_plot = Read_RAY(directory=directory, 
                           output_directory = output_directory,
                           ray_file=arms_save_file, 
                           ssp_depths=ssp_depths, 
                           ssp=ssp,
                           bath_ranges=bath_ranges, 
                           bath_depths=bath_depths, 
                           ati_depths=ati_depths, 
                           s_depth=sd[0], 
                           r_depth=rd[0], 
                           r_range=rr[0],
                           precision=precision,
                           bottom_opt=bottom_opt,
                           surface_opt=surface_opt)

shot_1_ray_plot.plot_ray_profile()
plt.show()