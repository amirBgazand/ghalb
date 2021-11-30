import numpy as np
from matplotlib import pyplot as plt

sample_rate=500
b=np.arange(5000)
shape=b.shape[0]

c=(np.arange(shape )/sample_rate)
print(b[1])
mat=[]
for i in range (shape) :
    mating=[b[i],c[i]]
    mat.append(mating)
mat=np.array(mat)
print(mat)    

# d=np.vstack((b,c))
# print(d)

# e=np.reshape(d,(shape,2))
# print(e)
# print(e[1])




plt.show()





# print(b)
# print(c)

# 
# print(d)
# e=np.reshape(d,(2,10))
# f=d.reshape(2,10)
# print(e)
# print(e.shape)
# print(f)
# 