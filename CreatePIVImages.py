#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 10:08:20 2022

@author: php
"""

import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
<<<<<<< HEAD
from PIL import Image, ImageDraw, ImageFilter
=======
from PIL import Image, ImageDraw
>>>>>>> c6f180c2c5362ad822b4a450df550a52a9678eed
import random
import os

image_size=256 #pix, image will be square
image_number=10
particle_number=200
particle_size=5# pix, radius

<<<<<<< HEAD
gaussian_blur_radius=2 # pix
image_type="L" #"RGB", "L" for 8bits

=======
>>>>>>> c6f180c2c5362ad822b4a450df550a52a9678eed
option='extension'#'random', 'drift', 'contraction', 'extention'

# TO DO : add blur and 8bits conversion

drift_step=25 #pix/image
displacement_step=2 #pix/image
cell_size=50 #radius, pix

<<<<<<< HEAD
output_folder='/home/php/Bureau/test/extension-blur15-8bits/'
=======
output_folder='/home/php/Bureau/test/extension/'
>>>>>>> c6f180c2c5362ad822b4a450df550a52a9678eed

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def generate_coordinates(pnumber, psize, imsize):
    rd=[]
    i=0
    while i  < pnumber:
        rd.append(int((imsize)*random.random())) # avoid borders ?
        i=i+1
    return rd

def is_in_zone(xmin, ymin, xmax, ymax, X, Y):
    if ( X>xmin and X< xmax and Y>ymin and Y<ymax):
        output=True
    else:
        output=False
    return output

rdx=generate_coordinates(particle_number, particle_size,image_size)
rdy=generate_coordinates(particle_number, particle_size,image_size)

if option == 'random':
    k=0
    while k < image_number:
<<<<<<< HEAD
        img=Image.new(image_type, (image_size, image_size))
=======
        img=Image.new('RGB', (image_size, image_size))
>>>>>>> c6f180c2c5362ad822b4a450df550a52a9678eed
        draw=ImageDraw.Draw(img)
        rdx=generate_coordinates(particle_number, particle_size,image_size)
        rdy=generate_coordinates(particle_number, particle_size,image_size)
        j=0
        while j < particle_number:
            shape=[ (rdx[j], rdy[j]), (rdx[j]+particle_size, rdy[j]+particle_size)]
            draw.ellipse(shape, fill="white", outline="white")
            j=j+1
<<<<<<< HEAD
        blur=img.filter(ImageFilter.GaussianBlur(radius=gaussian_blur_radius))
        blur.save(output_folder+'image'+str(k)+'.tiff')
=======
        img.save(output_folder+'image'+str(k)+'.tiff')
>>>>>>> c6f180c2c5362ad822b4a450df550a52a9678eed
        k=k+1
        
elif option == 'drift':
    rdx=generate_coordinates(particle_number, particle_size,image_size)
    rdy=generate_coordinates(particle_number, particle_size,image_size)
    k=0
    while k < image_number:
<<<<<<< HEAD
        img=Image.new(image_type, (image_size, image_size))
=======
        img=Image.new('RGB', (image_size, image_size))
>>>>>>> c6f180c2c5362ad822b4a450df550a52a9678eed
        draw=ImageDraw.Draw(img)
        j=0
        while j < particle_number:
            shape=[ (rdx[j]+k*drift_step, rdy[j]+k*drift_step), (rdx[j]+k*drift_step+particle_size, rdy[j]+k*drift_step+particle_size)]
            draw.ellipse(shape, fill="white", outline="white")
            j=j+1
<<<<<<< HEAD
        blur=img.filter(ImageFilter.GaussianBlur(radius=gaussian_blur_radius))
        blur.save(output_folder+'image'+str(k)+'.tiff')
=======
        img.save(output_folder+'image'+str(k)+'.tiff')
>>>>>>> c6f180c2c5362ad822b4a450df550a52a9678eed
        k=k+1
        
elif option == 'contraction' or 'extention':
    rdx=generate_coordinates(particle_number, particle_size,image_size)
    rdy=generate_coordinates(particle_number, particle_size,image_size)
    
    Xmin=Ymin=(image_size/2)-cell_size
    Xcenter=Ycenter=(image_size/2)
    Xmax=Ymax=(image_size/2)+cell_size
    
    if option=='extension': 
        contraction_step=-displacement_step
    elif option == 'contraction':
        contraction_step=displacement_step
    
    k=0
    while k < image_number:
<<<<<<< HEAD
        img=Image.new(image_type, (image_size, image_size))
=======
        img=Image.new('RGB', (image_size, image_size))
>>>>>>> c6f180c2c5362ad822b4a450df550a52a9678eed
        draw=ImageDraw.Draw(img)
        j=0
        while j < particle_number:
            if is_in_zone(Xmin,Ymin,Xcenter, Ycenter, rdx[j], rdy[j]):
                shape=[ (rdx[j]+k*contraction_step, rdy[j]+k*contraction_step), (rdx[j]+k*contraction_step+particle_size, rdy[j]+k*contraction_step+particle_size)]
            elif is_in_zone(Xcenter,Ymin,Xmax, Ycenter, rdx[j], rdy[j]):
                shape=[ (rdx[j]-k*contraction_step, rdy[j]+k*contraction_step), (rdx[j]-k*contraction_step+particle_size, rdy[j]+k*contraction_step+particle_size)]
            elif is_in_zone(Xmin,Ycenter,Xcenter, Ymax, rdx[j], rdy[j]):
                shape=[ (rdx[j]+k*contraction_step, rdy[j]-k*contraction_step), (rdx[j]+k*contraction_step+particle_size, rdy[j]-k*contraction_step+particle_size)]
            elif is_in_zone(Xcenter, Ycenter, Xmax, Ymax, rdx[j], rdy[j]):
                shape=[ (rdx[j]-k*contraction_step, rdy[j]-k*contraction_step), (rdx[j]-k*contraction_step+particle_size, rdy[j]-k*contraction_step+particle_size)]
            else:
                shape=[ (rdx[j], rdy[j]), (rdx[j]+particle_size, rdy[j]+particle_size)]
            draw.ellipse(shape, fill="white", outline="white")
            j=j+1
<<<<<<< HEAD
        blur=img.filter(ImageFilter.GaussianBlur(radius=gaussian_blur_radius))
        blur.save(output_folder+'image'+str(k)+'.tiff')
=======
        img.save(output_folder+'image'+str(k)+'.tiff')
>>>>>>> c6f180c2c5362ad822b4a450df550a52a9678eed
        k=k+1