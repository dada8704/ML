import numpy as np
import os

from KMEANS import *
from scipy import linalg
import cv2


def Spectral(Gram, k, mode = 1):
    print("Spectral !!!")
    

    ## compute the first k eigenvectors

    saved_vectors_sort = "./T_vector_S_7_C_42_sort.npy"
    saved_values_sort = "./T_value_S_7_C_42_sort.npy"
    if not os.path.isfile(saved_vectors_sort):
        # degree matrix
        Degree = np.sum(Gram, axis=1)
        Laplacian = np.diag(Degree) - Gram
        D__1_2 = np.diag(Degree ** (-0.5))
        Laplacian_sym = D__1_2 @ Laplacian @ D__1_2

        print("no file")
        Eigen = linalg.eigh(Laplacian_sym)
        eigen_values_unsorted = Eigen[0]
        eigen_vectors_unsorted = Eigen[1]


        Eigen_index = np.argsort(eigen_values_unsorted)
        Eigen_Value = eigen_values_unsorted[Eigen_index]
        Eigen_Vector = eigen_vectors_unsorted[Eigen_index]
        np.save(saved_vectors_sort, Eigen_Vector)
        np.save(saved_values_sort, Eigen_Value)
    else:
        Eigen_Vector = np.load(saved_vectors_sort)
        Eigen_Value = np.load(saved_values_sort)
        print(Eigen_Value)
        print(Eigen_Vector.shape)


    ## normalize

    Eigen_Vector_trans = Eigen_Vector[:, 0:k]
    for iter_row in range(len(Eigen_Vector_trans)):
        SSum = np.sum(Eigen_Vector_trans[iter_row])
        Eigen_Vector_trans[iter_row] = Eigen_Vector_trans[iter_row] / SSum

    #GIF = Kmeans(Gram = Eigen_Vector_T, k = k)
    print(Eigen_Vector_trans[0])

    visualize(Eigen_Vector, k)

    Gram_spectral = Spectral_kernel(Eigen_Vector = Eigen_Vector_trans, Gamma = 0.001)
    GIF = Kmeans(Gram = Gram_spectral, k = k, mode = mode)

    return GIF


def Spectral_kernel(Eigen_Vector, Gamma):
    Dis_kernel = (- Gamma * pdist(Eigen_Vector, 'sqeuclidean'))
    Kernelone = np.exp(Dis_kernel)
    Kernel = squareform(Kernelone)

    return Kernel

def visualize(Eigen_Vector, k):
    ## norm eigenvector
    for i in range(k):
        vector = Eigen_Vector[i]
        pre_norm = vector - min(pre_norm)
        norm = pre_norm / max(pre_norm) * 255
        norm_size = norm.reshape(100, 100)
        for iter_i in range(100):
            for iter_j in range(100):
                cv2.imwrite("visual" + str(i), norm_size)





