import numpy as np
import matplotlib.pyplot as plt
import os
import sys
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_dir)
from pyat.pyat.readwrite import *

class Write_TL:
    def __init__(self, 
                 dir,                   # Save File Directory
                 filename,              # Save Filename with no extension
                 ssp_depths,            # Numpy array of Sound Speed Profile Depths (Meters)
                 ssp,                   # Numpy array of Sound Speed Profile (same length as ssp_depths), (Meters/second)
                 bath_ranges,           # Numpy array of bathymetry range values (Kilometers)
                 bath_depths,           # Numpy array of bathymetry depths (same length as bath_ranges), (Meters)
                 freq,
                 nmedia,
                 sspopt,
                 bottom_type,
                 roughness,
                 bottom_depth,
                 bottom_ss,
                 bottom_alpha,
                 bottom_rho,
                 bottom_shear,
                 nsd,
                 sd,
                 nrd,
                 rd,
                 nrr, 
                 rr,
                 ray_compute,
                 num_beams,
                 launch_angles,
                 step_size,
                 max_depth,
                 max_range,
                 pair='L'):             # Default for 2D Ray ('L' = List of pairs)
        
        self.dir = dir
        self.filename = filename
        self.ssp_depth = ssp_depths
        self.ssp = ssp
        self.bath_ranges = bath_ranges
        self.bath_depths = bath_depths
        self.freq = freq
        self.nmedia = nmedia
        self.sspopt = sspopt
        self.bottom_type = bottom_type
        self.roughness = roughness
        self.bottom_depth = bottom_depth
        self.bottom_ss = bottom_ss
        self.bottom_alpha = bottom_alpha
        self.bottom_rho = bottom_rho
        self.bottom_shear = bottom_shear
        self.nsd=nsd
        self.sd=sd
        self.nrd=nrd
        self.rd=rd
        self.nrr=nrr
        self.rr=rr
        self.ray_compute=ray_compute
        self.num_beams=num_beams
        self.launch_angles=launch_angles
        self.step_size=step_size
        self.max_depth=max_depth
        self.max_range=max_range
        self.pair = pair


    def write_env(self):
        env_path = os.path.join(self.dir, self.filename + ".env")
        if len(self.ssp_depth) != len(self.ssp):
            raise ValueError("Depths and speeds must have the same length.")

        max_depth = max(np.max(self.ssp_depth), np.max(self.bath_depths))
        min_depth = min(np.min(self.ssp_depth), np.min(self.bath_depths))
        max_range = np.max(self.bath_ranges)

        with open(env_path, 'w') as f:
            f.write(f"'{self.filename}'\t\t\t! TITLE\n")
            f.write(f"{self.freq}\t\t\t! FREQ (Hz)\n")
            f.write(f"{self.nmedia}\t\t\t! NMEDIA\n")
            f.write(f"'{self.sspopt}'\t\t\t! SSPOPT\n")
            f.write(f"{len(self.ssp_depth)}  {min(self.ssp_depth):.1f}  {max(self.ssp_depth):.1f}\t\t\t! DEPTH of bottom (m)\n")
            for d, s in zip(self.ssp_depth, self.ssp):
                f.write(f"{d:.1f}  {s:.2f}  /\n")
            f.write("\n")
            f.write(f"'{self.bottom_type}' {self.roughness}\t\t\t! BOTTOM TYPE ('A' = fluid), roughness\n")
            f.write(f"{self.bottom_depth:.1f}  {self.bottom_ss:.2f}  {self.bottom_shear:.1f}  {self.bottom_rho:.1f}  {self.bottom_alpha:.1f} /\t\t\t! Bottom depth, sound speed, shear speed, density\n")
            f.write("\n")
            f.write(f"{self.nsd}\t\t\t! NSD: Number of source depths\n")
            for i in range(len(self.sd)):
                if i is len(self.sd)-1:
                    f.write(f"{self.sd[i]:.1f} /\t\t\t! Source depth (m)\n")
                else:
                    f.write(f"{self.sd[i]:.1f} /")
            f.write("\n")
            f.write(f"{self.nrd}\t\t\t! NRD: Number of receiver depths\n")
            for i in range(len(self.rd)):
                if i is len(self.rd)-1:
                    f.write(f"{self.rd[i]:.1f} /\t\t\t! Receiver depths (m)\n")
                else:
                    f.write(f"{self.rd[i]:.1f} ")
            f.write("\n")
            f.write(f"{self.nrr}\t\t\t! NR: Number of ranges\n")
            for i in range(len(self.rr)):
                if i is len(self.rr)-1:
                    f.write(f"{self.rr[i]:.1f} /\t\t\t! Range values (km)\n")
                else:
                    f.write(f"{self.rr[i]:.1f} ")
            f.write("\n")
            f.write(f"'{self.ray_compute}'\t\t\t! Option: 'R' for ray tracing, 'C' = coherent TL, 'I' = incoherent TL, 'S' = arrivals\n")
            f.write(f"{self.num_beams} \t\t\t! Number of beams\n")
            f.write(f"{self.launch_angles[0]} {self.launch_angles[1]} /\t\t\t! Launch angles (degrees)\n")
            f.write("\n")
            f.write(f"{self.step_size:.1f} {self.max_depth:.1f} {self.max_range:.1f}\t\t\t! Step size (m), Max depth (m), Max range (km)\n")
        
        print(f".env file written: {env_path}")
        

    def write_ssp(self):
        ssp_path = os.path.join(self.dir, self.filename + ".ssp")
        if len(self.ssp_depth) != len(self.ssp):
            raise ValueError("Depths and speeds must have the same length.")
    
        with open(ssp_path, 'w') as f:
            f.write(f"'{self.pair}'\n")
            f.write(f"{len(self.ssp_depth)}\n")
            for d, s in zip(self.ssp_depth, self.ssp):
                f.write(f"{d:.2f}  {s:.2f}\n")
        print(f".ssp file written: {ssp_path}")

    def write_bty(self):
        bty_path = os.path.join(self.dir, self.filename + ".bty")
        if len(self.bath_ranges) != len(self.bath_depths):
            raise ValueError("ranges_km and depths_m must be the same length.")
    
        with open(bty_path, 'w') as f:
            f.write(f"'{self.pair}'\n")
            f.write(f"{len(self.bath_ranges)},\n")
            for r, d in zip(self.bath_ranges, self.bath_depths):
                f.write(f"{r:.2f}  {d:.1f} / \n")
        print(f".bty file written: {bty_path}")

    def write_files(self):
        self.write_ssp()
        self.write_bty()
        self.write_env()


