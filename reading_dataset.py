import glob
import regex as re
import os
import wfdb

class data ():
    def __init__(self,folder=None,index=None,age=None, sex=None,Dx=None,Rx=None,Hx=None,Sx=None) :
        self.folder=folder
        self.index=index
        self.age=age
        self.sex=sex
        self.dx=Dx
        self.rx=Rx
        self.hx=Hx

def label2diagnosis(label):
    label_of_disease=['164861001', '426434006'  , '425419005' , '425623009','413844008' , '413444003' , '53741008', '266257000']
    
    list_of_coronary_disease=['myocardial ischemia', 'anterior ischemia', 'inferior ischaemia' ,
     'lateral ischaemia' , 'chronic myocardial ischemia' ,'acute myocardial ischemia' , 'coronary heart disease' ,
    'transient ischemic attack']

    st_elevation=164931005
    st_depresion=429622005
    left_ventricular_strain=370365005
    old_myocardial_infarction=164867002
    sinus_rhythm=426783006
    twave_inversion=59931005



    # for item in label_of_disease :
    #     if 

location='dataset\\6-PhysioNetChallenge2020_Training_E\\'

list_of_ecgs=[]
for item in glob.glob (f'{location}*.hea') :
    file_name=os.path.basename(item)
    ecg=data()
    ecg.folder=re.findall(r'^\D*',file_name)[0]
    ecg.index=re.findall(r'(\d*)\.',file_name)[0]
    with open (item, 'r') as file:
        lines=file.readlines()
        age_line=lines[13]
        ecg.age=re.findall(r'Age:\s(\d*)',age_line)[0]
        sex_line=lines[14]
        ecg.sex=re.findall(r'Sex:\s(.*)',sex_line)[0]
        dx_line=lines[15]
        ecg.dx=re.findall(r'\d+',dx_line)

    
        list_of_ecgs.append(ecg)
    # print(f'{ecg.age} , {ecg.sex}')

count=0
list_of_coronary_disease=['164861001', '426434006'  , '425419005' , '425623009','413844008' , '413444003' , '53741008', '266257000',
'164931005','429622005','370365005','164867002','426783006','59931005']


how_many=[0,0,0,0,0,0,0,0  ,0,0,0,0,0,0]

sinusiha=[]
for item in list_of_ecgs:
    for dx1 in item.dx:
        for dx2 in list_of_coronary_disease:
            if dx1==dx2:
                if dx1=='426783006':
                    sinusiha.append(item.index)
                index=list_of_coronary_disease.index(dx2)
                a=how_many[index]
                a+=1
                how_many[index]=a
print(how_many)                
 

