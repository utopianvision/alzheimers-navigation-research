import matplotlib.pyplot as plt
import numpy as np

tau = 2
r0 = 3
t_max = 200
h = 0.1
A_e = 1
A_i = 0.5
sigma_e = 1
sigma_i = 3
n = 256
dtheta = 2*np.pi/n
J0 = -5
J1 = 5
I0 = 1

theta = np.arange(0, 2*np.pi, dtheta) # angular position of each neuron (vector)
#print(theta)

t = np.arange(0, t_max + h, h)
r = np.zeros((len(t), n))

r[0, :] = r0
#r[0, int(n/2)] = r0+0.1
print(r)

def W(x): # connection strength between 2 neurons separated by angular dist x
    # A_e * np.exp(-x**2 / (2 * sigma_e**2)) - A_i * np.exp(-x**2 / (2 * sigma_i**2))
    return J0 + J1*np.cos(x)

def phi(x):
    return np.maximum(x,0)
    
W_mat = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        dist = np.abs(theta[i]-theta[j])
        if dist > np.pi:
            W_mat[i, j] = W(2*np.pi-dist)
        else:
            W_mat[i, j] = W(dist)

for i in range(1, len(t)): # loop over time
    total = W_mat @ r[i-1, :]
    integral = total * dtheta

    r[i, :] = (1 - h / tau) * r[i-1, :] + h/tau * phi(integral + I0)
    
plt.plot(np.arange(0, n, 1), r[0, :], label="Simulation")
plt.xlabel("n")
plt.ylabel("r(t_max, n)")
plt.legend()
plt.grid(True)
plt.show()
plt.plot(np.arange(0, n, 1), r[int(t_max/2), :], label="Simulation")
plt.xlabel("n")
plt.ylabel("r(t_max, n)")
plt.legend()
plt.grid(True)
plt.show()
plt.plot(np.arange(0, n, 1), r[t_max, :], label="Simulation")
plt.xlabel("n")
plt.ylabel("r(t_max, n)")
plt.legend()
plt.grid(True)
plt.show()