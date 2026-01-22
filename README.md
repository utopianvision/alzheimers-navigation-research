# Modeling Alzheimer’s Disease Through Navigation Circuit Degeneration and Brain Rhythms

This repository contains my ongoing research project studying how Alzheimer’s disease affects the brain's navigation circuits, specifically head-direction cells, grid cells, and place cells. The project combines computational modeling with EEG data analysis to explore circuit-level changes and their behavioral consequences.

---

## Folder Structure

```

project_root/
│
├── code/
│   ├── eeg_theta_topomap.py
│   ├── grid_pathology_timeline.py
│   ├── grid_map_degradation.py
│   └── head_direction_ring_attractor.py
│
├── docs/
│   ├── notes_and_equations.md
│   └── navigation_cells_overview.pdf
│
└── README.md

```

---

## Code

- **[eeg_theta_topomap.py](./code/eeg_theta_topomap.py)**  
  EEG analysis producing theta-band power topographic maps for control and Alzheimer’s groups.

- **[grid_pathology_timeline.py](./code/grid_pathology_timeline.py)**  
  Continuous attractor model illustrating progressive Alzheimer’s pathology across disease stages.

- **[grid_map_degradation.py](./code/grid_map_degradation.py)**  
  Simulation of grid-cell spatial map breakdown under increasing neuron loss.

- **[head_direction_ring_attractor.py](./code/head_direction_ring_attractor.py)**  
  Ring attractor model of head-direction cells and heading representation dynamics.

---

## Documentation

- **[notes_and_equations.md](./docs/notes_and_equations.md)**  
  Detailed notes on head-direction, grid, and place cells, including equations and explanations of the computational models.

- **[navigation_cells_overview.pdf](./docs/navigation_cells_overview.pdf)**  
  Slide deck summarizing navigation cell systems, models, and simulation results.

---

## Overview of the Project

- **Goal:** Understand how neuron loss in key navigation circuits affects spatial representation and whether these changes are reflected in EEG signals.
- **Methods:**
  - Computational modeling of head-direction and grid-cell networks
  - Progressive neuron loss to simulate Alzheimer’s disease pathology
  - EEG analysis tracking changes in gamma-band activity across disease stages
- **Status:** This research is ongoing. Models, analyses, and interpretations are actively being developed and refined.

---

## How to Explore

1. Start with **[docs/notes_and_equations.md](./docs/notes_and_equations.md)** for background on navigation circuits and the mathematical models.
2. Review **[docs/navigation_cells_overview.pdf](./docs/navigation_cells_overview.pdf)** for a visual summary of the project.
3. Explore the scripts in **[code/](./code/)** to see how the models and EEG analyses are implemented.

---

## References

- Nobel Prize in Physiology or Medicine (2014) – Discovery of place and grid cells
- Ranck (1984) – Head-direction cells
- Moser & Moser (2005) – Grid cells
- O’Keefe (1971) – Place cells
- OpenNeuro EEG Dataset: https://openneuro.org/datasets/ds004504/versions/1.0.7
