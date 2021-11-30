from types import WrapperDescriptorType
import wfdb
import matplotlib.pyplot as plt
data_path='dataset\\1-Training_WFDB\\'
record = wfdb.rdrecord(f'{data_path}A0015', )

annotation = wfdb.rdann(f'{data_path}A0015','mat',sampto=1000)

# print(annotation)
# print(dir(annotation))


import scipy.io
mat = scipy.io.loadmat(f'{data_path}A0015.mat')
# print(mat['val'].shape)
# print(mat['val'][1,:])
# plt.plot(mat['val'][0,:])

# plt.show()

wfdb.plot_wfdb(record=record, annotation=annotation, plot_sym=True,
                   time_units='seconds', title='MIT-BIH Record 100',
                   figsize=(10,4), ecg_grids='all')
