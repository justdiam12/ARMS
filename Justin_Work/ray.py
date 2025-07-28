import numpy as np
import matplotlib.pyplot as plt
import os

class Write_RAY:
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
            f.write(f"'{self.sspopt[0]}{self.sspopt[1]}{self.sspopt[2]}{self.sspopt[3]}{self.sspopt[4]}'\t\t\t! SSPOPT\n")
            if self.sspopt[1] == "A":
                f.write(f"{self.surface_opt[0]:.1f}  {self.surface_opt[1]:.2f}  {self.surface_opt[2]:.1f}  {self.surface_opt[3]:.1f}  {self.surface_opt[4]:.1f} /\t\t\t! Surface depth, compressional speed, shear speed, density, and attenuation\n")
            f.write(f"{len(self.ssp_depth)}  {min(self.ssp_depth):.1f}  {max(self.ssp_depth):.1f}\t\t\t! DEPTH of bottom (m)\n")
            for d, s in zip(self.ssp_depth, self.ssp):
                f.write(f"{d:.1f}  {s:.2f}  /\n")
            f.write("\n")
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


class Read_RAY:
    def __init__(self, 
                 directory=None, 
                 output_directory=None,
                 ray_file=None, 
                 ssp_depths=None, 
                 ssp=None, 
                 bath_ranges=None, 
                 bath_depths=None, 
                 ati_depths=None,
                 s_depth=None, 
                 r_depth=None, 
                 r_range=None,
                 precision=None,
                 bottom_opt=None,
                 surface_opt=None):
        
        self.dir = directory
        self.output_directory = output_directory
        self.ray_file = ray_file
        self.ssp_depths = ssp_depths
        self.ssp = ssp
        self.bath_ranges = bath_ranges
        self.bath_depths = bath_depths
        self.ati_depths = ati_depths
        self.ray_file_path = self.dir + self.ray_file + ".ray"
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

            # Plot ray
            axs[0].plot(r,z)

            # if np.abs(z[-1] - self.r_depth) <= self.precision and np.abs(r[-1] - self.r_range) <= self.precision:
            #     if alphas[i] < 0:
            #         up_down = -1
            #     elif alphas[i] > 0:
            #         up_down = 1
                
            #     # Get the indices where the ray bounces off the surface or bottom
            #     sign_change = np.diff(np.sign(np.diff(z)))
            #     p_and_t = np.where(sign_change != 0)[0]
            #     bounce_indices = p_and_t[np.where(np.diff(p_and_t) > 1)]
            #     bounce_indices = np.append(bounce_indices, p_and_t[-1])

                # # Get the reflection coefficient
                # R_string = ""
                # R = 1
                # for b in range(len(bounce_indices)):
                #     R_string = self.R_type(R_string, up_down)
                #     if up_down == -1:
                #         dr = np.abs(r[bounce_indices[b]] - r[bounce_indices[b]-10])
                #         dz = np.abs(z[bounce_indices[b]] - z[bounce_indices[b]-10])
                #         angle = np.degrees(np.arctan(dz/dr))
                #         sin_angle = np.sin(np.radians(angle))
                #         surface_Z = np.array(self.surface_Z, dtype=float)
                #         water_top_Z = np.array(self.water_top_Z, dtype=float)
                #         R = (surface_Z * sin_angle - water_top_Z * sin_angle) / (surface_Z * sin_angle + water_top_Z * sin_angle) * R
                #         up_down = 1
                #     else:
                #         dr = np.abs(r[bounce_indices[b]] - r[bounce_indices[b]-10])
                #         dz = np.abs(z[bounce_indices[b]] - z[bounce_indices[b]-10])
                #         angle = np.degrees(np.arctan(dz/dr))
                #         sin_angle = np.sin(np.radians(angle))
                #         bottom_Z = np.array(self.bottom_Z, dtype=float)
                #         water_bottom_Z = np.array(self.water_bottom_Z, dtype=float)
                #         R = (bottom_Z * sin_angle - water_bottom_Z * sin_angle) / (bottom_Z * sin_angle + water_bottom_Z * sin_angle) * R
                #         up_down = -1
                
                # if R_string not in self.bounce:
                #     self.bounce.append(R_string)
                #     self.alpha.append(alphas[i])
                #     self.R = np.append(self.R, R) 
                #     axs[0].plot(r,z, label=R_string)

        # sea_surface = np.zeros((len(self.bath_ranges)))
        axs[0].invert_yaxis()
        # axs[0].plot(self.bath_ranges, sea_surface, "--", color="black", linewidth=3)
        axs[0].plot(self.bath_ranges, self.ati_depths, "--", color="black", linewidth=3)
        axs[0].plot(0, self.s_depth, "bo", linewidth=3)
        axs[0].plot(self.r_range, self.r_depth, "ro", linewidth=3)
        axs[0].plot(self.bath_ranges, self.bath_depths, color="black", linewidth=3)
        axs[0].set_xlabel("Range (km)")
        axs[0].set_ylabel("Depth (m)")
        axs[0].set_title("Eigenrays")

        axs[1].plot(self.ssp, self.ssp_depths)
        axs[1].set_title("Sound Speed Profile")
        axs[1].set_xlabel("Sound Speed (m/s)")
        plt.savefig(self.output_directory + self.ray_file + ".png", dpi=300, bbox_inches='tight')
        plt.tight_layout()
                                
            
    def R_type(self, R_string, up_down):
        if up_down == 1:
            R_string += "B"
        else:
            R_string += "S"

        return R_string