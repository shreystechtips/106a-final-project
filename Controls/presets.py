import numpy as np

def swirl_preset(rate_theta = 15/180*np.pi, rate_r = 3, steps = 50, offset = 0):
    thetas = np.linspace(0, steps*rate_theta, num=steps)
    rads = np.linspace(0, steps*rate_r, num=steps)
    x = (rads*np.cos(thetas) + offset).astype(int)
    y = (rads*np.sin(thetas) + offset).astype(int)
    size = 2*max(np.max(np.abs(x)), np.max(np.abs(y)))
    return list(zip(x,y)), (size,size)

def cardiod_preset(a = 20, steps = 50, offset = 0):
    cos = np.cos(np.linspace(0, 2*np.pi, num=steps))
    sin = np.sin(np.linspace(0, 2*np.pi, num=steps))
    x = (a*cos*(1-cos)) 
    y = (a*sin*(1-cos))
    off = min(np.min(x), np.min(y))
    x -= off
    y -= off
    size = 2*max(np.max(np.abs(x)), np.max(np.abs(y)))
    import matplotlib.pyplot as plt
    plt.plot(x,y)
    plt.show()
    return list(zip(x,y)), (size,size)

def lisajous_preset(offset = 0, steps = 200):
    x = 4*np.sin( 3/4 *np.linspace(0, 8*np.pi, num=steps)) 
    y = 3*np.sin(np.linspace(0, 8*np.pi, num=steps)) 
    off = min(np.min(x), np.min(y))
    x = x - off
    y = y - off
    size = max(np.max(x), np.max(y)) 
    import matplotlib.pyplot as plt
    plt.plot(x,y)
    plt.show()
    return list(zip(x,y)), (size, size)
    
SCALE_SIZE = 300
def transform(point, old_dim, new_dim = SCALE_SIZE):
    scale = new_dim/old_dim
    old_dim = np.array(old_dim)
    new_dim = np.array(new_dim)
    point = np.array(point) 
    temp =  scale*(point - old_dim/2) + new_dim/2
    temp[0] = -temp[0] + new_dim
    return temp
