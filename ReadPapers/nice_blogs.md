Useful technique

#### Where to learn Nginx
https://tengine.taobao.org/book/index.html

#### How to transform a tensorflow model to tensorRT model
https://devblogs.nvidia.com/tensorrt-integration-speeds-tensorflow-inference/

#### How to use tensorRT
https://docs.nvidia.com/deeplearning/sdk/tensorrt-install-guide/index.html
https://docs.nvidia.com/deeplearning/sdk/tensorrt-developer-guide/index.html
###### Migrating from TensorRT 4 to 5
https://docs.nvidia.com/deeplearning/sdk/tensorrt-api/python_api/gettingStarted.html
#### How to run a tensorRT inference server
https://docs.nvidia.com/deeplearning/sdk/tensorrt-inference-server-guide/docs/quickstart.html

#### How to set jupyter
Step 1 install the jupyter
```buildoutcfg
pip install jupyter
```
Step 2 finish the config file
```buildoutcfg
jupyter notebook --generate-config # this line generate a default config file '~/.jupyter/jupyter_notebook_config.py'
# 打开ipython，创建一个密文的密码：
In [1]: from notebook.auth import passwd
In [2]: passwd()Enter password: 
Verify password: 
Out[2]: 'sha1:ce23d945972f:34769685a7ccd3d08c84a18c63968a41f1140274'
$vim ~/.jupyter/jupyter_notebook_config.py  # 注意目录根据自己实际确定
# 进行如下修改：
c.NotebookApp.ip='0.0.0.0'
c.NotebookApp.password = 'sha1:ce23d945972f:34769685a7ccd3d08c84a18c63968a41f1140274'(复制的上面那个密文的hash码, 网页登录用原值)
c.NotebookApp.open_browser = False
c.NotebookApp.port =8888 #随便指定一个端口
```

step 3 use the jupyter notebook
```buildoutcfg
conda activate YourPythonEnv
jupyter notebook
```
去浏览器打开,输入登录密码, 尽情享用

