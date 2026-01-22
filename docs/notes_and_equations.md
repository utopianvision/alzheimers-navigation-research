# Brain Navigation Cells: Notes and Equations

## Head Direction (HD) Cells
*   **Function:** Fire when an animal’s head points in a specific direction — act like the brain’s internal compass.
*   **Location:** Located mainly in the postsubiculum, also in anterior thalamus and related areas.
*   **Discovery:** James Ranck (1984) in rat postsubiculum.
*   **Role:** Provide directional input to navigation circuits — the “north arrow” for the brain’s GPS.

## Grid Cells
*   **Function:** Fire at multiple locations arranged in a hexagonal grid pattern.
*   **Location:** Found in the medial entorhinal cortex (MEC).
*   **Discovery:** May-Britt and Edvard Moser (2005).
*   **Role:** Provide a coordinate system for path integration and precise spatial mapping.

## Place Cells
*   **Function:** Fire when the animal is in one specific location (“place field”).
*   **Location:** Found in the hippocampus (CA1, CA3).
*   **Discovery:** John O’Keefe (1971).
*   **Role:** Encode current position in an environment, essential for cognitive maps.

---

## Ring Attractor Model (Head Direction Cells)

A **ring attractor** models HD cells mathematically: neurons arranged in a circle, each tuned to a facing direction ($0^\circ$–$360^\circ$). At any moment, a “bump” of activity represents current heading.

**Basic rate equation:**

$$\tau \frac{\partial r(\theta,t)}{\partial t} = -r(\theta,t) + f\left[ \int_{0}^{2\pi} W(\theta - \theta') \, r(\theta',t) \, d\theta' + I(\theta,t) \right]$$

**Where:**
*   $r(\theta,t)$: Firing rate of neuron tuned to direction $\theta$
*   $f(\cdot)$: Static nonlinearity (ReLU or sigmoid)
*   $W(\theta-\theta')$: Circular “Mexican-hat” connectivity stabilizing the activity bump
*   $I(\theta,t)$: External input (sensory cues)
*   $\tau$: Neuron response time constant

**Including head-rotation velocity $\omega(t)$:**

$$\tau \frac{\partial r(\theta,t)}{\partial t} = -r(\theta,t) + f\left[ \int_{0}^{2\pi} W(\theta - \theta') r(\theta',t) d\theta' + I(\theta,t) \right] + \alpha \, \omega(t) \frac{\partial r(\theta,t)}{\partial \theta}$$

This equation describes how activity bumps move as the head rotates, where $\alpha$ is a gain factor.
