sudo apt-get update
mkdir downloads 
cd ~/downloads
###### CUDA #######
echo 'cuda'
wget https://developer.nvidia.com/compute/cuda/8.0/Prod2/local_installers/cuda-repo-ubuntu1604-8-0-local-ga2_8.0.61-1_amd64-deb
wget https://developer.nvidia.com/compute/cuda/8.0/Prod2/patches/2/cuda-repo-ubuntu1604-8-0-local-cublas-performance-update_8.0.61-1_amd64-deb
sudo dpkg -i cuda-repo-ubuntu1604-8-0-local-ga2_8.0.61-1_amd64-deb
sudo apt-get update
sudo apt-get install cuda
sudo dpkg -i cuda-repo-ubuntu1604-8-0-local-cublas-performance-update_8.0.61-1_amd64-deb
sudo apt-get update
sudo apt-get upgrade cuda
sudo apt-get install unzip 
###### CUDNN ######
echo 'cudnn'
cd ~/downloads
gsutil cp gs://ucf101/cudnn-8.0-linux-x64-v5.1.tgz .
tar xvzf cudnn-8.0-linux-x64-v5.1.tgz
sudo cp -P cuda/include/cudnn.h /usr/local/cuda/include
sudo cp -P cuda/lib64/libcudnn* /usr/local/cuda/lib64
sudo chmod a+r /usr/local/cuda/include/cudnn.h /usr/local/cuda/lib64/libcudnn*
echo 'copy the following lines to add at end: export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/local/cuda/lib64:/usr/local/cuda/extras/CUPTI/lib64"
export CUDA_HOME=/usr/local/cuda'
read -p 'Press enter to continue'
nano ~/.bashrc
source ~/.bashrc
###### TORCH ######
echo 'torch'
git clone https://github.com/torch/distro.git ~/torch --recursive
cd ~/torch; bash install-deps;
./install.sh
source ~/.bashrc
###### CONDA ######
echo 'conda'
cd ~/downloads
wget https://repo.continuum.io/archive/Anaconda3-2018.12-Linux-x86_64.sh
bash Anaconda3-2018.12-Linux-x86_64.sh 
source ~/.bashrc
conda update conda
##### PYTORCH #####
echo 'pytorch'
conda install pytorch torchvision -c pytorch
##### CLEAN LUA #####
echo 'clean_lua'
cd ~/downloads
gsutil cp gs://ucf101/clean_lua.zip .
