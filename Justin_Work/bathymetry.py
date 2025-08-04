import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import RegularGridInterpolator
from matplotlib import gridspec
import scipy.io as io

# This function creates a 2D Map of Dabob Bathymetry (returns the 2D map as np.array, lon_range, and lat_range)
def map_2D(directory="/Users/justindiamond/Documents/Documents/UW-APL/Research/ARMS/Justin_Work/Data/Collected_Dabob_Bathymetry_combined.xlsx"):
    # Get Bathymetry Data
    data = pd.read_excel(directory, engine='openpyxl')
    data = data.to_numpy()

    # Extract lat, long, and depth
    latitude = np.array(data[:, 0])
    longitude = np.array(data[:, 1])
    depth = np.array(data[:, 2])

    # Range of latitude and longitude values
    lat_range = np.unique(latitude)
    lon_range = np.unique(longitude)

    bath_map = np.zeros((len(lat_range), len(lon_range)))

    for l in range(len(latitude)):
        lat_index = np.where(lat_range == latitude[l])[0]
        lon_index = np.where(lon_range == longitude[l])[0]
        bath_map[lat_index, lon_index] = depth[l]

    return bath_map, lon_range, lat_range

# This function plots a 2D bathymetry
def plot_2D_bathy(bath_map, lon_range, lat_range, save_dir=None):
    extent = [
        lon_range[0], lon_range[-1],  # x-axis: min to max longitude
        lat_range[0], lat_range[-1]   # y-axis: min to max latitude
    ]

    # Set figure size
    plt.figure(figsize=(5, 8))
    plt.imshow(bath_map, cmap='viridis', interpolation='nearest',
               origin='lower', extent=extent, aspect='auto')

    plt.colorbar(label='Depth')
    plt.title("Bathymetry")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    x_ticks = np.linspace(lon_range[0], lon_range[-1], 6)
    y_ticks = np.linspace(lat_range[0], lat_range[-1], 6)
    plt.xticks(x_ticks.round(2), rotation=45)
    plt.yticks(y_ticks.round(2))
    plt.tight_layout()
    if save_dir:
        plt.savefig(save_dir, dpi=300, bbox_inches='tight')
    plt.show()


# This function extracts a 1D bathymetry profile from a 2D bathymetry map (returns 1D profile as np.array)
def map_1D(bath_map, lon_range, lat_range, lon_start, lon_end, lat_start, lat_end, num_points=1000):
    interp = RegularGridInterpolator((lat_range, lon_range), bath_map, bounds_error=False, fill_value=np.nan)

    # Generate evenly spaced points along the trackline
    lons = np.linspace(lon_start, lon_end, num_points)
    lats = np.linspace(lat_start, lat_end, num_points)
    track_points = np.column_stack((lats, lons))

    # Interpolate bathymetry values
    profile = interp(track_points)

    # Compute cumulative distance (approximate, assuming small region)
    distances = np.sqrt((lons - lons[0])**2 + (lats - lats[0])**2)
    distances *= 111  # Rough conversion from degrees to km

    return profile, distances


def plot_1D_bathy(profile, distances, save_dir=None):
    plt.figure(figsize=(10,6))
    plt.plot(distances, profile, linewidth=2)
    plt.title("Trackline Profile")
    plt.xlabel("Distance (km)")
    plt.ylabel("Depth (m)")
    if save_dir:
        plt.savefig(save_dir, dpi=300, bbox_inches='tight')
    plt.show() 

def plot_all(bath_map, lon_range, lat_range, profile, distances, lon_start, lon_end, lat_start, lat_end, save_dir=None):
    extent = [
        lon_range[0], lon_range[-1],
        lat_range[0], lat_range[-1]
    ]

    fig = plt.figure(figsize=(12, 5))
    gs = gridspec.GridSpec(1, 2, width_ratios=[1, 2], wspace=0.3)

    ax0 = fig.add_subplot(gs[0])
    ax1 = fig.add_subplot(gs[1])
    
    im = ax0.imshow(bath_map, cmap='viridis', interpolation='nearest',
                origin='lower', extent=extent, aspect='auto')

    cbar = fig.colorbar(im, ax=ax0)
    cbar.set_label('Depth (m)')

    ax0.set_title("Bathymetry")
    ax0.set_xlabel("Longitude")
    ax0.set_ylabel("Latitude")

    x_ticks = np.linspace(lon_range[0], lon_range[-1], 6)
    y_ticks = np.linspace(lat_range[0], lat_range[-1], 6)
    ax0.set_xticks(x_ticks)
    ax0.set_xticklabels([f"{xtick:.2f}" for xtick in x_ticks], rotation=45)
    ax0.set_yticks(y_ticks)
    ax0.set_yticklabels([f"{ytick:.2f}" for ytick in y_ticks])

    ax0.plot([lon_start, lon_end], [lat_start, lat_end],
             color='red', linewidth=2, linestyle='--', label='Trackline')

    ax1.plot(distances, profile, linewidth=2)
    ax1.set_title("Trackline Profile")
    ax1.set_xlabel("Distance (km)")
    ax1.set_ylabel("Depth (m)")

    fig.tight_layout()

    if save_dir:
        plt.savefig(save_dir, bbox_inches='tight', dpi=300)
        io.savemat('/Users/justindiamond/Documents/Documents/UW-APL/Research/ARMS/Justin_Work/Data/track_info.mat', 
                    {'bath_map': bath_map,
                    'lon_range': lon_range, 
                    'lat_range': lat_range, 
                    'profile': profile, 
                    'distances': distances, 
                    'lon_start': lon_start, 
                    'lon_end': lon_end, 
                    'lat_start': lat_start, 
                    'lat_end': lat_end}) 
    else:
        plt.show()

# Latitude and Longitude inputs for the 1D trackline
lon_start=-122.83
lon_end=-122.85
lat_start=47.77
lat_end=47.71

save_dir = "/Users/justindiamond/Documents/Documents/UW-APL/Research/ARMS/Justin_Work/Output/dabob_bath.png"

# Create the map
# dabob_map, lon_range, lat_range = map_2D(directory="/Users/justindiamond/Documents/Documents/UW-APL/Research/ARMS/Justin_Work/Data/Collected_Dabob_Bathymetry_combined.xlsx")
# plot_2D_bathy(dabob_map, lon_range, lat_range, save_dir="/Users/justindiamond/Documents/Documents/UW-APL/Research/ARMS/Justin_Work/Ouput/dabob_bath.png")
# profile, distances = map_1D(bath_map=dabob_map, lon_range=lon_range, lat_range=lat_range, lon_start=lon_start, lon_end=lon_end, lat_start=lat_start, lat_end=lat_end, num_points=200)
# plot_1D_bathy(profile, distances)
# plot_all(dabob_map, lon_range, lat_range, profile, distances, lon_start=lon_start, lon_end=lon_end, lat_start=lat_start, lat_end=lat_end, save_dir=None)