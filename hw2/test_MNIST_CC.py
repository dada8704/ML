from MNIST_CONTINUEOUS import MNIST_CONTINUEOUS
#from decimal import *
#print(getcontext())
#Context(prec=28, rounding=ROUND_HALF_EVEN, Emin=-999999, Emax=999999, capitals=1, clamp=0, flags=[], traps=[InvalidOperation, DivisionByZero, Overflow])
import os


MNIST_CC = MNIST_CONTINUEOUS()

MNIST_CC.TRAIN("train-labels-idx1-ubyte", "train-images-idx3-ubyte")
M, V, P = MNIST_CC.Get_MVP()
#print(P[3])



#with open("M.txt", 'w') as outfile:
#	for iter_i in range(len(M)):
#		for iter_j in range(M[iter_i]):
#			outfile.write(str("%.8f" % M[iter_i][iter_j]))	#outfile.write(str(M))
#with open("V.txt", 'w') as outfile:
#	for iter_i in range(len(V)):
#		outfile.write(str("%.8f" % V[iter_i]))
#with open("P.txt", 'w') as outfile:
#	for iter_i in range(len(P)):
#		outfile.write(str("%.8f" % P[iter_i]) + " ")




#fm = open("M.txt", "r")
#fv = open("V.txt", "r")
#fp = open("P.txt", "r")

#M = fm.readlines()
#V = fv.readlines()
#P = fp.readlines()

#MNIST_CC.TTTTTTest(M = M, V = V, P = P, test_label_file = "t10k-labels-idx1-ubyte", test_image_file = "t10k-images-idx3-ubyte")

MNIST_CC.Test(test_label_file = "t10k-labels-idx1-ubyte", test_image_file = "t10k-images-idx3-ubyte")

for label in range(10):
    MNIST_CC.Print_digit(label = label)
