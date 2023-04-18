from math import log10, sqrt
import cv2
import numpy as np



def PSNR(original, compressed):
    
    mse = np.mean((original - compressed) ** 2)
    
    if mse == 0:
        return 100

    max_pixel = 255.0

    psnr = 20 * log10(max_pixel / sqrt(mse))
    return psnr

def PSNR_from_path(path1, path2):

    original = cv2.imread(path1)
    sobel = cv2.imread(path2)
    value = PSNR(original, sobel)
    print(f"PSNR value is {value} dB")
    return value

if __name__ == "__main__":

    original = cv2.imread("images/leisure/leisure-sobel_loa-k0.png")
    sobel = cv2.imread("images/leisure/leisure-sobel_loa-k7.png")
    value = PSNR(original, sobel)
    print(f"PSNR value is {value} dB")