#### How to set vnc4server
ubuntu18.04 和 16.04 的配置不一样,
ubuntu18.04选择使用xfce4作为远程桌面, 配置步骤:
```
# 安装 vnc4server，xfce4
sudo apt install vnc4server xfce4 xfce4-goodies  

# 启动+关闭VNC server, 默认创建了VNC xstartup配置文件
vncserver :2
vncserver -kill :2
 
# 修改 ~/.vnc/xstartup 配置信息为如下(其他内容不保留):

vim ~/.vnc/xstartup
    #!/bin/sh 
    # Uncomment the following two lines for normal desktop: 
    unset SESSION_MANAGER 
    unset DBUS_SESSION_BUS_ADDRESS 
    startxfce4 & 
    
# 设置vncserver密码
vncpasswd

# 开启vncserver
vncserver :2 -geometry 1920x1080 -depth 24

# 去ubuntu控制机器上, 配置remmina, 连接上面配置的这台远程被控机器. 
```
ubuntu18.04 [参考配置介绍](http://www.sohu.com/a/307156161_120123557) , 
ubuntu16.04 [参考配置介绍](http://www.freetutorialssubmit.com/Ubuntu+Remote+Desktop+multiple+users) .

错误解决：报错Failed to connect to socket /tmp/dbus-xxxxxxx: Connection refused
```
vim ~/.vnc/xstartup
    #!/bin/sh 
    # Uncomment the following two lines for normal desktop: 
    unset SESSION_MANAGER 
    unset DBUS_SESSION_BUS_ADDRESS 
    dbus-launch /usr/bin/startxfce4 &
```
重启vncserver
`
vncserver :2 -geometry 1920x1080 -depth 24
`
如果端口权限有问题， 尝试：
`
sudo ufw allow from any to any port 2 proto tcp
`

#### How to enable port 22
Make sure a port like 22 in ubuntu is disable
```buildoutcfg
# nothing output means the port is disable
sudo netstat -ntlp|grep 22

# run following
sudo apt-get install openssh-server
sudo apt-get install ufw
sudo ufw enable
sudo ufw allow 22

# make sure this port is working, the above line outputs the bellow
sudo netstat -ntlp|grep 22
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      10540/sshd          
tcp6       0      0 :::22                   :::*                    LISTEN      10540/sshd
```

#### Start up automatically in [Ubuntu18.04 (开机自动启动脚本设置)](https://blog.csdn.net/github_38336924/article/details/98183253)

* Ubuntu18.04 默认是没有 `/etc/rc.local` 这个文件的，需要自己创建
* systemd 默认读取 `/etc/systemd/system` 下的配置文件，该目录下的文件会链接`/lib/systemd/system/`下的文件。
* 执行 `ls /lib/systemd/system` 你可以看到有很多启动脚本，其中就有我们需要的 `rc.local.service`.
查看`/lib/systemd/system/rc.local.service`文件内容
    ```
    #  SPDX-License-Identifier: LGPL-2.1+
    #
    #  This file is part of systemd.
    #
    #  systemd is free software; you can redistribute it and/or modify it
    #  under the terms of the GNU Lesser General Public License as published by
    #  the Free Software Foundation; either version 2.1 of the License, or
    #  (at your option) any later version.
    
    # This unit gets pulled automatically into multi-user.target by
    # systemd-rc-local-generator if /etc/rc.local is executable.
    [Unit]
    Description=/etc/rc.local Compatibility
    Documentation=man:systemd-rc-local-generator(8)
    ConditionFileIsExecutable=/etc/rc.local
    After=network.target
    
    [Service]
    Type=forking
    ExecStart=/etc/rc.local start
    TimeoutSec=0
    RemainAfterExit=yes
    GuessMainPID=no
    ```
 
* 一般正常的启动文件主要分成三部分
  * [Unit] 段: 启动顺序与依赖关系
  * [Service] 段: 启动行为,如何启动，启动类型
  * [Install] 段: 定义如何安装这个配置文件，即怎样做到开机启动
 
* 可以看出，`rc.local.service` 它少了 `Install` 段，也就没有定义如何做到开机启动，所以显然这样配置是无效的。 
因此我们就需要在后面帮他加上 `[Install]` 段，可以发现`rc.local.service`是`rc-local.service`文件的链接文件，所以我们只需要修改`rc-local.service`文件即可

* 在`/lib/systemd/system/rc-local.service` 文件中添加如下代码：
    ```
    [Install]  
    WantedBy=multi-user.target  
    Alias=rc-local.service
    ```

* 在/etc/目录下面创建`rc.local`文件，赋予执行权限，
    ```shell script
    touch /etc/rc.local
    chmod +x /etc/rc.local
    ```

* `/etc/rc.local` 文件添加开机自动启动命令， 命令写在`exit 0`之前， 如下内容：
    ```shell script
    #!/bin/sh -e
    #
    # rc.local
    #
    # This script is executed at the end of each multiuser runlevel.
    # Make sure that the script will "exit 0" on success or any other
    # value on error.
    #
    # In order to enable or disable this script just change the execution
    # bits.
    #
    # Add script to do your job before "exit 0", here is a docker run scripts automatically started.
    /usr/bin/docker run -d --runtime=nvidia --rm --name=nvidia-dcgm-exporter -v /run/prometheus:/run/prometheus nvidia/dcgm-exporter
    /usr/bin/docker run -d --rm --net="host" --pid="host" --volumes-from nvidia-dcgm-exporter:ro quay.io/prometheus/node-exporter --collector.textfile.directory="/run/prometheus"
    
    exit 0
    ```

#### Install donet core
Refer to the [docs](https://docs.microsoft.com/zh-cn/dotnet/core/install/linux-package-manager-ubuntu-1804)

#### 如何[确定高斯滤波的标准差和窗口大小](https://www.cnblogs.com/shine-lee/p/9671253.html)

#### 断电后本地ubuntu18.04机器无法接入外网的解决办法
    ```
    #sudo vim /etc/resolv.conf #找一些公开dns 地址加进来，比如114.114.114.119，114.114.115.119， 注释掉现有的地址
    systemctl restart networking #重启网络
    sudo vim /etc/systemd/resolved.conf # 改这里的dns才能有效
    ```
#### TF 1.14 CUDA_ERROR_OUT_OF_MEMORY
When I trained a maskrcnn in a gpu mechine (1080ti, TaiTanXP), there was a error coming out frequently "Attempting to fetch value instead of handling error Internal: failed initializing StreamExecutor for CUDA device ordinal 0: Internal: failed call to cuDevicePrimaryCtxRetain: CUDA_ERROR_OUT_OF_MEMORY: out of memory; ... "
To fix the above error, I add `export CUDA_VISIBLE_DEVICES=1` before training with tf 1.14 by referring https://stackoverflow.com/questions/51430062/unable-to-create-tensorflow-session-internal-failed-initializing-streamexecut
