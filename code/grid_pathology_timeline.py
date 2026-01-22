import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve

# --- 1. Global Parameters ---
tau = 20.0       
dt = 0.2         
N = 70           # Requested Size
L = 60.0         # Adjusted L to keep resolution similar (dx ~ 0.85)
dx = L / N       

# Healthy Baseline Parameters
sigma_e = 3.0    
sigma_i = 5.0    
base_Ae = 1.0        
base_Ai = 0.5        
I_ext = 4.0      

# --- 2. Helper Functions ---

def phi(x):
    return np.maximum(x, 0)

def make_kernel(Ae, Ai):
    k_width = int(3 * sigma_i / dx) 
    k_range = np.arange(-k_width, k_width + 1) * dx
    K_X, K_Y = np.meshgrid(k_range, k_range)
    R_sq_kernel = K_X**2 + K_Y**2
    
    W = Ae * np.exp(-R_sq_kernel / (2 * sigma_e**2)) - \
        Ai * np.exp(-R_sq_kernel / (2 * sigma_i**2))
    return W * (dx * dx)

def run_simulation(steps, R_initial, Ae, Ai, mask=None):
    R = R_initial.copy()
    if mask is None:
        mask = np.ones_like(R)

    # Create the specific kernel for this stage
    W_kernel = make_kernel(Ae, Ai)

    for i in range(steps):
        # Apply death mask (if any)
        R = R * mask
        
        recurrent_input = convolve(R, W_kernel, mode='wrap')
        total_input = recurrent_input + I_ext
        dR = (-R + phi(total_input)) / tau
        R = R + dt * dR
        
        # Clamp for stability
        R = np.clip(R, 0, 20) 
            
    return R

# --- 3. Run The Timeline ---

np.random.seed(10) # Seed 10 for consistent patterns
R_start = np.random.rand(N, N) * 1.0 

# Store results for plotting
results = []
stage_names = []

# STAGE 1: HEALTHY CONTROL
# Balanced Excitation/Inhibition
print("Simulating Stage 1: Healthy...")
R_healthy = run_simulation(4000, R_start, Ae=1.0, Ai=0.5)
results.append(R_healthy)
stage_names.append("1. Healthy\n(Balanced E/I)")

# STAGE 2: EARLY AD (HYPEREXCITABILITY)
# Theory: Interneurons die/fail first.
# Simulation: Weaken Inhibition (Ai) by 20%
print("Simulating Stage 2: Hyperexcitability...")
# We start from the healthy state to see how it degrades
R_hyper = run_simulation(2000, R_healthy, Ae=1.0, Ai=0.4) 
results.append(R_hyper)
stage_names.append("2. Early AD\n(Hyperexcitability - Low Inhib)")

# STAGE 3: MILD-MODERATE AD (SYNAPTIC WEAKENING)
# Theory: Amyloid attacks excitatory synapses.
# Simulation: Reduce Excitation (Ae) by 20% (from healthy baseline)
# Note: Usually follows hyperexcitability, but we simulate 'silence' phase here.
print("Simulating Stage 3: Synaptic Weakening...")
R_weak = run_simulation(2000, R_healthy, Ae=0.8, Ai=0.5)
results.append(R_weak)
stage_names.append("3. Moderate AD\n(Synaptic Weakening - Low Excit)")

# STAGE 4: LATE AD (NEURON DEATH)
# Theory: Neurons physically die (Atrophy).
# Simulation: Healthy params, but 50% of neurons removed.
print("Simulating Stage 4: Neuron Death...")
death_mask = np.random.choice([0, 1], size=(N, N), p=[0.5, 0.5]) # 50% Death
R_death = run_simulation(2000, R_healthy, Ae=1.0, Ai=0.5, mask=death_mask)
results.append(R_death)
stage_names.append("4. Late AD\n(50% Neuron Death)")

# --- 4. Plotting ---
fig, axes = plt.subplots(1, 4, figsize=(24, 6))

for i, ax in enumerate(axes):
    # Use 'plasma' for high contrast
    im = ax.imshow(results[i], cmap='plasma', origin='lower', 
                   vmin=0, vmax=12) # Fixed scale for comparison
    ax.set_title(stage_names[i], fontsize=14, fontweight='bold')
    ax.axis('off') 

# Add colorbar
cbar_ax = fig.add_axes([0.92, 0.15, 0.01, 0.7])
fig.colorbar(im, cax=cbar_ax, label='Firing Rate')

plt.suptitle(f"Computational Timeline of Alzheimer's Pathology (N={N})", fontsize=18)
plt.show()