import numpy as np
import os 
import re 
import glob
import pandas
import subprocess 
import csv
import imageio

# root directory
root_path = '/home/hannah/mva/recvis/project/aot-recvis/'

tool_process_wd = root_path + '../AoT_Dataset/tool_process/'

path_to_data ='data/jpegs_256/'

folders = [f for f in os.listdir(path_to_data)]

paths_train = folders

def remove_black_frame(path_to_image):
	im = imageio.imread(path_to_image)
	means_rgb = np.mean(im, axis=2)
	row_means = np.mean(means_rgb, axis=1)
	col_means = np.mean(means_rgb, axis=0)

	row_start = next(x[0] for x in enumerate(row_means) if x[1] > 1)
	col_start = next(x[0] for x in enumerate(col_means) if x[1] > 1)
	row_finish = len(row_means) - next(x[0] for x in enumerate(np.flip(row_means)) if x[1] > 1)
	col_finish = len(col_means) - next(x[0] for x in enumerate(np.flip(col_means)) if x[1] > 1)
	return row_start, col_start, row_finish, col_finish

for i in range(len(folders)):
	try:
		print(i)
		### pre-define all paths
		images_folder = root_path + path_to_data + paths_train[i]
		images_path = root_path + path_to_data + paths_train[i] + '/frame%06d.jpg'
		output_extract = root_path + 'clean/' + paths_train[i] + '/extract'
		output_homo = root_path + 'clean/' + paths_train[i] + '/homo.txt'
		#output_mean_frame = root_path + 'clean/' + paths_train[i] + '/mean_frame.txt'
		output_mean_frame_diff = root_path + 'clean/' + paths_train[i] + '/mean_frame_diff.txt'
		output_warp = root_path + 'clean/' + paths_train[i] + '/warp'
		output_warp_bb = root_path + 'clean/' + paths_train[i] + '/war_bb.txt'
		output_flow = root_path + 'clean/' + paths_train[i] + '/flow'
		output_border = root_path + 'clean/' + paths_train[i] + '/border.txt'

		# make folder with name of video
		subprocess.call('mkdir ' + paths_train[i], 
			    cwd = root_path + 'clean', 
			    shell = True)

		### Get mean difference
		subprocess.call('./mDF'+' '+images_path+' '+output_mean_frame_diff+' 1', 
			    cwd = tool_process_wd, 
			    shell = True)

		### Get black frame
		list_files = os.listdir(images_folder)
		five_files = np.random.choice(list_files, 5)
		row_start, col_start, row_finish, col_finish = -np.inf, -np.inf, np.inf, np.inf
		for j in range(5):
			a, b, c, d = remove_black_frame(images_folder+'/'+five_files[j])
			row_start, col_start, row_finish, col_finish = max(row_start, a), max(col_start, b), min(row_finish, c), min(col_finish, d)
			border_file = str(row_start)+', '+str(col_start)+', '+str(row_finish-row_start)+', '+str(col_finish-col_start)+','
			print(border_file,  file=open(output_border, 'w'))

		### Decide which 41 images to take 
		### get 41 images from centre of image
		with open(output_mean_frame_diff, 'r') as f:
			reader = csv.reader(f)
			means_list = list(reader)

		means_list = np.int_(means_list)
		max_means = np.max(means_list, axis=1)
		conv_max_means = np.convolve(max_means, np.ones((41,))/41, mode='same')
		too_large = np.array([0 if x < 4 else 1 for x in conv_max_means])
		too_large[:21]=1
		too_large[-21:]=1
		median_frame = np.argmax(conv_max_means*(1-too_large))
		# print(paths_train[i])
		if (median_frame<22 or median_frame>(len(list_files)-22)):
			outskirts = np.ones(len(conv_max_means))
			outskirts[:21]=np.inf
			outskirts[-21:]=np.inf
			median_frame=np.argmin(conv_max_means*outskirts)
		### extract and crop
		subprocess.call('mkdir ' + 'extract', 
			cwd = root_path + 'clean/' + paths_train[i], 
			shell = True)

		subprocess.call('./eF'+' '+images_path+' '+output_extract+' '
			    +str(median_frame-20)+' '
			    +str(median_frame+20)+' 1 256 jpg '+output_border, 
			cwd = tool_process_wd, 
			shell = True)

		### compute homology
		subprocess.call('./cHFolder'+' '+output_extract+' '+output_homo +' 1 21 41', 
			    cwd = tool_process_wd, 
			    shell = True)

		### warp using homology
		subprocess.call('mkdir ' + 'warp', 
			    cwd = root_path + 'clean/' + paths_train[i], 
			    shell = True)

		subprocess.call('./wHFolder'+' '+output_extract+' '+output_homo+
			    ' '+output_warp+' 1 21 41 1 1 1 jpg', 
			    cwd = tool_process_wd, 
			    shell = True)

		### get flow
		subprocess.call('mkdir ' + 'flow', 
			    cwd = root_path + 'clean/' + paths_train[i], 
			    shell = True)

		subprocess.call('mkdir ' + 'b', 
			    cwd = output_flow, 
			    shell = True)

		subprocess.call('mkdir ' + 'f', 
			    cwd = output_flow, 
			    shell = True)

		subprocess.call('./doF256Folder'+' '+output_warp+' '+output_flow+' 10 0 1 jpg 1 21 41', 
			    cwd = tool_process_wd, 
			    shell = True)
	except:
		pass

