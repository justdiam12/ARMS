import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from struct import unpack
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
                 directory=None, 
                 tl_file=None,
                 freqs=None,
                 bath_depths=None,
                 bath_ranges=None,
                 ati_depths=None,
                 ati_ranges=None):
        
        self.directory = directory
        self.tl_file = tl_file
        self.freqs = freqs
        self.bath_depths = bath_depths
        self.bath_ranges = bath_ranges
        self.ati_depths = ati_depths
        self.ati_ranges = ati_ranges
    

    def read_shd_main(self, freq):
        # Assuming file naming changes with frequency, e.g., arms_1_tl_100.shd
        filename = os.path.join(self.directory, self.tl_file + ".shd")
        _, _, _, _, _, pressure = self.read_shd(filename, freq)
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

        output_path = f"{self.directory}{self.tl_file}_sweep.mp4"
        anim.save(output_path, writer='ffmpeg', fps=5)
        print(f"Saved animation to {output_path}")


    def plot_tl(self, pressure):
        pressure = abs(pressure)
        pressure = 10 * np.log10(pressure / np.max(pressure))
        levs = np.linspace(-30, 0, 31)

        plt.figure(figsize=(12, 8))
        plt.contourf(np.squeeze(pressure), levels=levs, cmap='viridis')
        plt.colorbar(label="Relative TL (dB)")
        plt.gca().set_aspect('auto')
        plt.tight_layout()
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
        plt.savefig(os.path.join(self.directory, self.tl_file + ".png"), dpi=300)
        plt.show()
    

    def fileparts(self, fname):
        fpath = os.path.dirname(os.path.abspath(fname))
        if '.' not in fname:
            ext = None
        else:
            ext_ind = [i for i in range(len(fname)) if fname[i]=='.']
            if len(ext_ind) > 1:
                print('Warning: lots of periods...')
                #raise ValueError("something fishy about a filename with two periods")
            ext_ind = ext_ind[-1]
            ext = fname[ext_ind:]
            #print('ext', ext)
            fname = fname[:ext_ind]
        return fpath, fname, ext
    

    def read_shd_bin(self, *varargin):
        s   = Source(0)
        r   = Dom(0,0)
        pos = Pos(s,r)
        '''
        Read TL surfaces from a binary Bellhop/Kraken .SHD file
        without having to convert to ASCII first.
        Useage:
        ... = read_shd_bin( filename, xs, ys )
        where (xs, ys) is the source coordinate in km
        (xs, ys) are optional
        Output is a 4-D pressure field p( Ntheta, Nsd, Nrd, Nrr )
        '''
        if (len(varargin) < 1) or (len(varargin) > 3):
            raise ValueError("Can only pass one to three arguments: filename; (filename, xs, ys); or (filename, freq)")

        filename = varargin[0]

        # optional frequency
        if len(varargin) == 2:
            freq = varargin[1]
        else:
            freq = np.NaN

        # optional source (x,y) coordinate
        if len(varargin) >= 3:
            xs = varargin[1]
            ys = varargin[2]
        else:
            xs = np.NaN
            ys = np.NaN

        ##
        f = open( filename, 'rb' )

        recl     = unpack('<I', f.read(4))[0];     #record length in bytes will be 4*recl
        title    = unpack('80s', f.read(80))

        f.seek(4 * recl); #reposition to end of first record
        PlotType = unpack('10s', f.read(10))

        f.seek(2 * 4 * recl); #reposition to end of second record
        Nfreq  = unpack('<I', f.read(4))[0]
        Ntheta = unpack('<I', f.read(4))[0]
        Nsx    = unpack('<I', f.read(4))[0]
        Nsy    = unpack('<I', f.read(4))[0]
        Nsd    = unpack('<I', f.read(4))[0]
        Nrd    = unpack('<I', f.read(4))[0]
        Nrr    = unpack('<I', f.read(4))[0]
        atten  = unpack('<I', f.read(4))[0]
        f.seek(3 * 4 * recl); #reposition to end of record 3
        freqVec = unpack(str(Nfreq) +'d', f.read(Nfreq*8))

        f.seek(4 * 4 * recl) ; #reposition to end of record 4
        pos.theta   = unpack(str(Ntheta) +'f', f.read(4*Ntheta))[0]

        if ( PlotType[ 1 : 2 ] != 'TL' ):
            f.seek(5 * 4 * recl); #reposition to end of record 5
            pos.s.x     = unpack(str(Nsx)+'f',  f.read(Nsx*4))
            f.seek( 6 * 4 * recl); #reposition to end of record 6
            pos.s.y     = unpack(str(Nsy) + 'f', f.read(Nsy*4))
        else:   # compressed format for TL from FIELD3D
            f.seek(5 * 4 * recl, -1 ); #reposition to end of record 5
            pos.s.x     = f.read(2,    'float32' )
            pos.s.x     = np.linspace( pos.s.x[0], pos.s.x[-1], Nsx )
            
            f.seek(6 * 4 * recl, -1 ); #reposition to end of record 6
            pos.s.y     = f.read(2,    'float32' )
            pos.s.y     = np.linspace( pos.s.y[0], pos.s.y[-1], Nsy )

        f.seek(7 * 4 * recl); #reposition to end of record 7
        pos.s.depth = unpack(str(Nsd)+'f', f.read(Nsd*4))
        pos.s.depth = np.array(pos.s.depth)

        f.seek(8 * 4 * recl); #reposition to end of record 8
        pos.r.depth = unpack(str(Nrd) + 'f', f.read(Nrd*4))
        pos.r.depth = np.array(pos.r.depth)

        f.seek(9 * 4 * recl); #reposition to end of record 9
        pos.r.range = unpack(str(Nrr) + 'f',f.read(Nrr*4))
        # pos.r.range = pos.r.range';   # make it a row vector
        pos.r.range = np.array(pos.r.range)
        pos.r.range = np.round(pos.r.range, 3)
        ##
        # Each record holds data from one source depth/receiver depth pair

        if PlotType == 'rectilin  ':
            pressure = np.zeros(( Ntheta, Nsd, Nrd, Nrr ), dtype=np.complex128)
            Nrcvrs_per_range = Nrd
        if PlotType == 'irregular ':
            pressure = np.zeros(( Ntheta, Nsd,   1, Nrr ), dtype=np.complex128)
            Nrcvrs_per_range = 1
        else:
            pressure = np.zeros(( Ntheta, Nsd, Nrd, Nrr ), dtype=np.complex128)
            Nrcvrs_per_range = Nrd

        ##
        if np.isnan( xs ):    # Just read the first xs, ys, but all theta, sd, and rd
            # get the index of the frequency if one was selected
            ifreq = 0
            if not np.isnan(freq):
                freqdiff = [abs( x - freq ) for x in freqVec]
                ifreq = min( freqdiff )

            for itheta in range (Ntheta):
                for isd in range(Nsd):
                    # disp( [ 'Reading data for source at depth ' num2str( isd ) ' of ' num2str( Nsd ) ] )
                    for ird in range( Nrcvrs_per_range):
                        recnum = 10 + ( ifreq   ) * Ntheta * Nsd * Nrcvrs_per_range + \
                                    ( itheta  )          * Nsd * Nrcvrs_per_range + \
                                    ( isd     )                * Nrcvrs_per_range + \
                                        ird    
                        status = f.seek(int(recnum) * 4 * recl); #Move to end of previous record
                        if ( status == -1 ):
                            raise ValueError( 'Seek to specified record failed in read_shd_bin' )
                        temp = unpack(str(2*Nrr)+'f', f.read(2 * Nrr*4));    #Read complex data
                        pressure[ itheta, isd, ird, : ] = temp[ 0 : 2 * Nrr -1 : 2 ] + complex(0,1) *np.array((temp[ 1 : 2 * Nrr :2]))
                        # Transmission loss matrix indexed by  theta x sd x rd x rr
                        
        else:              # read for a source at the desired x, y, z.
            
            xdiff = abs( pos.s.x - xs * 1000. )
            [ holder, idxX ] = min( xdiff )
            ydiff = abs( pos.s.y - ys * 1000. )
            [ holder, idxY ] = min( ydiff )
            
            # show the source x, y that was found to be closest
            # [ pos.s.x( idxX ) pos.s.y( idxY ) ]
            for itheta in range(Ntheta):
                for isd in range(Nsd):
                    # disp( [ 'Reading data for source at depth ' num2str( isd ) ' of ' num2str( Nsd ) ] )
                    for ird in range(Nrcvrs_per_range):
                        recnum = 10 + ( idxX   - 1 ) * Nsy * Ntheta * Nsd * Nrcvrs_per_range +   \
                                    ( idxY   - 1 )       * Ntheta * Nsd * Nrcvrs_per_range +  \
                                    ( itheta - 1 )                * Nsd * Nrcvrs_per_range +  \
                                    ( isd    - 1 )                      * Nrcvrs_per_range + ird - 1
                        status = f.seek(recnum * 4 * recl); # Move to end of previous record
                        if ( status == -1 ):
                            raise ValueError( 'Seek to specified record failed in read_shd_bin' )
                        
                        temp = f.read(2 * Nrr, 'float32' );    #Read complex data
                        pressure[ itheta, isd, ird, : ] = temp[ 1 : 2 : 2 * Nrr ] + complex(0,1) * np.array(temp[ 2 : 2 : 2 * Nrr ])
                        # Transmission loss matrix indexed by  theta x sd x rd x rr
                        
        f.close()
        return [ title, PlotType, freqVec, atten, pos, pressure ] 
    

    def read_shd (self, *varargin):
        '''
        Read the shade file
        [ PlotTitle, PlotType, freqVec, atten, Pos, pressure ] return vals
        calls the appropriate routine (binary, ascii, or mat file) to read in the pressure field
        
        usage: [ PlotTitle, PlotType, freqVec, atten, Pos, pressure ] = read_shd( filename )
            Reads first source.
                [ PlotTitle, PlotType, freqVec, atten, Pos, pressure ] = read_shd( filename, xs, ys )
            Reads source at the specified xs, ys coordinate.
                [ PlotTitle, PlotType, freqVec, atten, Pos, pressure ] = read_shd( filename, freq )
            Reads source at the specified frequency.
        
        Recommended to include a file extension, if it exists.
        Otherwise it may find a different file than you intended.
        
        Output is a 5-D pressure field p( Nfreq, Ntheta, Nsd, Nrd, Nrr )
        
        If omitted, take a guess at the extension
        Matlab 'exist' command is simpler; however, it searches the whole Matlab search path.
        '''


        # Determine type of file:

        #error( nargchk( 1, 3, len(varargin), 'struct' ) )
        if (len(varargin) < 1) or (len(varargin) > 3):
            raise ValueError("Can only pass one to three arguments: filename; (filename, xs, ys); or (filename, freq)")

        filename = varargin[0]

        # optional frequency
        if len(varargin) == 2:
            freq = varargin[1]
        else:
            freq = np.NaN

        # optional source (x,y) coordinate
        if len(varargin) >= 3:
            xs = varargin[1]
            ys = varargin[2]
        else:
            xs = np.NaN
            ys = np.NaN

        PlotType = [];  # in case this was not set

        [holder , name, ext ] = self.fileparts( filename )
        if (  ext == '.mat' ) :
            [ holder, holder1, ext2 ] = self.fileparts( name )

            if ext2 == '.shd':
                FileType = 'shdmat'
            elif ext2 == '.grn':
                FileType = 'grnmat'
            else:
                pass
        else:
            if filename == 'ASCFIL':
                FileType = 'asc'
            elif filename == 'SHDFIL':
                FileType = 'shd'
            elif filename == 'tl.grid':
                FileType = 'RAM'
            else:
                endchar = len( filename )
                if ( endchar >= 4 ):
                    FileType = filename[ endchar - 3 : endchar ].lower()

        ##
        if FileType in ['shd', 'grn' ]:   # binary format
            if len(varargin) ==  1:
                [ PlotTitle, PlotType, freqVec, atten, pos, pressure ] = self.read_shd_bin( filename )
            if len(varargin) ==  2:
                [ PlotTitle, PlotType, freqVec, atten, pos, pressure ] = self.read_shd_bin( filename, freq )
            if len(varargin) ==  3:
                [ PlotTitle, PlotType, freqVec, atten, pos, pressure ] = self.read_shd_bin( filename, xs, ys )
        else:
            raise ValueError( 'Unrecognized file extension' )

        # clean up PlotTitle by taking only the part up inside the quotes
        # nchars = strfind( PlotTitle, '''' );   # find quotes
        # PlotTitle = [ PlotTitle( nchars( 1 ) + 1 : nchars( 2 ) - 1 ) ]
        return [ PlotTitle, PlotType, freqVec, atten, pos, pressure ] 


class Source:
    def __init__(self, depth):
        self.depth = depth
        self.x = None
        self.y = None

class Dom:
    def __init__(self, ran, depth, offsets=None):
        self.range = ran # in km
        self.depth = depth
        if offsets is not None:
            self.offsets = offsets

class Pos:
    def __init__(self, Source, Dom):
        self.s = Source
        self.r = Dom

class Ice:
    def __init__(self, BumDen, eta, xi):
        self.BumDen=  BumDen
        self.eta = eta
        self.xi = xi