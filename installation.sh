###################
###### CUDA #######
###################

mkdir downloads 
cd downloads 
wget https://developer.nvidia.com/compute/cuda/8.0/Prod2/local_installers/cuda-repo-ubuntu1604-8-0-local-ga2_8.0.61-1_amd64-deb
wget https://developer.nvidia.com/compute/cuda/8.0/Prod2/patches/2/cuda-repo-ubuntu1604-8-0-local-cublas-performance-update_8.0.61-1_amd64-deb
sudo dpkg -i cuda-repo-ubuntu1604-8-0-local-ga2_8.0.61-1_amd64-deb
sudo apt-get update
sudo apt-get install cuda
sudo dpkg -i cuda-repo-ubuntu1604-8-0-local-cublas-performance-update_8.0.61-1_amd64-deb
sudo apt-get update
sudo apt-get upgrade cuda

######################
###### AoT_TCAM ######
######################

sudo cd downloads
wget https://github.com/donglaiw/AoT_TCAM/archive/master.zip
sudo apt-get install unzip 
unzip master.zip
# from own computer 
scp /media/hannah/hdd/recvis_data/clean_lua.zip hannah@35.193.61.70:~/downloads
scp /media/hannah/hdd/recvis_data/train01_cnn_ta_flow_orig_fb.txt hannah@104.154.26.113:~/downloads/AoT_TCAM-master/data
scp /media/hannah/hdd/recvis_data/test01_cnn_ta_flow_orig_fb.txt hannah@104.154.26.113:~/downloads/AoT_TCAM-master/data
scp /home/hannah/mva/recvis/project/AoT_TCAM/donkey_video.lua hannah@104.154.26.113:~/downloads/AoT_TCAM-master/


###################
###### CUDNN ######
###################

## from own computer 
scp cudnn-8.0-linux-x64-v5.1.tgz hannah@34.76.45.241:~/downloads
## back to instance
sudo apt-get install unzip 
tar xvzf cudnn-8.0-linux-x64-v5.1-ga.tgz
sudo cp -P cuda/include/cudnn.h /usr/local/cuda/include
sudo cp -P cuda/lib64/libcudnn* /usr/local/cuda/lib64
sudo chmod a+r /usr/local/cuda/include/cudnn.h /usr/local/cuda/lib64/libcudnn*
nano ~/.bashrc
# add following line at end
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/local/cuda/lib64:/usr/local/cuda/extras/CUPTI/lib64"
export CUDA_HOME=/usr/local/cuda
# then 
source ~/.bashrc

###################
###### LUA ########
###################

sudo apt-get install lua5.1

###################
###### TORCH ######
###################

git clone https://github.com/torch/distro.git ~/torch --recursive
cd ~/torch; bash install-deps;
./install.sh
source ~/.bashrc

###################
###### CONDA ######
###################

wget https://repo.continuum.io/archive/Anaconda3-2018.12-Linux-x86_64.sh
bash Anaconda3-2018.12-Linux-x86_64.sh 
source ~/.bashrc
conda update conda

###################
##### PYTORCH #####
###################

# python -m pip install -t lib http://download.pytorch.org/whl/cu80/torch-0.3.1-cp27-cp27mu-linux_x86_64.whl 
# python -m pip install -t lib torchvision 
conda install pytorch torchvision -c pytorch
