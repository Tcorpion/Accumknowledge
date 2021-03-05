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
1. Yolo v3, 网络结构+loss解析，参考[代码](https://github.com/DeNA/PyTorch_YOLOv3) 和博客[讲解](https://blog.csdn.net/wqwqqwqw1231/article/details/90667046)
   以及[知乎文](https://zhuanlan.zhihu.com/p/143747206).
2. [Comparision between Yolo v5 and v4](https://zhuanlan.zhihu.com/p/161083602), [details about v4](https://zhuanlan.zhihu.com/p/136172670) 
3. [Box regression loss revisiting](https://zhuanlan.zhihu.com/p/104236411): Ln (l2, l1) loss -> Smooth l1 loss -> IOU loss
   IoU Loss -> GIoU Loss -> DIoU Loss -> CIoU Loss
4. PANet refers to [here](https://zhuanlan.zhihu.com/p/63548148)

