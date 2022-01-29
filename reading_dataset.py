import regex as re
import os
import matplotlib.pyplot as plt
import scipy.io
import numpy as np
from denoising_function import denoising_data

label_of_disease=['164861001', '426434006'  , '425419005' , '425623009','413844008' , '413444003' , '53741008', '266257000',
    '164931005','429622005','59931005','428750005','370365005','164867002','426783006']

class data ():
    def __init__(self,folder=None,index=None,age=None, sex=None,Dx=None,Rx=None,Hx=None,Sx=None,samples=None,sample_rate=None,duration=None, mat=None) :
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
        self.mat=mat

    def find_duration(self):
        if self.samples != None:
            self.duration=self.samples /self.sample_rate
        return self.duration    
            


 

def label2diagnosis(label):
    label_of_disease=['164861001', '426434006'  , '425419005' , '425623009','413844008' , '413444003' , '53741008', '266257000',
    '164931005','429622005','59931005','164934002','164917005','428750005','370365005','164867002','164930006','164921003'
    ,'164951009','164947007','111975006','284470004','164873001','426783006']
    
    list_of_disease=['myocardial_ischemia', 'anterior_ischemia', 'inferior_ischaemia' ,'lateral_ischaemia' 
    , 'chronic_myocardial_ischemia' ,'acute_myocardial_ischemia' , 'coronary_heart_disease' ,'transient_ischemic_attack'
    ,'st_elevation','st_depresion','twave_inversion','twave_abnormal','qwave_abnormal','nonspecific_st_t_abnormality' 
    , 'left_ventricular_strain','old_myocardial_infarction','st_interval_abnormal','r_wave_abnormal','abnormal_QRS'
    ,'prolonged_pr_interval','prolonged_qt_interval','premature_atrial_contraction','left_ventricular_hypertrophy','sinus_rhythm']

    if label in list_of_disease:
        diagnosis=label_of_disease[list_of_disease.index(label)]
    elif label in label_of_disease:
        diagnosis=list_of_disease[label_of_disease.index(label)]
    else:
        diagnosis=label
       
    return (diagnosis)    
    
def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

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


def read_ecg(index,folder_number=5 , denoise=False):
    ecg_mat_file,ecg_annotation_file=get_ecg(index,folder_number)
    mat = scipy.io.loadmat(ecg_mat_file)
    np.seterr(invalid='ignore')


    mat=mat['val']
    if denoise == True:
        mat = denoising_data(mat)
    ecg=data()
    ecg.index=index
    ecg.mat=mat

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

    
def plot_ecg_form(ecg , mat,time, form):
    dx=ecg.dx
    new=[label2diagnosis(x) for x in ecg.dx]
    x=np.arange(ecg.samples, )/ecg.sample_rate
    y=mat/1000
    y_of_time=y[:,int(time[0]*ecg.sample_rate):int(time[1]*ecg.sample_rate)]
    maxy=y_of_time.max()
    miny=y_of_time.min()
    fig, ax = plt.subplots(6,2)
    if form == 'normal':
        leads=['I','II','III','aVR','aVL','aVF','V1','V2','V3','V4','V5','V6']
    else:         
        y_new=np.empty((12,int(ecg.samples)))
        y_new[0,:]=mat[4,:]
        y_new[1,:]=mat[0,:]
        y_new[2,:]=-mat[3,:]
        y_new[3,:]=mat[1,:]
        y_new[4,:]=mat[5,:]
        y_new[5,:]=mat[2,:]
        y_new[6:12,:]=mat[6:12,:]
        leads =['aVL','I','-aVR','II','aVF','III','V1','V2','V3','V4','V5','V6']
        mat=y_new

    for i in range (6):
        for j in range (2):
            y=mat[i+6*j,:]/1000
            ax[i,j].plot(x,y)
            ax[i,j].set_ylabel (leads[i+6*j])
            
            tool=ecg.duration
            small_vertical=np.arange(0,tool ,0.04)  
            big_vertical=np.arange(0,tool,0.2)

            [ax[i,j].axvline(x=k, linestyle='--',linewidth=0.2 ) for k in small_vertical]
            [ax[i,j].axvline(x=k, linestyle='--',linewidth=0.5 ) for k in big_vertical]

            small_horizontal=np.arange(-3,+3 ,0.1) 
            big_horizontal=np.arange(-3,+3,0.5)
            [ax[i,j].axhline(y=k, linestyle='--',linewidth=0.2 ) for k in small_horizontal]
            [ax[i,j].axhline(y=k, linestyle='--',linewidth=0.5 ) for k in big_horizontal]
            ax[i,j].axis([time[0], time[1],miny,maxy])
    
    fig.suptitle(f'age:{ecg.age} , dx:{str(new)} ' , fontsize=10 )        
    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.97, top=0.95, wspace=.12, hspace=0.22)        



