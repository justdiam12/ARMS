import numpy as np
import matplotlib.pyplot as plt
import os
import sys
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_dir)
from pyat.pyat.readwrite import *
import matplotlib.animation as animation

class Write_TL:
    def __init__(self, 
                 dir=None,                   # Save File Directory
                 filename=None,              # Save Filename with no extension
                 ssp_depths=None,            # Numpy array of Sound Speed Profile Depths (Meters)
                 ssp=None,                   # Numpy array of Sound Speed Profile (same length as ssp_depths), (Meters/second)
                 bath_ranges=None,           # Numpy array of bathymetry range values (Kilometers)
                 bath_depths=None,           # Numpy array of bathymetry depths (same length as bath_ranges), (Meters)
                 ati_depths=None,
                 freq=None,
                 nmedia=None,
                 sspopt=None,
                 surface_opt=None,
                 bottom_type=None,
                 roughness=None,
                 bottom_opt=None,
                 nsd=None,
                 sd=None,
                 nrd=None,
                 rd=None,
                 nrr=None, 
                 rr=None,
                 ray_compute=None,
                 num_beams=None,
                 launch_angles=None,
                 step_size=None,
                 max_depth=None,
                 max_range=None,
                 opt4=None,
                 pair='L'):             # Default for 2D Ray ('L' = List of pairs)
        
        self.dir = dir
        self.filename = filename
        self.ssp_depth = ssp_depths
        self.ssp = ssp
        self.bath_ranges = bath_ranges
        self.bath_depths = bath_depths
        self.ati_depths = ati_depths
        self.freq = freq
        self.nmedia = nmedia
        self.sspopt = sspopt
        self.surface_opt = surface_opt
        self.bottom_type = bottom_type
        self.roughness = roughness
        self.bottom_opt = bottom_opt
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
        self.opt4=opt4
        self.pair=pair


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
            if self.sspopt[3] == "' '":
                f.write(f"'{self.sspopt[0]}{self.sspopt[1]}{self.sspopt[2]} {self.sspopt[4]}'\t\t\t! SSPOPT\n")
            else:
                f.write(f"'{self.sspopt[0]}{self.sspopt[1]}{self.sspopt[2]}{self.sspopt[3]}{self.sspopt[4]}'\t\t\t! SSPOPT\n")
            if self.sspopt[1] == "A":
                f.write(f"{self.surface_opt[0]:.1f}  {self.surface_opt[1]:.2f}  {self.surface_opt[2]:.1f}  {self.surface_opt[3]:.1f}  {self.surface_opt[4]:.1f} /\t\t\t! Surface depth, compressional speed, shear speed, density, and attenuation\n")
            f.write(f"{len(self.ssp_depth)}  {min(self.ssp_depth):.1f}  {max(self.ssp_depth):.1f}\t\t\t! DEPTH of bottom (m)\n")
            for d, s in zip(self.ssp_depth, self.ssp):
                f.write(f"{d:.1f}  {s:.2f}  /\n")
            f.write("\n")
            if self.bottom_type[1] == "' '":
                f.write(f"'{self.bottom_type[0]}' {self.roughness}\t\t\t! BOTTOM TYPE, roughness\n")
            else:
                f.write(f"'{self.bottom_type[0]}{self.bottom_type[1]}' {self.roughness}\t\t\t! BOTTOM TYPE, roughness\n")
            f.write(f"{self.bottom_opt[0]:.1f}  {self.bottom_opt[1]:.2f}  {self.bottom_opt[2]:.1f}  {self.bottom_opt[3]:.1f}  {self.bottom_opt[4]:.1f} /\t\t\t! Bottom depth, compressional speed, shear speed, density, and attenuation\n")
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
            f.write(f"'{self.ray_compute[0]}{self.ray_compute[1]}{self.ray_compute[2]}{self.ray_compute[3]}{self.ray_compute[4]}'\t\t\t! Option: 'R' for ray tracing, 'C' = coherent TL, 'I' = incoherent TL, 'S' = arrivals\n")
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


    def write_ati(self):
        ati_path = os.path.join(self.dir, self.filename + ".ati")
        if len(self.bath_ranges) != len(self.ati_depths):
            raise ValueError("ranges_km and depths_m must be the same length.")
    
        with open(ati_path, 'w') as f:
            f.write(f"'{self.pair}'\n")
            f.write(f"{len(self.bath_ranges)},\n")
            for r, d in zip(self.bath_ranges, self.ati_depths):
                f.write(f"{r:.2f}  {d:.1f} / \n")
        print(f".ati file written: {ati_path}")


    def write_files(self):
        self.write_env()
        if self.bottom_type[1] == "*":
            self.write_bty()
        if self.sspopt[4] == "*":
            self.write_ati()


