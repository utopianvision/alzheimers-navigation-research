import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve

# ── Parameters ───────────────────────────────────────────────────────────────
tau = 20.0
dt = 0.2
N = 70
L = 60.0
dx = L / N

sigma_e = 3.0
sigma_i = 5.0
I_ext = 4.0

# ── Activation Function ──────────────────────────────────────────────────────
def phi(x):
    return np.maximum(x, 0)

# ── Kernel Construction ──────────────────────────────────────────────────────
def make_kernel(Ae, Ai):
    k_width = int(3 * sigma_i / dx)
    k_range = np.arange(-k_width, k_width + 1) * dx
    KX, KY = np.meshgrid(k_range, k_range)
    R_sq = KX**2 + KY**2

    W = Ae * np.exp(-R_sq / (2 * sigma_e**2)) - \
        Ai * np.exp(-R_sq / (2 * sigma_i**2))

    return W * (dx * dx)

# ── Simulation ───────────────────────────────────────────────────────────────
def run_simulation(steps, R_initial, Ae, Ai, mask=None):
    R = R_initial.copy()
    if mask is None:
        mask = np.ones_like(R)

    W_kernel = make_kernel(Ae, Ai)

    for _ in range(steps):
        R *= mask
        recurrent_input = convolve(R, W_kernel, mode='wrap')
        total_input = recurrent_input + I_ext
        dR = (-R + phi(total_input)) / tau
        R = R + dt * dR
        R = np.clip(R, 0, 20)

    return R

# ── Run Disease Timeline ─────────────────────────────────────────────────────
np.random.seed(10)
R_start = np.random.rand(N, N)

results = []
stage_names = []

# Healthy
R_healthy = run_simulation(4000, R_start, Ae=1.0, Ai=0.5)
results.append(R_healthy)
stage_names.append("Healthy")

# Early AD – Reduced Inhibition
R_early = run_simulation(2000, R_healthy, Ae=1.0, Ai=0.4)
results.append(R_early)
stage_names.append("Early AD")

# Moderate AD – Reduced Excitation
R_moderate = run_simulation(2000, R_healthy, Ae=0.8, Ai=0.5)
results.append(R_moderate)
stage_names.append("Moderate AD")

# Late AD – 50% Neuron Death
death_mask = np.random.choice([0, 1], size=(N, N), p=[0.5, 0.5])
R_late = run_simulation(2000, R_healthy, Ae=1.0, Ai=0.5, mask=death_mask)
results.append(R_late)
stage_names.append("Late AD")

# --- 4. Plotting ---
fig, axes = plt.subplots(1, 4, figsize=(18, 4))
fig.patch.set_facecolor("white")

global_vmax = max(r.max() for r in results) * 1.05

for i, ax in enumerate(axes):
    im = ax.imshow(
        results[i],
        cmap='plasma',
        origin='lower',
        vmin=0,
        vmax=global_vmax
    )
    
    ax.set_title(
        stage_names[i],
        fontsize=20,
        fontweight='bold',
        color="#1a1a2e",
        pad=8
    )
    
    ax.set_xticks([])
    ax.set_yticks([])
    
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    ax.set_facecolor("#f8f9fa")

plt.suptitle(
    "Computational Timeline of Alzheimer's Pathology",
    fontsize=25,
    fontweight="bold",
    color="#1a1a2e",
    y=1.02
)

plt.tight_layout(w_pad=2)
plt.show()