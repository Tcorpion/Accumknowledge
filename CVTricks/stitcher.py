#encoding=utf-8
"""
Stitch two images. 
"""

import os 
import cv2
import copy
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


CUR_DIR = Path(os.path.abspath(__file__)).parent


class Stitcher:

  def __init__(self, ):
      pass 

  def stitch_image_pairs(self, image_pairs, bsize=1024, ratio=0.75, reproj_thresh=4.0):
    """ 
    Args:
      image_pairs: list of image.
      bsize: int
      ratio: A distance ratio to decide whether two feature vector match.
      reproj_thresh: Maximum allowed reprojection error to treat a point pair
                     as an inlier. If the distance between a point's converted
                     result and the dest point is larger than the threshold,
                     this point is considered as an outlier. If the distance
                     is measured in pixels, it usually makes sense to set this
                     parameter somewhere in the range of 1 to 10. The higher value
                     means more error is allowed.
    """
    def resize_for_stitching_homo(img_item, dst_max_size=512):
        if max(img_item.shape) <= dst_max_size:
            return img_item
        img_item = cv2.pyrDown(img_item)
        return resize_for_stitching_homo(img_item)
    
    # Resize original images for fast stitching
    resize_image_set = []
    resizef = 1 #bsize / max(image_pairs[0].shape)
    # for img in image_pairs:
    #     img = resize_for_stitching_homo(img, dst_max_size=bsize)
    #     resize_image_set.append(img)
    # new_img1, new_img2 = resize_image_set
    new_img1, new_img2 = [np.copy(i) for i in image_pairs]

    # Match keypoints ang generate the homography of the pair
    (keypoint1, feature1) = self.detect_and_describe(new_img1, method="SIFT")
    (keypoint2, feature2) = self.detect_and_describe(new_img2, method="SIFT")

    hyperparameters = [
        (r, rt) for r in [ratio, ratio - 0.05, ratio + 0.05] for rt in [reproj_thresh, reproj_thresh + 3, reproj_thresh + 5]
    ]
    candidate_homos = []
    for i, (ratio, reproj_thresh) in enumerate(hyperparameters):
        (_, homography, _) = self.match_keypoints(keypoint2, keypoint1, feature2, feature1,
                                                ratio=ratio, reproj_thresh=reproj_thresh)
        #S = np.array([[1/resizef, 0,          resizef],
        #            [0,         1/resizef,  resizef],
        #            [0,         0,          1]],
        #            dtype=np.float32)
        #homography = np.matmul(S, np.matmul(homography, np.mat(S).I)).A
        candidate_homos.append(homography)

    # rendering
    boxes = self.boxPoints(image=image_pairs[1], homo=homography)
    bbox0 = self.img_bbox(image_pairs[0])[0].astype(np.int32)
    boxes = np.concatenate([boxes, bbox0], axis=0)

    brect = cv2.boundingRect(boxes)
    dsize = brect[2], brect[3]
    offset = np.float32([[1, 0, -brect[0]],
                         [0, 1, -brect[1]],
                         [0, 0, 1]])
    pano = np.zeros((dsize[1], dsize[0], 3), np.uint8)
    
    ihomo = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=np.float32)
    homo1, homo2 = np.dot(offset, ihomo), np.dot(offset, candidate_homos[2])

    img1, img2 = image_pairs
    cv2.warpPerspective(img1, homo1, dsize, pano, cv2.INTER_AREA, cv2.BORDER_TRANSPARENT)
    cv2.warpPerspective(img2, homo2, dsize, pano, cv2.INTER_AREA, cv2.BORDER_TRANSPARENT)
    
    return pano


  def detect_and_describe(self, image, method="SIFT"):
    """ Detect feature points and describe feature in given method.

    Args:
      image: The input image to detect and describe feature points.
      method: Given method for feature extraction.

    Return:
      feature points and feature vectors.
    """
    # Convert the image to grayscale.
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Check to see if we are using OpenCV 3.X.
    # Detect and extract features from the image.
    descriptor = cv2.xfeatures2d.SIFT_create()
    (key_points, features) = descriptor.detectAndCompute(image, None)

    key_points = np.float32([kp.pt for kp in key_points])

    return (key_points, features)


  def match_keypoints(self, key_points1, key_points2,
                      features1, features2, ratio, reproj_thresh):
    """ Match key points using with feature vectors and
        compute homography matrix between two images.

    Args:
      key_points: Coordinates of the raw key points from feature extraction.
      features: Feature vectors from feature extraction and description
      ratio: A distance ratio to decide whether two feature vector match.
      reproj_thresh: Maximum allowed reprojection error to
                     treat a point pair as an inlier.

    Return:
      matched points, homography matrix and the mask for outliers and inliers.
    """
    # Compute the raw matches and initialize the list of actual matches
    matcher = cv2.DescriptorMatcher_create("BruteForce")
    rawMatches = matcher.knnMatch(features1, features2, 2)

    # Loop over the raw matches and find out actual matches.
    matches = []
    for m in rawMatches:
      # Ensure the distance is within a certain distance ratio of each other.
      if len(m) == 2 and m[0].distance < m[1].distance * ratio:
        matches.append((m[0].trainIdx, m[0].queryIdx))

    # Computing a homography requires at least 4 pair of matched points.
    if len(matches) >= 4:
      pts1 = np.float32([key_points1[i] for (_, i) in matches])
      pts2 = np.float32([key_points2[i] for (i, _) in matches])
      mask = None
      # Compute the homography between the two sets of points.
      (homography, mask) = cv2.findHomography(pts1, pts2, cv2.RANSAC, reproj_thresh)
      rectify_stitching = True
      if rectify_stitching:
        mask_n = copy.deepcopy(mask)
        mask_n = mask_n.reshape(-1,) > 0
        npts1, npts2 = pts1[mask_n], pts2[mask_n]
        homography = self.__get_affine_homography(npts1, npts2)
        # homography = cv2.getAffineTransform(npts1, npts2)

      return (matches, homography, mask)

    # Otherwise, no homograpy could be computed
    return None


  def __get_affine_homography(self, pts1, pts2):
    """To get a kind of homograph taking account of points pair
     and horizontal line segment of shelf row.

    Args:
      pts1: array with shape (n, 2)
      pts2: array with shape (n, 2)
      line_segs2: a list of line_seg, each line_seg is [(lx, ly), (rx, ry)]

    Returns:
      h, the homograph matrix.
    """
    aList = []
    for (pt1, pt2) in zip(pts1, pts2):
      p1 = np.matrix([pt1[0], pt1[1], 1])
      p2 = np.matrix([pt2[0], pt2[1], 1])
      a2 = [0,                        0,                        0,
            -p2.item(2) * p1.item(0), -p2.item(2) * p1.item(1), -p2.item(2) * p1.item(2),
            p2.item(1) * p1.item(2)]
      a1 = [-p2.item(2) * p1.item(0), -p2.item(2) * p1.item(1), -p2.item(2) * p1.item(2),
            0,                        0,                        0,
            p2.item(0) * p1.item(2)]
      aList.append(a1)
      aList.append(a2)
    matrixA = np.matrix(aList)

    # svd composition
    u, s, v = np.linalg.svd(matrixA)
    vv = v[6].tolist()[0]
    vv[6:6] = [0, 0]

    # reshape the min singular value into a 3 by 3 matrix
    h = np.reshape(vv, (3, 3))

    # normalize and now we have h
    h = (1 / h.item(8)) * h

    return h

  
  def img_bbox(self, image):
      h, w = image.shape[:2]
      org = np.float32([[(0, 0), (w - 1, 0), (w - 1, h - 1), (0, h - 1)]])
      return org 


  def boxPoints(self, image, homo):
    """ Four convex after preprojection using homo.

    Author: Dmitry

    Args:
      homo: 3 x 3 matrix storing the homography matrix

    Returns:
      Four vertex points after reprojection
    """
    org = self.img_bbox(image)
    return np.round(cv2.perspectiveTransform(org, homo)[0]).astype(int)