class Read_TL:
    def __init__(self, 
                 directory, 
                 output_directory,
                 tl_file,
                 freq,
                 bath_ranges):
        
        self.dir = directory
        self.output_directory = output_directory
        self.tl_file = tl_file
        self.freq = freq
        self.bath_ranges = bath_ranges
    

    def read_shd(self):
        [x,x,x,x,ppos, pressure] = read_shd(self.dir + self.tl_file + ".shd", self.freq)

        return [x,x,x,x,ppos, pressure]

    
    def plot_tl(self, pressure):
        # Plot the pressure field
        print(pressure.shape)
        plt.figure(figsize=(12,8))
        pressure = abs(pressure)
        pressure = 10*np.log10(pressure/np.max(pressure))
        levs = np.linspace(-30, 0, 31)
        plt.contourf(np.squeeze(pressure), levels=levs)
        plt.colorbar()
        plt.gca().invert_yaxis()
        plt.title(f"{self.tl_file}, Frequency: {self.freq/1000:.2}")
        plt.xlabel("Range (km)")
        plt.ylabel("Depth (m)")
        n_range_pts = pressure.shape[3]
        interpolated_ranges = np.linspace(self.bath_ranges[0], self.bath_ranges[-1], n_range_pts)

        # Set custom x-ticks (e.g., 6 evenly spaced points)
        tick_locs = np.linspace(0, n_range_pts - 1, 6, dtype=int)
        tick_labels = [f"{interpolated_ranges[i]:.1f}" for i in tick_locs]

        plt.xticks(ticks=tick_locs, labels=tick_labels)
        plt.savefig(self.output_directory + self.tl_file + "_10500.png", dpi=300)
        plt.show()