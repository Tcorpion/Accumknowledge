# Docker

## Profiles
 * Installation

## Installation

* Building docker image you need
  * [This tutorial](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04#step-1-%E2%80%94-installing-docker) tells how to install latest docker from official repo.
  * Install nvidia-drivers and cuda drivers required for running current versions of models: [guide](https://gist.github.com/bzamecnik/b0c342d22a2a21f6af9d10eba3d4597b) can be used, but be sure to modify CUDA and cuDNN to the desired versions
    * Verify drivers installed by running `nvidia-smi` in shell, this will display a status output of your gpu device

  * Install [docker](https://docs.docker.com/engine/install/ubuntu/) and
  * Install [nvidia-container-toolkit or nvidia-container-runtime](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) after docker installation.
    ```
    # the following refers to https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html
    curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
       && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
       sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
       sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
    sed -i -e '/experimental/ s/^#//g' /etc/apt/sources.list.d/nvidia-container-toolkit.list
    sudo apt-get update
    
    sudo apt-get install -y nvidia-container-toolkit
    sudo nvidia-ctk runtime configure --runtime=docker
  
    sudo systemctl restart docker
    ```

    ```
    # the following refers to https://blog.csdn.net/ys5773477/article/details/133642150
    sudo curl -s -L https://nvidia.github.io/nvidia-container-runtime/gpgkey
    sudo apt-key add -distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
    sudo curl -s -L https://nvidia.github.io/nvidia-container-runtime/$distribution/nvidia-container-runtime.list
    sudo tee /etc/apt/sources.list.d/nvidia-container-runtime.list
    sudo apt-get update
    
    sudo apt-get install nvidia-container-runtime
    
    systemctl restart docker
    ```

## Run docker image without entrance

For docker image `gcr.io/xxxxxx/yyy:zzz`, run it in sleeping mode
```
sudo docker run -idt \
    --shm-size="1g" \
    --ulimit core=-1 \
    --security-opt seccomp=unconfined \
    gcr.io/xxxxxx/yyy:zzz sleep infinity

sudo docker run -d \
  --gpus all \
  -v ~/aa:/tmp/aa \
  -v /data/bb:/tmp/bb \
  -v /data/code:/cache/code \
  -it gcr.io/xxxxxx/yyy:zzz sleep infinity

# specify gpu id to container
sudo docker run -d \
  --gpus \"device=0,3\" \
  -v ~/aa:/tmp/aa \
  -v /data/bb:/tmp/bb \
  -v /data/code:/cache/code \
  -it gcr.io/xxxxxx/yyy:zzz sleep infinity
 ```
 
