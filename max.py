import numpy as np
import matplotlib.pyplot as plt



x=np.random.rand(25)*2. -1.
y=1. + 1.5*np.sin(x)+np.random.rand(len(x)) * 1.


theta_0,theta_1=np.polyfit(x,y,deg=1)
newxline=np.array([-1.,1.])
newyline=theta_0+theta_1*newxline

plt.plot(x,y,'bx')
plt.plot(newxline,newyline,'r-')
plt.show()
