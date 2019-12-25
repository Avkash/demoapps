
OPERATOR_LIST = {
    "+": "PLUS", 
    "-": "MINUS", 
    "*": "TIMES", 
    "/": "DIVISION"
}

IMAGE_LIST = {
    "Color image of the astronaut Eileen Collins." : "ASTRONAUT",
    "Checker Board": "CHECKER",
    "Greek coins from Pompeii": "COINS",
    "Hubble eXtreme Deep Field": "HUBBLE",
    "Horse" : "HORSE",
    "Camera" : "CAMERA",
    "Coffee Cup": "COFFEE"
}


IMGPROC_TYPES = {
    "Color(RGB) to Grayscale transformation" : "GRAYSCALE",
    "Color(RGB) to HSV(Hue,Saturation,Value) transformation" : "RGB2HSV",
    ##"Color(RGB) to HSL(Hue,Saturation,Lightness) transformation" : "RGB2HSL",
    "Resize Image" : "RESIZE", 
    "Image Rotation (Select Angle)" : "ROTATION", 
    "Flipping Image (Horizontal and Vertical)" : "FLIP", 
    "Alter Image Brightness" : "BRIGHTNESS", 
    "Image Filter (Median, Gaussian, Restoration & Sobel)" : "FILTER", 
    "Image Segmentation" : "SEGMENTATION"
}

FLIP_CHOICE = {
    "Original Image" : "ORIG",
    "Flip Horizontal" : "FLIP_LR",
    "Flip Vertical" : "FLIP_VR"
}

FILTER_CHOICE = {
    "Median Fliter" : "MEDIAN",
    "Gaussian Filter" : "GAUSSIAN",
    "Restoration Filter" : "RESTORATION",
    ##"Sobel_h Filter" : "SOBEL_H",
    ##"Sobel_v Filter" : "SOBEL_V",
    "Sobel Filter" : "SOBEL"
}