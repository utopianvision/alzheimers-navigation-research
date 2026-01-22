import mne
import numpy as np
import matplotlib.pyplot as plt
from mne.viz import plot_topomap

# Paths to the saved files
ad_save_path = "ad_group.fif"
cn_save_path = "cn_group.fif"

# Load the recordings
ad_data = mne.io.read_raw_fif(ad_save_path, preload=True)
cn_data = mne.io.read_raw_fif(cn_save_path, preload=True)

print("AD and CN recordings reloaded successfully!")

# Load the control group EEG data
cn_data = mne.io.read_raw_fif(cn_save_path, preload=True)

# Step 1: Set the correct montage (e.g., Standard 10-20)
montage = mne.channels.make_standard_montage("standard_1020")
cn_data.set_montage(montage)

# Step 2: Apply a bandpass filter for theta waves (4–8 Hz)
theta_data = cn_data.copy().filter(l_freq=4, h_freq=8, picks="eeg", verbose=True)

# Step 3: Plot the filtered theta waves for visual inspection
theta_data.plot(duration=10, n_channels=10)  # Adjust duration and number of channels as needed

# Step 4: Compute Power Spectral Density (PSD)
psd = theta_data.compute_psd()
freqs = psd.freqs  # Get the frequency array
psd_data = psd.get_data()  # Get the PSD data (channels x frequencies)

# Step 5: Extract the theta band (4–8 Hz)
theta_indices = np.logical_and(freqs >= 4, freqs <= 8)  # Logical mask for theta band
theta_psd_mean = psd_data[:, theta_indices].mean(axis=1)  # Mean PSD in theta band for each channel

# Step 6: Plot the Topomap of Theta Power with Correct Montage
fig, ax = plt.subplots(figsize=(8, 6))
im, _ = plot_topomap(theta_psd_mean, theta_data.info, cmap="viridis", axes=ax, show=False)

# Add a colorbar
cbar = fig.colorbar(im, ax=ax, orientation="vertical", shrink=0.6)
cbar.set_label("Theta Power (4–8 Hz)", fontsize=12)

plt.title("Theta Power Topomap (4–8 Hz)", fontsize=14)
plt.show()