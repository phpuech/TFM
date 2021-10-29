#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 13:41:37 2020
Modified strongly on Tue Feb 16 2021
@author: php

corrected for PIV proper calibration
and axis for maps on 9/7/21 (see below)
"""
# import packages for easy work
import numpy as np
import scipy as sp
# image : PIL et creation image sp
# from PIL import Image
# from scipy import ndimage
import matplotlib.pyplot as plt
# from scipy.optimize import curve_fit
# import matplotlib.gridspec as gridspec
import pandas as pd
# import os
# import time
import seaborn as sns
import matplotlib.cm as cm
from matplotlib.colors import Normalize
import math
import os
import shutil as sh
# from skimage import data, io, filt
import os
#============================================================
# TO BE CHECKED BY SYSTEMATIC DEBUGGING AND READING THE DOCS
# 1. MODIFIED IN CODE : some lines to check (plot quiver and colors bars) in part. norm of quivers...
# 2. indexes of times for the plots : starts at 1 or 0 ? PIV_1 is the frame 1 vs 0 : DONE - that only offsets the zero by one point
# 3. CHECKED IN TXT FILE : look for negative vector components of displacement vs stress
# 4. look for bin of hist : DONE 9/7/21
# 5. properly scale the axis of the maps : pixels to µm : DONE 9/7/21
# 6. check the autoscale function to turn them all autoscale
# 7. CHECKED USING NOTEBOOK : scalar product
# 8. ADDED IN CODE : colorbar for stress norm image, with absolute and relative max
# 9. ADDED IN CODE : axis in µm using pix2um for quivers : DONE 9/7/21
# 10. TO CORRECT : axis in µm for STRESS MAP (attention pix vs datapoint) : DONE 9/7/21
# 11. modified : booleans for choices overs plots, curves, new name in case of rerun...
#============================================================
#------------------------------------------------------------
#------------------------------------------------------------
# TO BE MODIFIED BY THE USER
#-----
# where is the data
source = '/home/php/Desktop/TFMFINALREG9x10-10ABC1MED15s/Forarticle/aligned'
new='' #'' #if empty str does not append anything to rep names
# time btw frames in secs
dt=5
# for energy calculation
vs3=8# pix, last window from calculation in Q.Tseng PIV, see also Martiel 2015 TFM in ImageJ
pix2um=0.156 # µm/pix, from lens calibration ; 40x AFM 0.156µm/pix
#-----   
# What do you want to do ?
CurvesOnly=False # True will only send out the selected curve(s), not the images
# Which Curves ?
SignalOverImage=True
Energy=True
StressCurve='sum' #'sum', 'median', 'mean'
# Which plots if not CurvesOnly=True ?
MapDisplVect=False # quiver of vectors of displacement
HistDisplNorm=False # histograms of displacement norm, same bin size
MapStressVect=False # quiver of "vectors of stress"
MapStressNorm=False # discreet map of stress norm
decimals=1 #for rounding the x,y axis values
MapStressNormImage=True # stress norm map as interpolated, smoothed image
#-----
# for data duplication
Move=False # True, Move the files, while False : keep a copy at original place
#-----
 # output parameters for aesthetics of plots and maps
 # for manual setting the color scales of stress maps
 # Stress Heatmap
maxMap=240 # Pa, for output as a heatmap (discreet image)
# Stress Image
maxImage=240 # Pa, for output map as image
Autoscale =False
SmoothIt='gaussian' # for interpolation on MapStressNormImage 
'''
the smoothing of the images can be 'none', 'nearest', 'bilinear', 'bicubic', 'spline16', 'spline36', 
# 'hanning', 'hamming', 'hermite', 'kaiser', 'quadric',
# 'catrom', 'gaussian', 'bessel', 'mitchell', 'sinc', 'lanczos' 
'''
# displacement histos param
maxdepl=2#µm
widthbin=0.1#µm
maxdeplNumber=50
# for the two types of quivers
quivercolor=True # plot with arrows in color coded to amplitude
amplDispl=0.2#None # for displacement quiver : number of units per vector lentgh - can be se to None for autoscale
amplStress=50#None # for stress quiver : number of units per vector lentgh - can be se to None for autoscale
# generic image parameters for output
# for output, dpi of the images that are saved
dotperinch=150
#image size (inch)
inch=5
#------------------------------------------------------------
#------------------------------------------------------------
# Start of real code...
#------------------------------------------------------------

PIVbool=(MapDisplVect or HistDisplNorm)
FTTCbool=(MapStressNorm or MapStressNormImage or MapStressVect)

# loop over subfolders ie over segments of the same movie
subdirs = [os.path.join(source, segment) for segment in os.listdir(source) if os.path.isdir(os.path.join(source,segment))]
for sub in subdirs:
    
    
    inputpathTop=sub+'/save/'
    print(inputpathTop)
    
    filesToSort = [f for f in os.listdir(inputpathTop) if f.endswith('.txt')]
    filesToSort.sort()
    
    # creating folders in subsfolders for file sorting
    if PIVbool or Energy:
        copyPIV=inputpathTop+'PIV'+new+'/'
        if not os.path.exists(copyPIV):
            os.makedirs(copyPIV)
    # sorting the different text files in copyPIV)
        if MapDisplVect:
            copyPIV2=copyPIV+'piv/'
            if not os.path.exists(copyPIV2):
                os.makedirs(copyPIV2)
        if HistDisplNorm:
            outputHist=copyPIV+'hist-binconst/'
            if not os.path.exists(outputHist):
                os.makedirs(outputHist)
                
    if FTTCbool or not CurvesOnly:
        copyFTTC=inputpathTop+'FTTC'+new+'/'  
        if not os.path.exists(copyFTTC):
            os.makedirs(copyFTTC)
        if MapStressVect:
            outputD=copyFTTC+'mapFarrows/'
            if not os.path.exists(outputD):
                os.makedirs(outputD)
        if MapStressNorm:
            outputFdiscret=copyFTTC+'mapFdiscret/'
            if not os.path.exists(outputFdiscret):
                os.makedirs(outputFdiscret)
        if MapStressNormImage:
                outputF=copyFTTC+'mapF/'
                if not os.path.exists(outputF):
                    os.makedirs(outputF)   
        outputC=copyFTTC+'curves/'
        if not os.path.exists(outputC):
            os.makedirs(outputC)    
        
    # sorting the different text files in subfolders   
    for i in filesToSort:
        if (FTTCbool and ("Traction" in str(i))):
            sh.copy(inputpathTop+i, copyFTTC)
            if Move:
                os.remove(inputpathTop+i)
            print(str(i), "> FTTC")
        elif ((PIVbool or Energy) and ("PIV" in str(i))) :
            if not ("FTTC" in str(i)):
                    if not ("Traction" in str(i)):
                            sh.copy(inputpathTop+i, copyPIV)
                            if Move:
                                os.remove(inputpathTop+i)
                            print(str(i), "> PIV")
        else:
            print(str(i), "> this file is not copied")
    
    #-----
    # PIV reconstructions and histograms        
    # where is the data for PIV maps processing
    if PIVbool:
        inputpathPIV=copyPIV
        filesPIV = [f for f in os.listdir(inputpathPIV) if f.endswith('.txt')]
        filesPIV.sort()
    
    # number of files
        totalPIV=len(filesPIV)
        print("Number of files for PIV:", totalPIV)
    
    # clean the display
        plt.close(fig='all')
    
    # for indication of remaining files to process
        j=1
        
        # rebuilding the PIV maps and plot histograms
        for i in filesPIV:
            print("processing", i, " - ", totalPIV-j, " files left")
            datafile =inputpathPIV+i
        
            #loading only the first 5 columns cf website Q. Tseng on PIV
            originaldata = pd.read_csv(datafile, delimiter=r"\s+",   comment='#', usecols=[0,1,2,3,4], names=['x', 'y','dx', 'dy','dnorm'])
        
            #reorient the df 
            #mapdata=pd.pivot_table(originaldata, values='dnorm', index=['y'], columns='x')
            
            if HistDisplNorm and not CurvesOnly: # histogram plot of norm f displacement
                fig1=plt.figure('HistDisplNorm', figsize=(inch, inch), dpi=dotperinch)
                n = math.ceil((originaldata['dnorm'].max() - originaldata['dnorm'].min())*pix2um/widthbin)# corrected on 9/7/21
                plt.hist(originaldata['dnorm']*pix2um, density=False) # corrected on 9/7/21
                plt.xlabel("Displacement (µm)")
                plt.xlim(0,maxdepl)
                plt.ylabel("Number")
                plt.ylim(0,maxdeplNumber)
                fig1.tight_layout()
                plt.savefig(outputHist+str(i)+'.png')
        
            
            if MapDisplVect and not CurvesOnly:  # vector plots of displacement
                fig2=plt.figure('MapHistVect',figsize=(inch, inch), dpi=dotperinch)
                Distcolors=originaldata['dnorm'].values
                # warning there is a subtle point with minus sign on dy
                if quivercolor:
                	# check the following lines ---
    	            # normalize the colorscale 
                    norm=Normalize()
                    norm.autoscale(Distcolors)
                    colormap=cm.gist_heat
    	            #------------------------------
                    ax1=plt.quiver(originaldata['x']*pix2um, -originaldata['y']*pix2um,originaldata['dx']* pix2um, -originaldata['dy']* pix2um, color=colormap(norm(Distcolors)), units='xy', scale=amplDispl, width=0.15) # removed shaft width=1 # corrected on 9/7/21
                    plt.colorbar()
                else:
                	ax1=plt.quiver(originaldata['x']*pix2um, -originaldata['y']*pix2um,originaldata['dx']*pix2um, -originaldata['dy']*pix2um, units='xy', scale=amplDispl, width=0.15)# corrected on 9/7/21
    
                #scale axis to µm
                xmin, xmax = plt.xlim()
                ymin, ymax = plt.ylim()
                plt.xlim(0, xmax)
                plt.ylim(ymin,0)
                plt.xlabel('µm')
                plt.ylabel('µm')
                fig2.tight_layout()
                plt.savefig(copyPIV2+str(i)+'.png')
            
            # clean the display
            plt.close(fig='all')
            j=j+1
        
    #-----
    # FTTC reconstructions and histograms        
    # where is the data for FTTC maps processing
    
    if (FTTCbool or CurvesOnly):
        inputpathFTTC=copyFTTC    
        filesFTTC = [f for f in os.listdir(inputpathFTTC) if f.endswith('.txt')]
        filesFTTC.sort()
        
         
        
        # lists to store output calculated data
        StressSum=[]
        FrameNumber=[]
        FrameTime=[]
        
        # clean the display
        plt.close(fig='all')
        
        # total number of files
        totalFTTC=len(filesFTTC)
        print("Number of files for FTTC:", totalFTTC)
        if PIVbool and FTTCbool:
            print("Identical to number for PIV:", totalFTTC==totalPIV)
        
        # for indication of remaining files to process
        k=1    
        
        if StressCurve=='mean':
            StressTitle='Mean'
            StressName='StressMean.txt'
        elif StressCurve=='median':
            StressTitle='Median'
            StressName='StressMedian.txt'
        elif StressCurve=='sum':
            StressTitle='Sum'
            StressName='StressSum.txt'
        
        for i in filesFTTC:
            print("processing", i, " - ", totalFTTC-k, "to go")
            datafile =inputpathFTTC+i
        
            # create the scalings for the x and y scales
            originaldata = pd.read_csv(datafile, delimiter=r"\s+",   comment='#', names=['x', 'y','Sx', 'Sy','Snorm'])
            originaldata['xum']=np.around(originaldata['x']*pix2um,decimals) # decommented and corrected on 9/7/21
            originaldata['yum']=np.around(originaldata['y']*pix2um, decimals) # decommented and corrected on 9/7/21
           
        
            # append total stress 
            if StressCurve=='mean':
                sumsignal=originaldata['Snorm'].mean()
            elif StressCurve=='median':
                sumsignal=originaldata['Snorm'].median()
            elif StressCurve=='sum':
                sumsignal=originaldata['Snorm'].sum()
            
            StressSum.append(sumsignal)
            
            # recover frame number
            cut=i.split(".")
            recut=cut[0].split("_")
            frame=int(recut[2])
            
            # create x-axis lists for plots
            FrameNumber.append(frame)
            FrameTime.append(frame*dt)
        
            #mapdata=pd.pivot_table(originaldata, values='Snorm', index=['y'], columns='x') # commented on 9/7/21
            mapdata=pd.pivot_table(originaldata, values='Snorm', index=['yum'], columns='xum') # decommented on 9/7/21
        
            if MapStressNorm and not CurvesOnly: # discreet map of stress norm
                fig3=plt.figure('MapStressNorm', figsize=(inch, inch), dpi=dotperinch)
                if Autoscale:
                    sns.heatmap(mapdata, cmap='gist_heat', vmin=0)
                else:
                    sns.heatmap(mapdata, cmap='gist_heat', vmin=0, vmax=maxMap)
                #scale axis to µm
                # xmin, xmax = plt.xlim()
                # ymin, ymax = plt.ylim()
                # plt.xlim(0, xmax * pix2um)
                # plt.ylim(0, ymax * pix2um)
                plt.xlabel('µm')
                plt.ylabel('µm')
                fig3.tight_layout()
                plt.savefig(outputFdiscret+str(i)+'.png')
        
            if MapStressNormImage and not CurvesOnly: #stress norm as an interpolated image
                fig4=plt.figure('MapStressNormImage', figsize=(inch, inch), dpi=dotperinch)
                if Autoscale:
                    ax1=plt.imshow(mapdata, origin='upper',cmap='gist_heat', interpolation=SmoothIt, vmin=0)
                else:
                    ax1=plt.imshow(mapdata, origin='upper',cmap='gist_heat', interpolation=SmoothIt, vmin=0, vmax=maxImage) # removed : option extend for subsetting image
                # check the following lines ----
                plt.colorbar()
                #cbar.minorticks_on()
                plt.clim(0,maxImage)
                #scale axis to µm
                # xmin, xmax = plt.xlim()
                # ymin, ymax = plt.ylim()
                # plt.xlim(xmin * pix2um, xmax * pix2um)
                # plt.ylim(ymin * pix2um, ymax * pix2um)
                plt.xlabel('µm')
                plt.ylabel('µm')
                #-------------------------------
                fig4.tight_layout()
                plt.savefig(outputF+str(i)+'.png')
    
            if MapStressVect and not CurvesOnly: # "quiver of stress"
                fig5=plt.figure('MapStressVect', figsize=(inch, inch), dpi=dotperinch)
                Stresscolors=originaldata['Snorm'].values
                # warning there is a subtle point with minus sign on fy
                if quivercolor:
    	            # check the following lines ---
    	            # normalize the colorscale 
                    norm=Normalize()
                    norm.autoscale(Stresscolors)
                    colormap=cm.gist_heat
    	            #------------------------------inputpathTop+'FTTC/' 
                    ax1=plt.quiver(originaldata['x']*pix2um, -originaldata['y']*pix2um,originaldata['Sx'], -originaldata['Sy'], color=colormap(norm(Stresscolors)), units='xy', scale=amplStress, width=0.15) # removed shaft width=1 # corrected on 9/7/21
                    plt.colorbar()#cm.ScalarMappable(norm=norm, cmap='inferno'))
                else:
                	ax1=plt.quiver(originaldata['x']*pix2um, -originaldata['y']*pix2um,originaldata['Sx'], -originaldata['Sy'], units='xy', scale=amplStress, width=0.15) # corrected on 9/7/21
                #scale axis to µm
                xmin, xmax = plt.xlim()
                ymin, ymax = plt.ylim()
                plt.xlim(0, xmax)
                plt.ylim(ymin,0)
                plt.xlabel('µm')
                plt.ylabel('µm')
                fig5.tight_layout()
                plt.savefig(outputD+str(i)+'.png')
            
            plt.close(fig='all')
            k=k+1
        
        #--------------------------------------------------------------
        # building the curves and text data files
        #-----
        # building df for stress sum and same it to txt
        if SignalOverImage:
            df = pd.DataFrame({"N":FrameNumber, "t":FrameTime, "S":StressSum})
            df=df.sort_values(by=['N'])
            df.to_csv(outputC+StressName, sep="\t")
            
            # plot it
            fig6=plt.figure(StressTitle+' Stress over image', figsize=(inch, inch), dpi=dotperinch)        
            plt.plot(df['t'], df['S'], color='indianred')
            plt.xlim(0,)
            plt.ylim(0,22500)
            plt.ylabel(StressTitle+" of Stress, over image (Pa)")
            plt.xlabel("Time (sec)")
            fig6.tight_layout()
            plt.savefig(outputC+"Stress"+StressTitle+".png")
            #plt.ylim(0,)
            #plt.xlim(0,)
        
        #-----
        # energy calculation
        if Energy:
            Energy=[]
            NFrame=[]
            TFrame=[]
            
            # Unit area of the pixel of stress, for force as Stress*Unit rea, in m**2 cf Martiel 2015 and doc Q. Tseng
            UnitAreaForForce=(vs3*pix2um*10**(-6))**2
                        
            inputpathPIV=copyPIV
            inputpathFTTC=copyFTTC
            m=1
            #calculate the energy
            while m<totalFTTC:
                NFrame.append(m)
                TFrame.append(m*dt)
                
                pivfile = pd.read_csv(inputpathPIV+'PIV_'+str(m)+'.txt', delimiter=r"\s+",   comment='#', names=['xpix', 'ypix', 'dx', 'dy', 'dnormum'], usecols=[0,1,2,3,4]) # corrected on 9/7/21
                fttcfile = pd.read_csv(inputpathFTTC+'Traction_PIV_'+str(m)+'.txt', delimiter=r"\s+",   comment='#', names=['xpix', 'ypix', 'SxPa', 'SyPa', 'SnormPa'])
                
                #corrected for 1/2 on may 7, 2021 - PHP
                energysignal=(1/2)*(np.sum(fttcfile['SxPa']*pivfile['dx']*pix2um*10**(-6))+np.sum(fttcfile['SyPa']*pivfile['dy']*pix2um*10**(-6)))*UnitAreaForForce # corrected on 9/7/21
                Energy.append(energysignal)
                m=m+1
                
            # building dataframe and export as txt
            df2=pd.DataFrame({"N":NFrame, "t":TFrame, "E":Energy})
            df2.to_csv(outputC+"Energy.txt", sep="\t")
            
            # plot it
            fig7=plt.figure('Energy over image', figsize=(inch, inch), dpi=dotperinch)
            plt.xlim(0,1600)
            plt.ylim(0,1.8e-14)
            plt.plot(df2['t'], df2['E'], color='indianred')
            plt.ylabel("Energy, over image (J)")
            plt.xlabel("Time (sec)")
            fig7.tight_layout()
            plt.savefig(outputC+"Energy.png")
            #plt.ylim(0,)
            #plt.xlim(0,)
        
    #show the last two plots
    plt.show()
    
    
