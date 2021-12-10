import numpy as np

def swirl_preset(rate_theta = 15/180*np.pi, rate_r = 3, steps = 50, offset = 150):
    thetas = np.linspace(0, steps*rate_theta, num=steps)
    rads = np.linspace(0, steps*rate_r, num=steps)
    x = (rads*np.cos(thetas) + offset).astype(np.uint8)
    y = (rads*np.sin(thetas) + offset).astype(np.uint8)
    size = max(np.max(x), np.max(y))
    return list(zip(x,y)), (size,size)

