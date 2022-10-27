#!/usr/bin/env python
# coding: utf-8



import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import scipy.io as sp
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sim_excluded_idx = [121, 128, 137]

data = sp.loadmat('dataset_battery_voltage/dataset1.mat')
columns=['time', 'courant', 'soc', 'temperature', 'voltage']

data_total_rc1 = pd.DataFrame(data['RC1Model'][0][0][0], columns=columns)
data_total_rc2 = pd.DataFrame(data['RC2Model'][0][0][0], columns=columns)

for sim in range(1, len(data['RC1Model'][0][0])):
    
    if sim in sim_excluded_idx:
        continue
        
    print("add sim :", sim)
    data_total_rc1 = data_total_rc1.append(pd.DataFrame(data['RC1Model'][0][0][sim], columns=columns))
    data_total_rc2 = data_total_rc2.append(pd.DataFrame(data['RC2Model'][0][0][sim], columns=columns))

data_total_rc1.reset_index(drop=True, inplace=True)
data_total_rc2.reset_index(drop=True, inplace=True)

print(data_total_rc1.shape)
print(data_total_rc2.shape)

data_total = data_total_rc1.join(data_total_rc2, lsuffix='_rc1', rsuffix='_rc2')
print(data_total.shape)

data_total['delta_volt_rc2_rc1'] = data_total['voltage_rc2'] - data_total['voltage_rc1']
data_total = data_total.drop(columns=['time_rc2', 'courant_rc2', 'soc_rc2'])

data_total.to_csv('./dataset_battery_voltage/subset_test.csv', index=False)




