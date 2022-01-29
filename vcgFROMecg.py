from numpy.lib.type_check import real
from reading_dataset import *
import regex as re
import os
import matplotlib.pyplot as plt
import scipy.io
import numpy as np
import math
import pickle 
from mpl_toolkits import mplot3d

def rotate(x,y,theta):
    rotation_matrix=np.array([[np.cos(theta),-np.sin(theta)],[np.sin(theta),np.cos(theta)]])
    newarray=np.empty((2,x.shape[0]))
    newarray[0,:]=x
    newarray[1,:]=y
    newarray=rotation_matrix.dot(newarray)
    x_new=newarray[0,:]
    y_new=newarray[1,:]
    return (x_new , y_new)

 

def sixty_leads2vcg(first_mat,second_mat,theta1,theta2):
    
    
    # nesbat=np.divide(first_mat, second_mat)
    nesbat=first_mat/second_mat
    theta=np.arctan((nesbat*np.cos(theta2)-np.cos(theta1))/ (np.sin(theta1)-nesbat*np.sin(theta2)))
    r=first_mat/np.cos(theta-theta1)
    x=r*np.cos(theta)
    y=r*np.sin(theta)
    
    return x, y
    

# f=np.array([1,2,3,4])
# s=np.array([1,1,1,1])

# print(sixty_leads2vcg(f,s,np.pi/6,-np.pi/6))

    
peaks=pickle.load (open('peaks.pkl' , 'rb'))



def threeD (x,y,z):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot3D(x, y, z, 'gray')


def ecg2vcg(index,peak_number=0,folder_number=5 , type='all' , denoise=True):
    ecg= read_ecg(index , folder_number , denoise=denoise)
    new=[label2diagnosis(x) for x in ecg.dx]
    ecg_peaks=peaks[index]
    my_peak=ecg_peaks[peak_number]
    next_peak=ecg_peaks[peak_number+2]
    
    time0=int(my_peak*ecg.sample_rate)
    time1=int(next_peak*ecg.sample_rate)
    duration=np.arange(ecg.samples, )/ecg.sample_rate
    duration=duration [time0:time1]
    mat_I=ecg.mat[0,time0:time1]
    mat_aVF=ecg.mat[5,time0:time1]

    mat_II = ecg.mat[1,time0:time1]
    mat_avl = ecg.mat[4,time0:time1]
    

    mat_aVR = ecg.mat[3,time0:time1]
    mat_III = ecg.mat[2,time0:time1]
    x1,y1=rotate(mat_II,mat_avl,-np.pi/3 )  
    x2,y2=rotate(mat_aVF,mat_I,-np.pi/2)
    x3,y3=rotate(mat_aVR,mat_III,5*np.pi/6)
    x4,y4=sixty_leads2vcg(mat_avl,-mat_aVR , np.pi/6,-np.pi/6)
    x5,y5= sixty_leads2vcg(mat_I,mat_II , 0,-np.pi/3)
    x6,y6=sixty_leads2vcg(mat_II,mat_III , -np.pi/3,-4*np.pi/6)
    X_average=(x1+x2+x3+x4+x5+x6)/6
    Y_average=(y1+y2+y3+y4+y5+y6) /6
    if type== 'all':
        plt.plot(x1,y1, label='II and avl')
        plt.plot(x2,y2 , label ='aVF and I')
        plt.plot (x3,y3 , label= 'aVR and III')
        plt.plot(x4,y4 , label= 'aVL,-aVR')
        plt.plot(x5,y5 , label= 'I,II')
        plt.plot(x6,y6 , label= 'II,III')

        plt.plot(X_average,Y_average  , label='average')

    if type == 'average':
        plt.plot(X_average,Y_average  , label='average')

    if type == '3d':
        threeD(X_average,Y_average,duration)

    plt.legend(loc="upper left")
    plt.suptitle(f'age:{ecg.age} , dx:{str(new)} ' , fontsize=10 )

    plt.show()





# plot_ecg(1)







