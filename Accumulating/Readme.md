Here are some repeated experiments and recordings related to:
```
0. ***** Daily leetcode (in python/c++)
  0.1 高频题, 好人开发整理: https://codetop.cc/home
  0.2 个人总结, 写在本子上了，呃呃呃


0. ***** Fine-Grained Recognition
   Large intra-class distance and small inter-class distance. CVPR-2021 tutorial 
[Fine-Grained Visual Analysis with Deep Learning](https://fgva-cvpr21.github.io/)
provides a nice guide for engineers.

   0.1 Detect/segmente before recognition to get the informative crops, then classify the
       crops to get fine-grained category. This is to add attention by mannul operations.
   0.2 Add attention module to crop informative parts during training, like [TASN](Looking 
       for the Devil in the Details: Learning Trilinear Attention Sampling Network for Fine-grained 
       Image Recognition) and [MMAL-Net](Multi-branch and Multi-scale Attention Learning for Fine-Grained 
       Visual Categorization). Note that attention module brings low batch-size since more GPU-memory is 
       used, it could reduce the advantage and sometimes even brings worse accuracy.
   0.3 Clean dirty labeling in training set based on confusion matrix. Anyway, the non-matched predictions 
       in training set must be relabeled.
   0.4 Adopt activelearning by adding low score predictions epecially wrong predictions. Usually, adding 
       training set is useful. However, when training set size grows larger, the accuracy-curve grows up 
       slow and its gradient tends to zero, directly adding more data is inefficient. An efficient method
       is to add low score predictions, including wrong predictions. The term "low score" is at the inverse
       side to high score predictions like 0.9, 0.95 and 0.999. The theshold of low score may be 0.5 or 0.3,
       it is a hyper-parameter. Anyway, the wrong predictions must be relabeled and added to training.   
   0.5 Make the training set balance. 
       0.5.1 If there are enough images for each category, that means the total number of each class is more 
       than a few handruds, the recommended method is to split the classes of higher total numbers and train 
       multiple models, then assemble these models in inference by averaging scores from all models. 
       0.5.2 If some classes have few samples, try focal loss.
   0.6 Posible solution of fine-grained recognition for super-huge number of images, as HUAWEI team said in a 
       interview, embedding based retrieval is the most efficient and effective method, besides, the embedding
       training should be implemented on a balanced dataset.

1. **** (Review) Metric Learning + Loss Functions + Self-Supervised Learning.
   These three items are combined together for they are always coupled with each other closely.

2. **** (Review) Segmentation
   2.1 Semantic Segmentation
   2.2 Instance Segmentation
       tricks: FPN + IOU Loss 
   2.3 Panoptic Segmentation
   2.4 Deconv to the original size of input image(For example, the upsampling in Adalsn)
       The disadvantage of deconv: [Deconvolution and Checkerboard Artifacts](https://distill.pub/2016/deconv-checkerboard/)
       Using deconvolution makes Heavy checkerboard artifacts.
       Using resize-convolution makes No checkerboard artifacts.

3. **** (Review) Detection + Fine-Grained Recognition
   3.1 Anchor Based
       3.1.1 One Stage
       3.1.2 Two Stage
   3.2 Anchor Free
       3.2.1 One Stage
       3.2.2 Two Stage
   3.3 Orientated Bounding box
       3.3.1 [e2cnn, E(2)-Equivariant CNNs] (https://github.com/QUVA-Lab/e2cnn)
       3.3.2 [Official code of the paper "ReDet: A Rotation-equivariant Detector for Aerial Object Detection" (CVPR 2021)] (https://github.com/csuhan/ReDet)
   3.4 Tricks
       3.4.1 Soft-NMS to avoid removing true positive boxes by IOU threshold
   3.5 KeyPoints Detection, MMPose
   3.6 Skeleton Detection

4. **** (Review) Model Deployment on server

5. *** Face recognition + Land Mark + metric learning

6. *** Transformer
    [reference 1](https://zhuanlan.zhihu.com/p/43493999, https://zhuanlan.zhihu.com/p/44121378)

7. *** RL Introduction

8. *** OCR Application 
   8.1 [Engineering sharing of OCR](https://zhuanlan.zhihu.com/p/368035566)  

9. *** NLP
   9.1 (Review) NLP introduction
   9.2 DL based
   9.3 OCR + NLP

10. *** SLAM + 3D 
  10.1 Eigen C++ lib for matrics:  https://eigen.tuxfamily.org/index.php?title=Main_Page 

11. *** Cpp, makefile, cmake, CMakeList.txt, design pattern(in c++/python/java)
  11.1 VS CODE 官方文档, 支持多种coding语言 https://code.visualstudio.com/docs 
      11.1.1 vscode默认outline显示函数内部变量，很丑，设置不显示内部变量: https://blog.csdn.net/Zjhao666/article/details/120523879 
             只需要ctrl+shift+p，修改setting.json的outline.showVariables的默认设置，为false就行了。

  11.2 C/C++标准库， C/C++标准库到底是什么？ https://blog.csdn.net/lbw520/article/details/104585775
  11.3 标准库简介， 标准库简介—C++学习 https://blog.csdn.net/weixin_51958878/article/details/116010182
  11.4 linux下g++、make、cmake编译工具代码实例 https://blog.csdn.net/qq_39975542/article/details/124318369
  11.5 ***** cmake 如何入门 知乎回答 https://www.zhihu.com/question/58949190 和里面提到的 https://github.com/ttroy50/cmake-examples 
            c语言程序的编译过程: 预处理(宏替换、头文件插入等) -> 编译(生成优化后的汇编代码) -> 汇编(生成机器码) -> 连接()
            
            """
            预处理: 预处理阶段其实就是将源文件进行完全展开，删除不必要的项，增加必要的项。一般包含:
            （1）将所有的#define删除，并且展开所有的宏定义。说白了就是字符替换
            （2）处理所有的条件编译指令，#ifdef #ifndef #endif等，就是带#的那些
            （3）处理#include，将#include指向的文件插入到该行处，展开头文件
            （4）删除所有注释
            （5）添加行号和文件标示，这样的在调试和编译出错的时候才知道是是哪个文件的哪一行
            （6）保留#pragma编译器指令：其他以#开拓的都是预编译指令，但是这个指令例外，此为编译器指示字，所以此步骤需要保留，关于此指示字的具体用法，在后面的内容将会详细讲解。

            编译: 编译就是将 高级语言 翻译为 汇编语言的过程。并且在该过程中相关优化代码。编译过程一般包含:
            （1）词法分析;（2）语法分析;（3）语义分析;（4）源代码优化;（5）目标代码生成;（6）目标代码优化

            汇编: 汇编将 汇编语言 转变成 机器语言，生成目标文件。每一个汇编语句几乎都对应一条机器指令。根据汇编指令和机器指令的对照表一一翻译即可。
             目标文件由段组成。通常一个目标文件中至少有两个段: 
             代码段, 该段中所包含的主要是程序的指令。该段一般是可读和可执行的，但一般却不可写; 
             数据段,主要存放程序中要用到的各种全局变量或静态的数据。一般数据段都是可读，可写，可执行的。

            连接: 最后的连接阶段，将所有的 目标文件 和 需要的库连接，生成可执行文件。链接分为静态链接和动态链接。
            """
  

12. *** Model lightweight
    12.1 Model deployment on embedding/mobile system
    12.2 Model quantization
    12.3 Model pruning 
    12.4 Model distillation

13. ** DL on Video

14. * DL on Audio

15. *** Daily Reading on Maths books

(The number of `*` represents priority.)
```

The above experiments will **take less than 50% time** compared to repeating on mmdetection/mmsegmentation, since **in 
mmdetection/mmsegmentation more methods and parameters** will be used.

