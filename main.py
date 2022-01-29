from numpy.lib.type_check import real
from reading_dataset import *
import regex as re
import os
import matplotlib.pyplot as plt
import scipy.io
import numpy as np
import math
import pickle
from vcgFROMecg import ecg2vcg
label_of_coronaries=['164861001', '426434006'  , '425419005' , '425623009','413844008' , '413444003' , '53741008', '266257000',]

# create_file(find_plus_minus(label_of_coronaries,minus=['59931005','164934002']),'coronary with out t wave change')

# create_file(find_coronaries(5),'coronaries')

# create_file(find_plus_minus(['59931005','164934002'],minus=label_of_coronaries),'twave abnormal but not coronary')

# create_file(find_plus_minus(['59931005','164934002']),'twave abnormal')

# create_file(find_normals(),'normals')

plot_ecg(178   ,folder_number=5)


# ecg2vcg(3  , type='3d')