def stitch_demo():
    # 使用opencv自带的 stitcher 拼接
    root = str(CUR_DIR / "stitch_imgs")
    img1 = cv2.imread(f"{root}/img_0002.jpg", 1) 
    img2 = cv2.imread(f"{root}/img_0003.jpg", 1) 
 
    # stitcher = cv2.createStitcher(False)    # 老的OpenCV版本，用这一个
    stitcher = cv2.Stitcher.create(cv2.Stitcher_PANORAMA)  # 我的是OpenCV4
 
    (status, pano) = stitcher.stitch((img1, img2))
    if status != cv2.Stitcher_OK:
        print("不能拼接图片, error code = %d" % status)
    else:
        print("拼接成功.")
        plt.imshow(pano[:, :, ::-1])
        plt.show()


def affine_stitch():
    # 参考链接进行拉普拉斯融合： https://blog.csdn.net/qq_45717425/article/details/122638358 
    # 下面的是自己计算homograph拼接
    root = str(CUR_DIR / "stitch_imgs")
    img1 = cv2.imread(f"{root}/img_0002.jpg", 1) 
    img2 = cv2.imread(f"{root}/img_0003.jpg", 1) 
    
    pano = Stitcher().stitch_image_pairs([img1, img2][::-1])
    plt.imshow(pano[:, :, ::-1])
    plt.show()
    


if __name__=="__main__":
    
    affine_stitch()

    stitch_demo()

