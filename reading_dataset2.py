import glob
import matplotlib
import regex as re
import os
import wfdb
import matplotlib.pyplot as plt
import scipy.io
import numpy as np

label_of_disease=['164861001', '426434006'  , '425419005' , '425623009','413844008' , '413444003' , '53741008', '266257000',
    '164931005','429622005','59931005','428750005','370365005','164867002','426783006']

class data ():
    def __init__(self,folder=None,index=None,age=None, sex=None,Dx=None,Rx=None,Hx=None,Sx=None,samples=None,sample_rate=None,duration=None) :
        self.folder=folder
        self.index=index
        self.age=age
        self.sex=sex
        self.dx=Dx
        self.rx=Rx
        self.hx=Hx
        self.samples=samples
        self.sample_rate=sample_rate
        self.duration=duration

    def find_duration(self):
        if self.samples != None:
            self.duration=self.samples /self.sample_rate
        return self.duration    
            


 

def label2diagnosis(label):
    label_of_disease=['164861001', '426434006'  , '425419005' , '425623009','413844008' , '413444003' , '53741008', '266257000',
    '164931005','429622005','59931005','164934002','164917005','428750005','370365005','164867002','164930006','164921003','164951009','164947007','111975006','284470004','164873001','426783006']
    
    list_of_disease=['myocardial_ischemia', 'anterior_ischemia', 'inferior_ischaemia' ,'lateral_ischaemia' 
    , 'chronic_myocardial_ischemia' ,'acute_myocardial_ischemia' , 'coronary_heart_disease' ,'transient_ischemic_attack'
    ,'st_elevation','st_depresion','twave_inversion','twave_abnormal','qwave_abnormal','nonspecific_st_t_abnormality' , 'left_ventricular_strain','old_myocardial_infarction','st_interval_abnormal','r_wave_abnormal','abnormal_QRS','prolonged_pr_interval','prolonged_qt_interval','premature_atrial_contraction','left_ventricular_hypertrophy','sinus_rhythm']

    if label in label_of_disease:
        diagnosis=list_of_disease[label_of_disease.index(label)]
    else:
        diagnosis=label
       
    return (diagnosis)    
    


def get_location(folder_number):
    folders=['1-Training_WFDB','2-Training_2','3-PhysioNetChallenge2020_Training_StPetersburg'
        ,'4-PhysioNetChallenge2020_Training_PTB','5- PhysioNetChallenge2020_Training_PTB-XL','6-PhysioNetChallenge2020_Training_E']
    location= 'dataset\\'+folders[folder_number]  +'\\'
    pishvands=['A','Q','I','S','HR','E']
    pishvand=pishvands[folder_number]
    zfilling_number= [5 if folder_number==5 or folder_number==4 else 4][0] 
    return location , pishvand , zfilling_number


def get_ecg(index,folder_number):
    location , pishvand , zfilling_number=get_location(folder_number)
    ecg_annotation_file=f'{location}{pishvand}{(str(index)).zfill(zfilling_number)}.hea'
    ecg_mat_file=f'{location}{pishvand}{(str(index)).zfill(zfilling_number)}.mat'
    return ecg_mat_file, ecg_annotation_file


def read_ecg(index,folder_number=5):
    ecg_annotation_file=get_ecg(index,folder_number)[1]
    ecg=data()
    ecg.index=index
    with open (ecg_annotation_file, 'r') as file:
        lines=file.readlines()
        first_line=lines[0]
        first_line=first_line.split(' ')
        ecg.sample_rate=float(first_line[2])
        ecg.samples=float(first_line[3])
        ecg.duration=(ecg.samples)/(ecg.sample_rate)
        age_line=lines[13]
        ecg.age=re.findall(r'Age:\s(\d*)',age_line)[0]
        sex_line=lines[14]
        ecg.sex=re.findall(r'Sex:\s(.*)',sex_line)[0]
        dx_line=lines[15]
        ecg.dx=re.findall(r'\d+',dx_line)
        ecg.duration=ecg.find_duration()

    return ecg

    




def plot_ecg (index,channels=None,folder_number=5):
    ecg_mat_file=get_ecg(index,folder_number)[0]
    ecg= read_ecg(index , folder_number)
    mat = scipy.io.loadmat(ecg_mat_file)
    mat=mat['val']
   
    subplot(channels,ecg,mat)
    
    plt.show()


def subplot (channels , ecg , mat):
    leads=['I','II','III','aVR','aVL','aVF','V1','V2','V3','V4','V5','V6']
    x=np.arange(ecg.samples, )/ecg.sample_rate
    if type(channels)!=list:
        plt.plot(x,mat [channels ,:]/1000)
        plt.ylabel(leads[channels])
    else:    
        if channels==None:
            channels=[i for i in range(12)]
        
        x=np.arange(ecg.samples, )/ecg.sample_rate
        num=len(channels)
        fig, ax = plt.subplots(num)
        for i in range (num):
            y=mat[channels[i],:]/1000
            ax[i].plot(x,y)
            ax[i].set_ylabel (leads[channels[i]])

# plot_ecg (15, folder_number=0 , channels=[4,5] )



def find_normals(folder_number):
    location=get_location(folder_number)[0]
    number_of_files=int (len([name for name in os.listdir(location) if os.path.isfile(os.path.join(location, name))])/2)
    count=0
    normal_numbers=[]
    for i in range (1,number_of_files+1):
        ecg=read_ecg(i , folder_number)
        if ecg.dx==['426783006']:
            normal_numbers.append(i)
    return normal_numbers        


def find_coronaries(folder_number):
    location=get_location(folder_number)[0]
    number_of_files=int (len([name for name in os.listdir(location) if os.path.isfile(os.path.join(location, name))])/2)
    coroneries=[]
    label_of_coronaries=['164861001', '426434006'  , '425419005' , '425623009','413844008' , '413444003' , '53741008', '266257000',]

    for i in range (1,number_of_files+1):
        ecg=read_ecg(i , folder_number)
        assert type(ecg.dx)==list
        if ecg.dx != None:
            for dx in ecg.dx :
                if dx in label_of_coronaries:
                    new= [label2diagnosis(x) for x in ecg.dx]
                    coroneries.append(new)
                    break
    return(coroneries)    
    
# print(find_normals(5))
print(find_coronaries(5))