class Read_TL:
    def __init__(self, 
                 directory, 
                 output_directory,
                 tl_file,
                 freqs,  # renamed to plural for clarity
                 bath_ranges):
        
        self.dir = directory
        self.output_directory = output_directory
        self.tl_file = tl_file
        self.freqs = freqs
        self.bath_ranges = bath_ranges
    

    def read_shd(self, freq):
        # Assuming file naming changes with frequency, e.g., arms_1_tl_100.shd
        filename = f"{self.dir}{self.tl_file}.shd"
        _, _, _, _, _, pressure = read_shd(filename, freq)
        return pressure


    def plot_frame(self, ax, pressure, freq):
        ax.clear()
        pressure = abs(pressure)
        pressure = 10 * np.log10(pressure / np.max(pressure))
        levs = np.linspace(-30, 0, 31)

        im = ax.contourf(np.squeeze(pressure), levels=levs, cmap='viridis')
        ax.invert_yaxis()

        ax.set_title(f"{self.tl_file}, Frequency: {freq/1000:.1f} kHz")
        ax.set_xlabel("Range (km)")
        ax.set_ylabel("Depth (m)")

        # Tick labeling
        n_range_pts = pressure.shape[-1]
        interpolated_ranges = np.linspace(self.bath_ranges[0], self.bath_ranges[-1], n_range_pts)
        tick_locs = np.linspace(0, n_range_pts - 1, 6, dtype=int)
        tick_labels = [f"{interpolated_ranges[i]:.1f}" for i in tick_locs]
        ax.set_xticks(tick_locs)
        ax.set_xticklabels(tick_labels)

        return im


    def tl_animate(self):
        fig, ax = plt.subplots(figsize=(12, 8))
        cbar_ax = fig.add_axes([0.91, 0.15, 0.02, 0.7])  # position of colorbar
        contour = [None]  # to store the contour handle for colorbar

        def update(frame_idx):
            ax.clear()
            freq = self.freqs[frame_idx]
            pressure = self.read_shd(freq)

            pressure = abs(pressure)
            pressure = 10 * np.log10(pressure / np.max(pressure))
            levs = np.linspace(-30, 0, 31)

            cs = ax.contourf(np.squeeze(pressure), levels=levs, cmap='viridis')
            ax.invert_yaxis()
            ax.set_title(f"{self.tl_file}, Frequency: {freq/1000:.1f} kHz")
            ax.set_xlabel("Range (km)")
            ax.set_ylabel("Depth (m)")

            # Set x-ticks
            n_range_pts = pressure.shape[-1]
            interpolated_ranges = np.linspace(self.bath_ranges[0], self.bath_ranges[-1], n_range_pts)
            tick_locs = np.linspace(0, n_range_pts - 1, 6, dtype=int)
            tick_labels = [f"{interpolated_ranges[i]:.1f}" for i in tick_locs]
            ax.set_xticks(tick_locs)
            ax.set_xticklabels(tick_labels)

            # Update colorbar
            cbar_ax.clear()
            fig.colorbar(cs, cax=cbar_ax, label="Relative TL (dB)")

            return cs.collections

        anim = animation.FuncAnimation(
            fig, update,
            frames=len(self.freqs),
            blit=False,
            repeat=False
        )

        output_path = f"{self.output_directory}{self.tl_file}_sweep.mp4"
        anim.save(output_path, writer='ffmpeg', fps=5)
        print(f"Saved animation to {output_path}")

    def plot_tl(self, pressure):
        pressure = abs(pressure)
        pressure = 10 * np.log10(pressure / np.max(pressure))
        levs = np.linspace(-30, 0, 31)

        plt.contourf(np.squeeze(pressure), levels=levs, cmap='viridis')
        plt.gca().invert_yaxis()

        plt.title(f"{self.tl_file}, Frequency: {self.freqs[0]/1000:.1f} kHz")
        plt.xlabel("Range (km)")
        plt.ylabel("Depth (m)")

        # Tick labeling
        ax = plt.gca()
        n_range_pts = pressure.shape[-1]
        interpolated_ranges = np.linspace(self.bath_ranges[0], self.bath_ranges[-1], n_range_pts)
        tick_locs = np.linspace(0, n_range_pts - 1, 6, dtype=int)
        tick_labels = [f"{interpolated_ranges[i]:.1f}" for i in tick_locs]
        ax.set_xticks(tick_locs)
        ax.set_xticklabels(tick_labels)
        plt.savefig(self.output_directory + self.tl_file + ".png", dpi=300)
        
