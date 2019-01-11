import numpy as np
import os 
import re 
import glob
from shutil import copytree
from shutil import move

path_to_data = '/home/hannah/mva/recvis/project/aot-recvis/clean/'

folders = [f for f in os.listdir(path_to_data)]

# gets files where the flow was generated correctly
# copies them to a folder called clean (subfolders are now f and b with flow_x_... and flow_y_... as subfiles)
for fold in folders:
    if ((len(glob.glob(path_to_data+fold+'/'+'flow/b/flow*'))==80) and (len(glob.glob(path_to_data+fold+'/'+'flow/f/flow*'))==80)):
        src = path_to_data+fold+'/'+'flow/'
        dst = '/media/hannah/hdd/recvis_data/clean'+fold
        copytree(src, dst)

# create subfolders x and y for the x and y flows 
path_to_data = '/media/hannah/hdd/recvis_data/clean/'
folders = [f for f in os.listdir(path_to_data)]

i=0
for fold in folders:
    i+=1
    print(i)
    x_flow_b = glob.glob(path_to_data+fold+'/'+'b/flow_x_*')
    y_flow_b = glob.glob(path_to_data+fold+'/'+'b/flow_y_*')
    x_flow_f = glob.glob(path_to_data+fold+'/'+'f/flow_x_*')
    y_flow_f = glob.glob(path_to_data+fold+'/'+'f/flow_y_*')

    os.chdir(path_to_data+fold+'/'+'b/')
    if not os.path.exists('x'):
        os.makedirs('x')
        os.makedirs('y')

    os.chdir(path_to_data+fold+'/'+'f/')
    if not os.path.exists('x'):
        os.makedirs('x')
        os.makedirs('y')

    for xfl in x_flow_b: 
        move(xfl, path_to_data+fold+'/'+'b/x/')

    for yfl in y_flow_b: 
        move(yfl, path_to_data+fold+'/'+'b/y/')

    for xfl in x_flow_f: 
        move(xfl, path_to_data+fold+'/'+'f/x/')

    for yfl in y_flow_f: 
        move(yfl, path_to_data+fold+'/'+'f/y/')

### get subsample of files 
subsample = np.random.choice(folders, 100)

for fold in subsample:
    src = path_to_data+fold
    dst = '/media/hannah/hdd/recvis_data/clean_subsample/'+fold
    copytree(src, dst)




