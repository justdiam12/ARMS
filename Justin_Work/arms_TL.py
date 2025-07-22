import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as io
import struct

# Add the root directory to sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # one level up
sys.path.append(root_dir)
from Justin_Work.tl import Write_TL, Read_TL
from pyat.pyat.readwrite import *

# Main Data Directory and Save File Name
track_dir = "/Users/justindiamond/Documents/Documents/UW-APL/Research/ARMS/Justin_Work/Data/"
directory = "/Users/justindiamond/Documents/Documents/UW-APL/Research/ARMS/Justin_Work/Data/arms_tl/"
output_directory = "/Users/justindiamond/Documents/Documents/UW-APL/Research/ARMS/Justin_Work/Output/"
arms_save_file = "arms_1_tl"

# Trackline Information
track_info = io.loadmat(os.path.join(track_dir, "track_info.mat"))

# Bathymetry (.bty file info)
bath_ranges = np.squeeze(np.array(track_info["distances"]), axis=0) # Meters
bath_depths = np.squeeze(np.array(track_info["profile"]), axis=0)

# Sound Speed Profile (.ssp file info)
ssp_data = io.loadmat(os.path.join(track_dir, "ARMS_firstDay_CTD_info.mat"))
ssp_ = np.squeeze(np.array(ssp_data["Sound_velocity"]), axis=1) # Meters per second
ssp_depths_ = np.squeeze(np.array(ssp_data["Depth"]), axis=1) # Meters per second

# Fix SSP and Depths for Max Bathymetry Depth
ssp = np.append(ssp_, 1500.0)
ssp_depths = np.append(ssp_depths_, 200.0)

# Environmental Information (.env file info)
freq = 10500.0   # Hz
nmedia = 1   # Number of media layers (water column SSP)
sspopt = "CVW"   # C = linear, V = Variable
bottom_type = "A*"   # A = fluid, A~ = fluid with no .bot file
roughness = 0.0   # Roughness
bottom_depth = max(bath_depths)   # Bottom Depth (m)
bottom_ss = 1600.0   # Meters per Second
bottom_alpha = 0.0   # dB per wavelength
bottom_rho = 1.8   # Grams per Centimeter^3
bottom_shear = 0.0   # Meters per Second
nsd = 1   # NSD (Number of source depths)
sd = [20.0]   # Source depth(s) (Meters)
nrd = 201   # NRD (number of receiver depths)
rd = [0.0, 200.0]   # Receiver depths (Meters)
nrr = 501   # NR (number of receiver ranges)
rr = [0.0, max(bath_ranges)]   # Receiver ranges (km)
ray_compute = "C"   # Compute rays (E = eigenrays)
num_beams = 0   # Number of beams
launch_angles = [-89.0, 89.0]   # Beam launch angles
step_size = 0.0   # Step size (meters)
max_depth = bottom_depth+5   # Max depth (Meters)
max_range = max(bath_ranges)+1  # Max range (Kilometers)
precision = 1
surface_Z = 446.0
surface_c = 343.0
bottom_Z = bottom_ss * bottom_rho * 1000
water_top_Z = ssp[0] * 1029
water_bottom_Z = ssp[-1] * 1029

arms_1_tl = Write_TL(dir=directory, 
                      filename=arms_save_file, 
                      ssp_depths=ssp_depths,
                      ssp=ssp,
                      bath_ranges=bath_ranges,
                      bath_depths=bath_depths,
                      freq=freq,
                      nmedia=nmedia,
                      sspopt=sspopt,
                      bottom_type=bottom_type,
                      roughness=roughness,
                      bottom_depth = bottom_depth,
                      bottom_ss=bottom_ss,
                      bottom_alpha=bottom_alpha,
                      bottom_rho=bottom_rho,
                      bottom_shear=bottom_shear,
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
                      max_range=max_range)

arms_1_tl.write_files()

# Run BELLHOP
os.system("/Users/justindiamond/Documents/Documents/UW-APL/Research/ARMS/bellhopcuda/bin/bellhopcxx -2D /Users/justindiamond/Documents/Documents/UW-APL/Research/ARMS/Justin_Work/Data/arms_tl/arms_1_tl")

arms_1_tl_plot = Read_TL(directory=directory, 
                         output_directory = output_directory,
                         tl_file=arms_save_file,
                         freqs=[freq], 
                         bath_ranges=bath_ranges)

[_, _, _, _, _, pressure] = arms_1_tl_plot.read_shd()
arms_1_tl_plot.plot_tl(pressure)