import numpy as np
import matplotlib.pyplot as plt
import os

class Write_RAY:
    def __init__(self, 
                 dir=None,                   # Save File Directory
                 filename=None,              # Save Filename with no extension
                 ssp_depths=None,            # Numpy array of Sound Speed Profile Depths (Meters)
                 ssp=None,                   # Numpy array of Sound Speed Profile (same length as ssp_depths), (Meters/second)
                 ssp_ranges=None,
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
        self.ssp_ranges = ssp_ranges
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
        if self.ssp_depth.shape[1] != self.ssp.shape[1]:
            raise ValueError("Depths and speeds must have the same length.")

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
            if self.ssp.shape[0] == 1:
                f.write(f"{self.ssp_depth.shape[1]}  {min(self.ssp_depth[0,:]):.1f}  {max(self.ssp_depth[0,:]):.1f}\t\t\t! DEPTH of bottom (m)\n")
            else: 
                f.write(f"{0}  {min(self.ssp_depth[0,:]):.1f}  {max(self.ssp_depth[0,:]):.1f}\t\t\t! DEPTH of bottom (m)\n")
            for d, s in zip(self.ssp_depth[0,:], self.ssp[0,:]):
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
        if self.ssp_depth.shape[1] != self.ssp.shape[1]:
            raise ValueError("Depths and speeds must have the same length.")
    
        with open(ssp_path, 'w') as f:
            if self.ssp.shape[0] == 1:
                f.write(f"'{self.pair}'\n")
                for d, s in zip(self.ssp_depth[0,:], self.ssp[0,:]):
                    f.write(f"{d:.1f}  {s:.2f}  /\n")
            else:
                f.write(f"{self.ssp.shape[1]}\n")
                for i in range(self.ssp_depth.shape[1]):
                    if i == self.ssp_depth.shape[1]-1:
                        f.write(f"{self.ssp_depth[0,i]:0.1f}    \n")
                    else:
                        f.write(f"{self.ssp_depth[0,i]:0.1f}    ")
                for i in range(self.ssp.shape[0]):
                    for j in range(self.ssp.shape[1]):
                        if j == self.ssp.shape[1]-1:
                            f.write(f"{self.ssp[i,j]:0.2f} /\n")
                        else:
                            f.write(f"{self.ssp[i,j]:0.2f} ")
                return

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
        self.write_ssp()
        if self.bottom_type[1] == "*":
            self.write_bty()
        if self.sspopt[4] == "*":
            self.write_ati()


class Read_RAY:
    def __init__(self, 
                 directory=None, 
                 ray_file=None,
                 ray_compute_type=None, 
                 ssp_depths=None, 
                 ssp=None,
                 ssp_ranges=None, 
                 bath_ranges=None, 
                 bath_depths=None, 
                 ati_depths=None,
                 s_depth=None, 
                 r_depth=None, 
                 r_range=None,
                 precision=None,
                 bottom_opt=None,
                 surface_opt=None):
        
        self.directory = directory
        self.ray_file = ray_file
        self.ray_compute_type = ray_compute_type
        self.ssp_depths = ssp_depths
        self.ssp = ssp
        self.ssp_ranges = ssp_ranges
        self.bath_ranges = bath_ranges
        self.bath_depths = bath_depths
        self.ati_depths = ati_depths
        self.ray_file_path = os.path.join(self.directory, self.ray_file + ".ray")
        self.s_depth = s_depth
        self.r_depth = r_depth
        self.r_range = r_range
        self.precision = precision
        self.bottom_opt = bottom_opt
        self.surface_opt = surface_opt

    def read_ray_file(self, filepath):
    
        with open(filepath, 'r') as f:
            lines = f.readlines()

        # Basic metadata
        title = lines[0].strip()
        frequency = float(lines[1].strip())
        nsrc, nrd, nr = map(int, lines[2].strip().split())
        nbeams, ncoords = map(int, lines[3].strip().split())
        src_depth = float(lines[4].strip())
        r_end = float(lines[5].strip())
        coord_type = lines[6].strip()  # should be 'rz'

        # Read ray points
        line = 7
        ray_data = []
        alpha_data = []
        while line <= len(lines)-1:
            alpha_data.append(float(lines[line].strip()))
            npts, ndim, _ = map(int, lines[line+1].strip().split())
            line = line+2
            start_line = line
            ray = []
            for l in lines[start_line:start_line+npts]:
                r, z = map(float, l.strip().split())
                ray.append((r, z))
                line = line + 1
            if self.ray_compute_type == "E":
                in_precision = 0
                for i in range(len(self.r_depth)):
                    if np.abs(ray[-1][1]-self.r_depth[i]) <= self.precision and np.abs(ray[-1][0]-self.r_range[0]*1000) <= self.precision:
                        in_precision = 1
                    else:
                        continue
                if in_precision == 1:
                    ray_data.append(ray)
            elif self.ray_compute_type == "R":
                if np.abs(ray[0][0] - 0) <= self.precision and np.abs(ray[-1][0] - self.r_range[0]*1000) <= self.precision:
                    ray_data.append(ray)

        return ray_data, alpha_data


    def plot_ray_profile(self):
        rays, alphas = self.read_ray_file(self.ray_file_path)
        fig, axs = plt.subplots(1, 2, figsize=(12, 6), sharey=True, gridspec_kw={'width_ratios': [3, 1]})
        
        for i in range(len(rays)):
            ray = rays[i]
            r = []
            z = []
            for j in range(len(ray)):
                index = ray[j]
                r.append(index[0] / 1000)
                z.append(index[1])

            #plot the rays
            axs[0].plot(r,z)

        axs[0].invert_yaxis()
        axs[0].plot(self.bath_ranges, self.ati_depths, "--", color="black", linewidth=3)
        for i in range(len(self.s_depth)):
            axs[0].plot(0, self.s_depth[i], "bo", linewidth=3)
        for i in range(len(self.r_depth)):
            axs[0].plot(self.r_range[0], self.r_depth[i], "ro", linewidth=3)
        axs[0].plot(self.bath_ranges, self.bath_depths, color="black", linewidth=3)
        axs[0].set_xlabel("Range (km)")
        axs[0].set_ylabel("Depth (m)")
        if self.ray_compute_type == "E":
            axs[0].set_title("Eigenray Coordinates")
        elif self.ray_compute_type == "R":
            axs[0].set_title("Ray Coordinates")
        for i in range(self.ssp.shape[0]):
            axs[1].plot(self.ssp[i,:], self.ssp_depths[0,:])
        axs[1].set_title("Sound Speed Profile")
        axs[1].set_xlabel("Sound Speed (m/s)")
        plt.savefig(os.path.join(self.directory, self.ray_file + ".png"), dpi=300, bbox_inches='tight')
        plt.tight_layout()
                                
            
    def R_type(self, R_string, up_down):
        if up_down == 1:
            R_string += "B"
        else:
            R_string += "S"

        return R_string