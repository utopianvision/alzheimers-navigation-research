import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve

# --- 1. Parameters (Stabilized) ---
tau = 20.0       # Slower time constant for stability
dt = 0.2         
N = 150          # Large Grid
L = 100.0        
dx = L / N       

# Parameters optimized for robust Grid Formation
sigma_e = 3.0    
sigma_i = 5.0    
A_e = 1.0        
A_i = 0.5        
I_ext = 4.0      

# Connectivity Kernel
k_width = int(3 * sigma_i / dx) 
k_range = np.arange(-k_width, k_width + 1) * dx
K_X, K_Y = np.meshgrid(k_range, k_range)
R_sq_kernel = K_X**2 + K_Y**2
W_kernel = A_e * np.exp(-R_sq_kernel / (2 * sigma_e**2)) - \
           A_i * np.exp(-R_sq_kernel / (2 * sigma_i**2))
W_kernel *= (dx * dx)

def phi(x):
    return np.maximum(x, 0)

def run_simulation(steps, R_initial, mask=None):
    R = R_initial.copy()
    if mask is None:
        mask = np.ones_like(R)

    for i in range(steps):
        # 1. Apply Death Mask
        R = R * mask
        
        # 2. Convolve
        recurrent_input = convolve(R, W_kernel, mode='wrap')
        
        # 3. Update Dynamics (Euler Integration)
        total_input = recurrent_input + I_ext
        dR = (-R + phi(total_input)) / tau
        R = R + dt * dR
        
        # **FIX: Safety Clamp**
        # If values get too high due to instability, cap them.
        # This prevents the "White Screen / NaN" error.
        R = np.clip(R, 0, 20) 
            
    return R

# --- 2. Phase 1: Establish Healthy Grid ---
print(f"Generating healthy grid (N={N}x{N})...")
np.random.seed(10) # Seed 10 gives a nice pattern

# Start with random noise
R_start = np.random.rand(N, N) * 1.0 

# Run long enough to form a stable grid (needs more steps since dt is smaller)
# 4000 steps * 0.2 dt = 800ms simulation time
R_healthy = run_simulation(4000, R_start) 

# --- 3. Phase 2: Simulate Alzheimer's Progression ---
death_rates = [0.0, 0.30, 0.60, 0.90] # Disease stages
results = []
names = []

print("Simulating neuron death...")
for rate in death_rates:
    print(f"  - Simulating {int(rate*100)}% death...")
    mask = np.random.choice([0, 1], size=(N, N), p=[rate, 1-rate])
    
    # Run short simulation to see how the grid breaks
    R_diseased = run_simulation(1000, R_healthy, mask)
    results.append(R_diseased)
    names.append(f"{int(rate*100)}% Neuron Loss")

# --- 4. Plotting ---
fig, axes = plt.subplots(1, 4, figsize=(24, 6))

for i, ax in enumerate(axes):
    # Use 'viridis' or 'plasma'
    # vmin/vmax ensures the color scale stays consistent across plots
    im = ax.imshow(results[i], cmap='viridis', origin='lower', 
                   vmin=0, vmax=np.percentile(R_healthy, 99))
    ax.set_title(names[i], fontsize=16, fontweight='bold')
    ax.axis('off') 

# Add colorbar
cbar_ax = fig.add_axes([0.92, 0.15, 0.01, 0.7])
fig.colorbar(im, cax=cbar_ax, label='Firing Rate')

plt.suptitle(f"Alzheimer's Model: Degradation of Spatial Map (N={N}x{N})", fontsize=20)
plt.show()