def plot_ecg (index,time=None,channels=None,folder_number=5 , form='better'):
    ecg= read_ecg(index , folder_number)
    mat=ecg.mat

    
    if time != None:
        assert type(time)==tuple  
    else:
        if ecg.samples != None :
            time=(0,ecg.samples/ecg.sample_rate)  
    if channels != None:
        subplot(channels,ecg,mat)
    else:
        plot_ecg_form(ecg,mat,time ,form)
        
    plt.show()


def subplot (channels , ecg , mat ):
    leads=['I','II','III','aVR','aVL','aVF','V1','V2','V3','V4','V5','V6']
    x=np.arange(ecg.samples, )/ecg.sample_rate
    new=[label2diagnosis(x) for x in ecg.dx]
    
    if type(channels)!=list and channels!=None :
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
            maxy=y.max()
            miny=y.min()
            tool=ecg.duration
            small_vertical=np.arange(0,tool ,0.04)  
            big_vertical=np.arange(0,tool,0.2)

            [ax[i].axvline(x=j, linestyle='--',linewidth=0.1 ) for j in small_vertical]
            [ax[i].axvline(x=j, linestyle='--',linewidth=0.5 ) for j in big_vertical]

            small_horizontal=np.arange(miny,maxy ,0.1) 
            big_horizontal=np.arange(miny,maxy,0.5)
            [ax[i].axhline(y=j, linestyle='--',linewidth=0.1 ) for j in small_horizontal]
            [ax[i].axhline(y=j, linestyle='--',linewidth=0.5 ) for j in big_horizontal]
            ax[i].plot(x,y)
            ax[i].set_ylabel (leads[channels[i]])
            plt.subplots_adjust(left=0.07, bottom=0.02, right=0.98, top=0.98, wspace=0, hspace=0)
            
        fig.suptitle(f'age:{ecg.age} , dx:{str(new)} ' , fontsize=10 )

# plot_ecg (13,(0,6) )










def find_normals(folder_number=5):
    location=get_location(folder_number)[0]
    number_of_files=int (len([name for name in os.listdir(location) if os.path.isfile(os.path.join(location, name))])/2)
    count=0
    normal_numbers=[]
    for i in range (1,number_of_files+1):
        ecg=read_ecg(i , folder_number)
        if ecg.dx==['426783006']:
            normal_numbers.append(i)
            count+=1
    return normal_numbers    , count    


def find_coronaries(folder_number):
    location=get_location(folder_number)[0]
    number_of_files=int (len([name for name in os.listdir(location) if os.path.isfile(os.path.join(location, name))])/2)
    coroneries=[]
    coronery_ids=[]
    label_of_coronaries=['164861001', '426434006'  , '425419005' , '425623009','413844008' , '413444003' , '53741008', '266257000',]
    for i in range (1,number_of_files+1):
        try :
            ecg=read_ecg(i , folder_number)
            assert type(ecg.dx)==list
            
            if ecg.dx != None:
                for dx in ecg.dx :
                    if dx in label_of_coronaries:
                        coronery_ids.append(ecg.index)
                        new= [label2diagnosis(x) for x in ecg.dx]
                        new.insert(0,ecg.index)
                        coroneries.append(new)
                        break
        except:
            pass            
    return coronery_ids   , coroneries
    

def find_plus_minus(yekish_bashe , minus=[],  hamash_bashe=None ,folder_number=5):
    location=get_location(folder_number)[0]
    number_of_files=int (len([name for name in os.listdir(location) if os.path.isfile(os.path.join(location, name))])/2)
    count=0
    list_of_ids=[]


    list_of_dxs=[]
    for i in range (1,number_of_files+1):
        ecg=read_ecg(i , folder_number)


        if len(intersection(yekish_bashe,ecg.dx))!=0 and len(intersection(minus,ecg.dx))==0:
            if ecg.dx!=None:
                count+=1
                list_of_ids.append(ecg.index)
                
                new= [label2diagnosis(x) for x in ecg.dx]
                new.insert(0,ecg.index)
                list_of_dxs.append(new)
    return list_of_ids,list_of_dxs        , count    



def create_file(list_that_you_want,name_of_file,folder_number=5, ):

    loc='seperated ecgs\\'
    leng=len(list_that_you_want[0])
    with open (f'{loc}file{folder_number} {name_of_file}.txt' , 'w') as f:
        f.write(str(leng))
        for item in list_that_you_want:
            f.write(str(item))


# f_ischemia(5)
# plot_ecg(146 , (0,6),folder_number=4)
# plot_ecg(145  ,folder_number=5)




# def read_dat_file():
#     location='\\data\\staff-iii-database-1.0.0\\data'

#     sed = np.loadtxt(f'{location} ', unpack = True)

