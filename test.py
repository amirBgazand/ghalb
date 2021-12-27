# import scipy.io
# import pandas as pd

# def get_location(folder_number):
#     folders=['1-Training_WFDB','2-Training_2','3-PhysioNetChallenge2020_Training_StPetersburg'
#         ,'4-PhysioNetChallenge2020_Training_PTB','5- PhysioNetChallenge2020_Training_PTB-XL','6-PhysioNetChallenge2020_Training_E']
#     location= 'dataset\\'+folders[folder_number]  +'\\'
#     pishvands=['A','Q','I','S','HR','E']
#     pishvand=pishvands[folder_number]
#     zfilling_number= [5 if folder_number==5 or folder_number==4 else 4][0] 
#     return location , pishvand , zfilling_number


# def get_ecg(index,folder_number):
#     location , pishvand , zfilling_number=get_location(folder_number)
#     ecg_annotation_file=f'{location}{pishvand}{(str(index)).zfill(zfilling_number)}.hea'
#     ecg_mat_file=f'{location}{pishvand}{(str(index)).zfill(zfilling_number)}.mat'
#     return ecg_mat_file, ecg_annotation_file


# mat = scipy.io.loadmat(get_ecg(1,5)[0])
# mat = {k:v for k, v in mat.items() if k[0] != '_'}
# data = pd.DataFrame({k: pd.Series(v[0]) for k, v in mat.items()}) # compatible for both python 2.x and python 3.x

# data.to_csv("example.csv")



a=[1,2,3,]

print(str(a))