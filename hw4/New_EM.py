import numpy as np
from UTIL import *
import copy
from numba import jit





@jit
def E_step(Binomial_matrix, input_N, lamBda, probability, hidden_W):
    for iter_image in range(input_N):
        for iter_digit in range(10):
            hidden_W[iter_image][iter_digit] = lamBda[iter_digit]
    for iter_image in range(input_N):
        for iter_pixel in range(28 * 28):
            for iter_digit in range(10):
            
                if Binomial_matrix[iter_image][iter_pixel] == 1:
                    hidden_W[iter_image][iter_digit] *= probability[iter_pixel][iter_digit]
                else:
                    hidden_W[iter_image][iter_digit] *= (1 - probability[iter_pixel][iter_digit])
                ## deal with underflow
            if iter_pixel % 10 == 0:
                hidden_W[iter_image] /= hidden_W[iter_image].sum()
                #hidden_W[iter_image][iter_digit] *= jimmy
        hidden_W[iter_image] /= hidden_W[iter_image].sum()
        
    hidden_W[hidden_W<0.001] = 0.001


@jit
def M_step(Binomial_matrix, lamBda, hidden_W, probability, input_N):
    for iter_digit in range(10):
        lamBda[iter_digit] = 0.0
        for iter_image in range(input_N):
            lamBda[iter_digit] += hidden_W[iter_image][iter_digit]
    for iter_digit in range(10):
        for iter_pixel in range(28 * 28):
            probability[iter_pixel][iter_digit] = 0.0
    
    for iter_pixel in range(28 * 28):
        for  iter_digit in range(10):
            for iter_image in range(input_N):
                if Binomial_matrix[iter_image][iter_pixel] == 1:
                    probability[iter_pixel][iter_digit] += (hidden_W[iter_image][iter_digit])
                    #print(hidden_W[iter_image][iter_digit], probability[iter_pixel][iter_digi
                        
            
            probability[iter_pixel][iter_digit] /= lamBda[iter_digit]
    
    lamBda /= lamBda.sum()


#@jit
#def Test(Binomial_matrix, Label_fptr, label, probability):
#    GroundTruth = np.zeros((10, 10))
#    items = np.zeros(10)
#    for iter_label in range(60000):
#        label_now = get_label(Label_fptr)
#        xxx = int(items[label_now])
#        label[label_now][xxx] = iter_label
#        items[label_now] = items[label_now] + 1
#
#    for iter_digits in range(10):
#        for iter_item in range(int(items[iter_digits])):
#            ans = np.ones(10)
#            for iter_pixel in range(28 * 28):
#                for iter_digit in range(10):
#                
#                    if Binomial_matrix[int(label[iter_digit][iter_item])][iter_pixel] == 1:
#                        ans[iter_digit] *= probability[iter_pixel][iter_digit]
#                    else:
#                        ans[iter_digit] *= (1 - probability[iter_pixel][iter_digit])
#                    ## deal with underflow
#                if iter_pixel % 10 == 0:
#                    ans /= ans.sum()
#                    #hidden_W[iter_image][iter_digit] *= jimmy
#            ans /= ans.sum()
#            GroundTruth[iter_digits][ans.argmax()] += 1
#    return GroundTruth


def print_P(probability):
    for i in range(10):
        print("\nclass ", i, ":")
        for iter_y in range(28):
            for iter_x in range(28):
                if probability[iter_x + iter_y * 28][i] < 0.4:
                    print("0", end = "")
                else:
                    print("1", end = "")
            print()
        print("\n\n")



def Cal_from_W(hidden_W, Label_fptr, input_N):
    gt = np.zeros((10, 10))
    for iter_image in range(input_N):
        label_now = get_label(Label_fptr)
        ans = hidden_W[iter_image].argmax()
        gt[label_now][ans] += 1
    return gt


#@jit
#def Cal_w(Binomial_matrix, image_th, probability):
#    ans = np.ones(10)
#    for iter_pixel in range(28 * 28):
#        for iter_digit in range(10):
#        
#            if Binomial_matrix[image_th][iter_pixel] == 1:
#                ans[iter_digit] *= probability[iter_pixel][iter_digit]
#            else:
#                ans[iter_digit] *= (1 - probability[iter_pixel][iter_digit])
#            ## deal with underflow
#        if iter_pixel % 10 == 0:
#            ans = norm_probability(ans)
#            #hidden_W[iter_image][iter_digit] *= jimmy
#    ans = norm_probability(ans)
#    return ans
#
#@jit
#def Get_label_100(Label_fptr, label):
#    items = np.zeros(10)
#    for iter_label in range(60000):
#        label_now = get_label(Label_fptr)
#        xxx = int(items[label_now])
#        label[label_now][xxx] = iter_label
#        items[label_now] = items[label_now] + 1
#
#            #print(label[iter_digit][iter_item], end = " ")
#        #print("--------  ", iter_digit, "\n")
#    #print("items", items)
#    return items


