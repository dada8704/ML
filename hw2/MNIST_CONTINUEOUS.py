import sys
import math
import numpy as np
class MNIST_CONTINUEOUS():
    #def __init__(self, train_image_file, train_label_file, test_image_file, test_label_file):
    #    self.train_image_file = train_image_file
    #    self.train_label_file = train_label_file
    #    self.test_image_file = test_image_file
    #    self.test_label_file = test_label_file

    def __init__(self):
        self.Prior = np.zeros((10), dtype = float) ## Just count it!!
        self.Mean = np.zeros((10, 28 * 28), dtype = float)
        self.Var = np.zeros((10, 28 * 28), dtype = float)
        self.pre_Square = np.zeros((10, 28 * 28), dtype = float)
        self.trained = False

    def init_data(self, label_file, image_file):
        Label_fptr = open(label_file, "rb")
        Image_fptr = open(image_file, "rb")

        ## init label file
        Label_fptr.read(4) ## magic number
        Label_fptr.read(4) ## number of items

        ## init image file
        Image_fptr.read(4) ## magic number
        Image_fptr.read(4) ## number of images
        Image_fptr.read(4) ## number of rows
        Image_fptr.read(4) ## number of columns

        return Label_fptr, Image_fptr

    def get_label(self, fptr):
        label = int.from_bytes(fptr.read(1), byteorder = 'big')
        #print(label)
        return label

    def get_pixel(self, fptr):
        pixel = int.from_bytes(fptr.read(1), byteorder = 'big')
        return pixel

    def image_process(self, label, Image_fptr):
        #print("ll:", label)
        for iter_pixel in range(28 * 28):
            pixel = self.get_pixel(fptr = Image_fptr)
            #print(pixel)
            self.Mean[label][iter_pixel] = self.Mean[label][iter_pixel] + pixel
            self.pre_Square[label][iter_pixel] = self.pre_Square[label][iter_pixel] + (pixel * pixel)
        #print("nononono")
        #for i in range(len(self.pre_Square)):
        #    print("######", i, self.pre_Square[i])
        #print("square", self.pre_Square)


    def norm_probability(self, probability):
        total = 0.0
        #print(probability)
        for iter_i in range(len(probability)):
            total = total + probability[iter_i]
        #print(probability, "total", total)
        for iter_i in range(len(probability)):
            probability[iter_i] = float(float(probability[iter_i]) / float(total))
        #print(probability)
        return probability


    def TRAIN(self, train_label_file, train_image_file):
        Label_fptr, Image_fptr = self.init_data(label_file = train_label_file, image_file = train_image_file)
        train_case_num = 60000
        self.printProgress(0, 100, prefix="training:", suffix="Complete", barLength=50)
        for iter_label in range(train_case_num):
            label = self.get_label(fptr = Label_fptr)
            #print("LL", label)
            self.Prior[label] = self.Prior[label] + 1
            self.image_process(label = label, Image_fptr = Image_fptr)
            self.printProgress(int(iter_label/600), 100, prefix="training: ", suffix="Complete", barLength=50)
        

        for digit in range(10):
            print(self.Prior)
            for iter_pixel in range(28 * 28):
                #Mean = self.Mean[digit][iter_pixel]
                #pRe_Square = self.pre_Square[digit][iter_pixel]
                
                self.Mean[digit][iter_pixel] = \
                    float(self.Mean[digit][iter_pixel] / self.Prior[digit])
                
                self.pre_Square[digit][iter_pixel] = \
                    float(self.pre_Square[digit][iter_pixel] / self.Prior[digit])
                
                self.Var[digit][iter_pixel] = \
                    self.pre_Square[digit][iter_pixel] - (self.Mean[digit][iter_pixel] ** 2)

                if self.Var[digit][iter_pixel] == 0:
                    self.Var[digit][iter_pixel] = 0.05
                elif self.Var[digit][iter_pixel] < 0:
                    self.Var[digit][iter_pixel] = -(self.Var[digit][iter_pixel])
        
        #print("fuck", self.Prior / 60000)
        #print(self.Mean)
        #print(self.pre_Square)
        #self.Prior = self.Prior / 60000
        #print(self.Mean[0])
        self.Prior = self.norm_probability(self.Prior)
        print("norm_print(self.Prior)", self.Prior)
        self.trained = True
        return self.Mean, self.Var, self.Prior

    def Get_MVP(self):
        if(self.trained):
            return self.Mean, self.Var, self.Prior
        else:
            print("not train yet")
            return None, None, None

    def get_image(self, ptr):
        image = np.zeros((28 * 28), dtype = float)
        for iter_pixel in range(28 * 28):
            image[iter_pixel] = self.get_pixel(fptr = ptr)
        return image


    def cal_probability(self, test_image):
        predict_probability = np.zeros((10), dtype = float)
        for digit in range(10):
            predict_probability[digit] = np.log(self.Prior[digit])
            #print(self.Prior[digit])
            for iter_pixel in range(28 * 28):
                tmp1 = np.log(float(1.0 / math.sqrt(2.0 * math.pi * self.Var[digit][iter_pixel])))
                tmp2 = float(((test_image[iter_pixel] - self.Mean[digit][iter_pixel]) ** 2) / (2 * self.Var[digit][iter_pixel]))
                predict_probability[digit] = predict_probability[digit] + tmp1 - tmp2
                #print("tmp1", tmp1)
                #print("tmp2", tmp2)
        return predict_probability





    def Test(self, test_label_file, test_image_file):
        Label_fptr, Image_fptr = self.init_data(label_file = test_label_file, image_file = test_image_file)
        Error = 0
        test_case_num = 10000
        for test_case in range(test_case_num):
            test_label = self.get_label(fptr = Label_fptr)
            #predict_probability = np.zeros((10), dtype = float)
            test_image = self.get_image(ptr = Image_fptr)
            prepre = self.cal_probability(test_image = test_image)

            #print("before: ", prepre)

            predict_probability = self.norm_probability(prepre)
            
            #print("after:", predict_probability)

            prediction = np.argmin(predict_probability)
            print("Prediction: ", prediction, ", Ans: ", test_label)
            if prediction != test_label:
                Error = Error + 1
            print("Posterior (in log scale):")
            for j in range(10):
                print(j, ": ", predict_probability[j])
            print("Error rate: ", float(Error / (test_case + 1)))



    def printProgress(self, iteration, total, prefix='', suffix='', decimals=1, barLength=100):
        formatStr = "{0:." + str(decimals) + "f}"
        percent = formatStr.format(100 * (iteration / float(total)))
        filledLength = int(round(barLength * iteration / float(total)))
        bar = '#' * filledLength + '-' * (barLength - filledLength)
        sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)),
        if iteration == total:
            sys.stdout.write('\n')
        sys.stdout.flush()




    def Print_digit(self, label):
        print("label", label)
        for pixel_y in range(28):
            for pixel_x in range(28):
                print(int(self.Mean[label][28 * pixel_y + pixel_x] > 128), " ", end = "")
            print("")
        print("\n\n\n")









