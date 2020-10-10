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

#### FinalShell tool
This is a nice tool, referring to [here](https://www.jianshu.com/p/14c3b78ca570)

#### Trojan tutorial 

All tutorial details come from [here](https://tlanyan.me/trojan-tutorial/) , the following were copied.

pp.ua官方网站是 https://pp.ua/，页面都是俄文。幸运的是申请、激活域名和后台页面都有英文界面，有英语基础的无需借助翻译软件也可正常操作。

##### pp.ua申请教程, 

下面介绍个人二级免费域名pp.ua申请教程

    * 免费二级域名pp.ua申请, 参考[教程](https://tlanyan.me/personal-free-pp-ua-domain-tutorial/). 简要流程:
      * 打开 https://nic.ua/en/domains/.pp.ua，搜索框中输入要申请的二级域名，例如tlanyan，然后点击“Search”按钮查看是否已被注册；
      * 没被占用的域名会出现绿色的勾和“Add to cart”的按钮，点击“Add to cart”将域名加入购物车； 
      * 接着点击“Checkout”去付款。由于是免费的，实际上无需付款和添加支付方式;
      * 国家选”China”，手机号填写自己的手机号，其他信息使用大写拼音填写即可，例如Last name(名)填QUANQUAN，First name(姓)填ZHANG，Middle name不需要填，Region(省)、City(城市)、Address(详细地址)也一样用大写拼音填写就可以，ZIP是邮政编码。填好后点击“Save contact”保存；
      * 接下来是确认域名持有人信息，默认是刚才保存的信息，点击“Continue checkout”，订单就完成了；
      * 网站会发两封邮件(一封账号确认邮件，另一封订单确认邮件)，内容都是俄文，不用管，点击里面的链接打开就行了;

到此域名注册已经完成，点击右上角邮箱下拉菜单中的“dashboard”进入管理后台，点击左侧的“domains”就可以看到刚才注册的域名。
免费域名需要激活才使用，接下来介绍激活教程.

##### pp.ua激活教程

管理后台查看域名，刚注册的域名前面有个蓝圈圈，鼠标放上去会有“processing a job. please wait xxxx”的提示。这表示域名尚未激活，因此什么操作都做不了。
正确的做法是等待，一般一天之内会发送激活码到你的手机上(国外的手机号会快一些)，短信以“MRG”开头：
收到短信后，打开 https://apu.drs.ua/en/，依次输入域名、手机号(要加国家代码，例如+86)、短信里给的激活码(8位数字)，点击“Continue”完成激活.
再回到管理后台，域名前面的蓝圈圈变成了绿色的点，鼠标移上去出现“active”的提示。

##### 设置DNS解析

激活域名后，在后台点域名后面的设置按钮，页面往下拉，找到“NS-servers”，选择“NIC.UA nameservers”.
接着点左侧菜单的“Name Servers”，点域名后面的设置按钮，在下方的DNS-recoords中设置DNS解析.
新注册域名有效期都是一年，不能立即续费，可在到期前4个月申请续费，最长可续费10年.
每个账号、手机号一个月内只能激活三个免费域名.

##### 部署v2ray/trogan

1. 申请域名 lyzhaishang.pp.ua, vm带public ip, dns解析域名domain到vm的public ip.
2. 参考以下 申请SSL证书
   ubuntu18.04 安装 nginx: [在Ubuntu 18.04/19.04系统上安装Nginx最新版本的方法](https://ywnz.com/linuxyffq/5148.html)
   ubuntu18.04 使用Certbot：[在Linux上安装letsencrypt的最简单方法](https://ywnz.com/linuxyffq/4483.html)

    ```bash
    sudo snap install core; sudo snap refresh core
    sudo apt-get remove certbot
    sudo snap install --classic certbot
    sudo ln -s /snap/bin/certbot /usr/bin/certbot
    sudo certbot certonly --nginx -d lyzhaishang.pp.ua -d www.lyzhaishang.pp.ua
    ```
3. 部署服务端[v2ray](https://tlanyan.me/v2ray-tutorial/), 部署nginx做[流量伪装](https://tlanyan.me/v2ray-traffic-mask/). 
   目前已在win10上的client验证成功, ubuntu上的client没有验证成.

#### ssh科学上网

使用ssh代理，需要你有一台外部的vps，最好是国外的，能够访问各种所需服务。假设你可ssh连接到vps，如下步骤可建成一个代理服务器：

    ssh -D127.0.0.1:8080 user@host

    使用-D参数绑定监听。上述命令中我们监听的端口是8080.如果你知道-N和-T参数的含义，上述命令可以改为： ssh -NT -D *:8080，这里我们监听所有的来源而不限于本机（127.0.0.1）。通过这样做，可以对外提供服务。

    配置浏览器的代理。我使用的是switchysharp这个插件，在配置里找到socks代理，主机填写127.0.0.1，端口填写刚才使用的8080端口，协议版本选择socks v5.0。

    保存配置，并且启用该配置，就可以看到能够顺利访问外部站点资源了。

ssh代理的原理如下： 用户的请求直接走ssh的通道向远程服务器发起请求。由于ssh是加密连接，内容不能被外部监听，所以只要能连到服务器就有效。而squid之类的代理，首先还是要通过http方式请求服务器，中间路由一看到请求的地址，然后就干掉了。

此代理的限制： 在使用过程中应当保持ssh会话一直连接。由于请求是通过ssh通道传递，所以要保证ssh会话有效。使ssh处于不断线状态可在服务器上做如下配置：vim /etc/ssh/sshd_config，将下面配置启用：

    ClientAliveInterval 60
    ClientAliveCountMax 3    

然后重启sshd服务： service sshd restart.
下次再次连接进来，即可发现会话会一直保持，就可以愉快的上网了。

#### shadowsocks科学上网

部署[ss服务端](https://tlanyan.me/using-shadowsocks-to-fuck-the-gfw/)
```bash
# 1 按装工具shadowsocks
sudo apt-get install shadowsocks

# 2 配置端口, 开启vm的对外端口, 比如8080, 然后完成配置文件
sudo vim ~/shadowsocks.json
```
~/shadowsocks.json内容如下, 参考[指导](https://tlanyan.me/on-fuck-gfw-again/)

    {
         "server":"0.0.0.0",
         "local_address": "127.0.0.1",
         "local_port":1080,
         "port_password": {
             "8080": "123.0000"
         },
         "timeout":300,
         "method":"aes-256-cfb",
         "fast_open": false
    }

```bash
# 3 开启服务
sudo ssserver -c /home/`whoami`/shadowsocks.json --log-file /var/log/shadowsocks -d start
```

部署[ss本地客户端](https://yq.aliyun.com/articles/503030)
```bash
# 1 同样地, 安装shadowsocks
sudo apt-get install shadowsocks

# 2 完成对应的本地配置文件
sudo vim ~/local_shadowsocks.json
```
~/local_shadowsocks.json内容如下,

    {
     "server":"20.46.179.229", # 指向服务端vm的public ip
     "server_port":8080,
     "local_port":1080,
     "password":"123.0000",
     "timeout":300,
     "method":"aes-256-cfb"
    }

```bash
# 3 运行本地sslocal
nohup /usr/bin/sslocal -c ~/local_shadowsocks.json & 即可在后台运行
# 或者直接运行
sslocal -c ~/local_shadowsocks.json
```
最后在chrome浏览器使用Switchysharp插件配置socks代理, SOCKS Host 为 127.0.0.1, port为1080.
除了部署服务端，强烈建议安装bbr模块加快网速