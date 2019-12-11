Useful technique

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

# 开启vncserver
vncserver :2 -geometry 1920x1080 -depth 24

# 去ubuntu控制机器上, 配置remmina, 连接上面配置的这台远程被控机器. 
```
ubuntu18.04 [参考配置介绍](http://www.sohu.com/a/307156161_120123557) , 
ubuntu16.04 [参考配置介绍](http://www.freetutorialssubmit.com/Ubuntu+Remote+Desktop+multiple+users) .

### How to enable port 22
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

