#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 08:43:34 2020

@author: sschanz
"""

from landlab.components import LinearDiffuser, StreamPowerEroder, FlowAccumulator
from landlab.io import read_esri_ascii, write_esri_ascii
from landlab.plot.imshow import imshow_grid
import matplotlib.pyplot as plt
import pathlib
import os

"""
This code uses the Landlab toolkit (https://landlab.readthedocs.io/en/latest/index.html) to simulate diffusion and erosion across a landscape. The intent is to examine how an inactive earthflow evolves over 10k, with ascii files exported every 2k that can be imported to ArcGIS and used to calculate MAD roughness (https://github.com/cageo/Trevisani-2015).
"""

### IMPORT ASCI OF A EARTHFLOW IN TEANAWAY
(mg, z) = read_esri_ascii("Jungle_creek.asc", name = "topographic__elevation") #elevation in feet, distance in feet

### PLOT INITIAL TOPOGRAPHY
fig1 = plt.figure()
imshow_grid(mg, 'topographic__elevation')
plt.title('Initial topography')

### DIFFUSE and EROD THROUGH TIME AND OUTPUT EVERY 2000 YEARS
ld = LinearDiffuser(mg, linear_diffusivity = 0.002) # Diffusivity from Martin, 2000
fa = FlowAccumulator(mg,flow_director = 'D8')
sp = StreamPowerEroder(mg, K_sp = 0.0001)

dt = 100
time = 10000

for x in range(0,time,dt):
    ld.run_one_step(dt)
    fa.run_one_step()
    sp.run_one_step(dt)
    
    if x%2000 == 0:
        fname = os.path.join(pathlib.Path().absolute(), 'slide_sp_%s.asc' % x)
        write_esri_ascii(fname, mg, 'topographic__elevation')

### PLOT END TOPOGRAPHY
fig2 = plt.figure()
imshow_grid(mg, 'topographic__elevation')
plt.title('End topography')  