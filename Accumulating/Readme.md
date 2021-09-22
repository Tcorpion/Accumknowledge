Here are some repeated experiments and recordings related to:
```
0. ***** Daily leetcode (in python/c++)



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

1. **** (Review) Metric Learning + Loss Functions + Self-Supervised Learning.
   These three items are combined together for they are always coupled with each other closely.

2. **** (Review) Segmentation
   2.1 Semantic Segmentation
   2.2 Instance Segmentation
       tricks: FPN + IOU Loss 
   2.3 Panoptic Segmentation

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

4. **** (Review) Model Deployment on server

5. *** Face recognition + Land Mark + metric learning

6. *** Transformer
    [reference 1](https://zhuanlan.zhihu.com/p/43493999, https://zhuanlan.zhihu.com/p/44121378)

7. *** RL Introduction

8. *** OCR Application

9. *** NLP
   9.1 (Review) NLP introduction
   9.2 DL based
   9.3 OCR + NLP

10. *** SLAM + 3D 

11. *** Cpp, makefile, cmake, CMakeList.txt, design pattern(in c++/python/java)

12. *** Model lightweight
    11.1 Model deployment on embedding/mobile system
    11.2 Model quantization
    11.3 Model pruning 
    11.4 Model distillation

13. ** DL on Video

14. * DL on Audio

15. *** Daily Reading on Maths books

(The number of `*` represents priority.)
```

The above experiments will **take less than 50% time** compared to repeating on mmdetection/mmsegmentation, since **in 
mmdetection/mmsegmentation more methods and parameters** will be used.

