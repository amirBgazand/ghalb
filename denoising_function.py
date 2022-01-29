import numpy as np
import pywt
import bwr


def denoising_data(a_person_data) :

    number_of_leads=a_person_data.shape[0]
    number_of_steps=a_person_data.shape[1]

    denoised_baseline_data=np.zeros((number_of_leads,number_of_steps))

    for i in range(number_of_leads) :
        noisy_data=[]
        counter=0

        # step1-removing powerline interface for each lead
        for j in range(number_of_steps) :
            noisy_data.append(a_person_data[i,j])
            if a_person_data[i,j]==0 :
                counter=counter+1
        
        if counter==len(noisy_data) :
            for j in range(number_of_steps) :
                denoised_baseline_data[i,j]=noisy_data[j]
            continue

        w=pywt.Wavelet('sym4')
        maxlev = pywt.dwt_max_level(len(noisy_data), w.dec_len)
        threshold = 0.04
        coeffs = pywt.wavedec(noisy_data, 'sym4', level=maxlev)

        for coeff_num in range(1, len(coeffs)):
            coeffs[coeff_num] = pywt.threshold(coeffs[coeff_num], threshold*max(coeffs[coeff_num]))

        datarec = pywt.waverec(coeffs, 'sym4')


        # step2-removing baseline wander for each lead
        base_line=bwr.calc_baseline(datarec)
        ecg_out=datarec-base_line

        # making n*steps matrix
        for j in range(number_of_steps) :
            denoised_baseline_data[i,j]=ecg_out[j]


    return denoised_baseline_data




