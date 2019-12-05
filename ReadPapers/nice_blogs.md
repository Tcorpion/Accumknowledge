Useful technique

#### How to transform a tensorflow model to tensorRT model
https://devblogs.nvidia.com/tensorrt-integration-speeds-tensorflow-inference/

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

