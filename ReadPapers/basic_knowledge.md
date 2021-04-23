### CVML knowledge
边读边写，把掌握的cvml内容再次描述出来，以达到:
1. 以一种友好的方式, 让不知道这些内容的人也能理解;
2. 在社区交流自己的心得以及使用技巧, 欢迎在issue里面提出指正和更多意见;
3. 作为知识备忘小本本, 方便自己快速回忆以前的理解过的、用过的内容.

罗列的有点多，一点点垒，有些是个人使用体会, 有些还在学习中.

### Model training optimizer 
1. [从SGD, SGDM, 到Adam: 一个框架看懂优化算法之异同 SGD/AdaGrad/Adam](https://zhuanlan.zhihu.com/p/32230623)
2. [Adam那么棒，为什么还对SGD念念不忘 (2)—— Adam的两宗罪](https://zhuanlan.zhihu.com/p/32262540)
3. [LRN Local response normalization](https://blog.csdn.net/hduxiejun/article/details/70570086)
    * LRN全称为Local Response Normalization，即局部响应归一化层，LRN函数类似DROPOUT和数据增强作为relu激励之后防止数据过拟合而提出的一种处
    理方法。这个函数很少使用，基本上被类似DROPOUT这样的方法取代，见最早的出处AlexNet论文对它的定义, 《ImageNet Classification with Deep
     ConvolutionalNeural Networks》
    * tensorflow官方文档中的tf.nn.lrn函数给出了局部响应归一化的论文出处，
    [详见](http://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks) 
    * 为什么要有局部响应归一化（Local Response Normalization)? [详见](http://blog.csdn.net/hduxiejun/article/details/70570086)
    * Given location (c, x, y) of feature map F, enlarge the higher value and reduce lower value among different feature
    maps at location (x, y).
 4. Batch normalization. For each batch calculation, get the **mean value** and **variance**, record them, then get 
    x_n = (x-u) / deta as normalization value for purposes like accelerating convergence, [avoiding zero gradient, 
    infinite gradient](https://zhuanlan.zhihu.com/p/180568816), and avoiding overfitting, then linearly move x_n to 
    (x_n * t + b), here t and b are model parameters of bn layer.

### Detection

#### Metrics
先说说detection中用到的那些评价指标。在实践中应用中，我们感知到的是:
```
a. 这个目标检测到了，定位中心刚刚好或者略有偏差，检测框大小合适
b. 那个目标好像漏检了，没有被框住
c. 还有几个目标检测得有点不准确, 有的定位偏向一侧，有的检测框尺寸过大，有的过小
d. 检测一张图好快， 只花了120ms
e. 显存占用好多，
```
这些直接感知，对应的度量指标metrics中,有这么一些: `IOU, Precision, Recall, FPS`, 这些metrics中，前者的计算直接跟detections检测框的坐标+score
和groundtruth boundingbox有关，后两者依赖于IOU和score, 它们的中间计算结果是`TP, FN, FP`， Precision = TP / (TP + FP), 
Recall = TP / (TP + FN)。FPS比较直观， frame per second.

检测模型通常输出的detections能达到数量级30k ~ 100k， 这些detections的scores分布多样化，这些输出依赖于模型参数设置和检测数据，比如候选anchors数量、
feature map的大小， (FPN)feature level层数、待检测图像中目标密集程度、检测inference中截断score阈值、检测inference中输出截断个数。在使用
模型时，前面提到的这些因素是可以进行超参数设置，同样的模型经过训练后在inference阶段使用不同超参数可以得到不同的precision和recall(各位调参虾的表演不尽相同)。
为了全面对比模型好坏，学界提出F1, AP50, AP75, mAP[50-95], AR50. AR75, mAR[50-95]，详细可以参考
[这些知乎软文](https://zhuanlan.zhihu.com/p/107989173?from_voters_page=true), 还有
[github Metrics 介绍](https://github.com/rafaelpadilla/Object-Detection-Metrics)

需要说明的是，论文通常宣称达到SOTA mAP, SOTA AP50 或者 AP75，在比较和使用时，需要观察前面提及的那些超参数论文设置的多少，**每个模型在不同超参数
下可以得到有高有低的mAP, AP50和AP75，把这些考虑进来非常重要。**

1. Yolo v3, 网络结构+loss解析，参考[代码](https://github.com/DeNA/PyTorch_YOLOv3) 和博客[讲解](https://blog.csdn.net/wqwqqwqw1231/article/details/90667046)
   以及[知乎文](https://zhuanlan.zhihu.com/p/143747206).
2. [Comparision between Yolo v5 and v4](https://zhuanlan.zhihu.com/p/161083602), [details about v4](https://zhuanlan.zhihu.com/p/136172670) 
3. [Box regression loss revisiting](https://zhuanlan.zhihu.com/p/104236411): Ln (l2, l1) loss -> Smooth l1 loss -> IOU loss
   IoU Loss -> GIoU Loss -> DIoU Loss -> CIoU Loss
4. PANet refers to [here](https://zhuanlan.zhihu.com/p/63548148)

#### Anchor Based
Anchor源自faster-rcnn，目的是为了是proposal更高效更准，预设anchor比selective搞出proposal要高效一大截,虽然预设的anchor绝大多数都是negative
背景范围，真正属于positive前景目标的anchor只占很少比例，但是采取其他手段(按规则过滤negative anchors, 只使用三倍正样本量)照样可以正常训练。

针对特定数据领域，anchor可以针对性设计aspect ratio，size，甚至旋转角度。有一大票从anchor角度出发搞事情涨点的tricks论文,罗列如下:
xxx
xxx
xxx
(待我一一收集过来)

#### Anchor free

#### Two stage detection

#### One stage detection

#### Multi-resolution (FPN)

#### Loss function

### Pose estimation

### Segmentation

#### Semantic segmentation

#### Instance segmentaion

### Attention
视觉中的注意力机制，是模仿人类观察图像时，专注于重要局部细节，摈弃无关内容。
在CNN中，有两类方法：
1. spatial-wise. CNN中某一卷积特征大小 H*W, 这个范围内只有部分区域的特征对后续的任务(识别、检测、分割)起明显作用，特别是细粒度分类中一些特别局
部的特征，由此可以使用一个 H*W 大小的权重因子，逐个像素赋予一个权重，重要的空间位置给一个大权重，无关紧要的空间位置给一个近似0的权重，使模型忽略不
太重要的区域，重点关注更有意义的特征。
典型例子，`Squeeze-and-Excitation Networks. Jie Hu, Li Shen, Samuel Albanie, Gang Sun, Enhua Wu. (CVPR 2018)`, 在attention
分支中，通过channel-wise max pooling和mean pooling得到 H*W*2 的权重隐变量，再经过1*1卷积, softmax非线性映射, 学习得到取值[0, 1]范围的
spatial-wise weights。

2. channel-wise. CNN中卷积特征的通道数是人为指定，各个通道之间同样有三六九等之分，重要的通道(相对后续任务来说)应该收到更多的关注，那么类似于spatial-wise
给各个通道一个单独的权重，可以让模型着重关注有意义的通道特征。
典型例子，`CBAM: Convolutional Block Attention Module. Sanghyun Woo, Jongchan Park, Joon-Young Lee, In So Kweon.(ECCV, 2018)`
在channel-wise attention分支中，通过spatial-wise pooling得到 1*1*C 的权重隐变量，再经过两个MLP或是1*1卷积进一步学习得到channel-wise weights

上面这两种attention从不同角度出发，当然可以组合在一起使用. 比如2中的`CBMA`.

Tips, 细细一品，不管是spatial-wise还是channel-wise的attention,和dropout似乎有异曲同工之妙，不同之处在于，attention使用起来可以把赋权
(pixel-wise multiplication)后的特征灵活应用, 
比如, `Wang, Fei, et al. "Residual attentionnetwork for image classification." arXiv preprint arXiv:1704.06904` 计算残差，
raw feature + attention feature, 其次attention是学出来的，而dropout是超参数预设置.

### Self-supervised Learning

### Metric learning

### Fine-grained classification

### Reinforcement learning
