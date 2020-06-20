import cv2
import numpy as np
from matplotlib import pyplot as plt
plt.rcParams['figure.figsize'] = [10, 10]

"""Helper function to display images"""
def dispim(img, cmap='gray'):
    if cmap == 'gray':
        plt.imshow(img, cmap='gray')
    elif cmap == 'bin':
        plt.imshow(img, cmap='binary')
    else:
        plt.imshow(img)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

"""Function mapping image size to kernel size, mapping found emperically."""
def get_ksize(size):
    if size < 540:
        ksize = 5
    elif size < 720:
        ksize = 7
    elif size < 1080:
        ksize = 9
    else:
        ksize = 11
    return ksize

"""Automated Canny Detection"""
def detect(src, sigma=0.33):
    
    # 'src' is a single channel image
    m = np.median(src)
    
    # Getting the integer bounds automatically for double thresholding
    l = int(max(0  , (1.0-sigma)*m))
    u = int(min(255, (1.0+sigma)*m))
    
    noisy_dst = cv2.Canny(src, l, u)
    
    # 'Smoothening' the noisy image with gaussian blurring
    size = min(src.shape)
    k = get_ksize(size)
    dst = cv2.GaussianBlur(noisy_dst, (k, k), 0)
    return dst

def thresh(img, t=0.5, method='bin'):
    # Binary Thresholding:
    # c = (img > t).astype(int)
    # return c
    if method == 'agt':
        c = cv2.adaptiveThreshold(img, 1, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        return c
    elif method == 'bin':
        c = (img > t).astype(int)
        return c
    

# src = cv2.imread('square.png', 0)
# src = cv2.GaussianBlur(src, (5, 5), 0)

# dst = detect(src)
# dispim(src)
# dispim(dst)















