# Docker

## Profiles
 * Installation

## Installation

* Building docker image you need
  * [This tutorial](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04#step-1-%E2%80%94-installing-docker) tells how to install latest docker from official repo.
  * Install nvidia-drivers and cuda drivers required for running current versions of models: [guide](https://gist.github.com/bzamecnik/b0c342d22a2a21f6af9d10eba3d4597b) can be used, but be sure to modify CUDA and cuDNN to the desired versions
    * Verify drivers installed by running `nvidia-smi` in shell, this will display a status output of your gpu device

  * Install [docker](https://docs.docker.com/install/) and [nvidia docker version 2.0](https://github.com/nvidia/nvidia-docker/wiki/Installation-(version-2.0)). The easiest way to do this is to run
    * `curl -fsSL get.docker.com -o get-docker.sh` and then `sh get-docker.sh`, this installs docker
    * Follow steps in [nvidia docker](https://github.com/nvidia/nvidia-docker/wiki/Installation-(version-2.0)) to install/
    * ~~ if you can't install nvidia-docker2 after `sudo apt-get update`, see: https://nvidia.github.io/nvidia-docker/
    * Verify the installation by running `sudo docker run --runtime=nvidia --rm nvidia/cuda:9.0-base nvidia-smi`, this runs the same `nvidia-smi` command as before but inside of the docker container, if all is working then you will see similar status screen
    ```
        Mon Mar 18 09:32:18 2019       
    +-----------------------------------------------------------------------------+
    | NVIDIA-SMI 396.26                 Driver Version: 396.26                    |
    |-------------------------------+----------------------+----------------------+
    | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
    | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
    |===============================+======================+======================|
    |   0  Tesla K80           Off  | 00008751:00:00.0 Off |                    0 |
    | N/A   64C    P0    64W / 149W |      0MiB / 11441MiB |     97%      Default |
    +-------------------------------+----------------------+----------------------+
                                                                                   
    +-----------------------------------------------------------------------------+
    | Processes:                                                       GPU Memory |
    |  GPU       PID   Type   Process name                             Usage      |
    |=============================================================================|
    |  No running processes found                                                 |
    +-----------------------------------------------------------------------------+

    ```
  *Note:  Nvidia drivers must be installed on the host machine and be aware of NVIDIA Driver Version.

## Run docker image without entrance

For docker image `gcr.io/xxxxxx/yyy:zzz`, run it in sleeping mode
```
sudo docker run -idt \
    --shm-size="1g" \
    --ulimit core=-1 \
    --security-opt seccomp=unconfined \
    gcr.io/xxxxxx/yyy:zzz sleep infinity
 ```
 
