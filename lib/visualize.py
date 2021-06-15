#encoding=utf-8
"""
This is used for visualization

Created on : 20-12-3
Author     : Yulu Zhang
Version    : 1.0
"""

import cv2
import numpy as np




def draw_img_text(ori_image, text, add_bndbox=False, target_size=260):

  height, width = ori_image.shape[:2]
  img_size = target_size - 6
  resizef = max(height, width) * 1.0 / img_size

  while resizef > 1.8:
    ori_image = cv2.pyrDown(ori_image)
    height, width = ori_image.shape[:2]
    resizef = max(height, width) * 1.0 / img_size

  nh, nw = int(height / resizef), int(width / resizef)
  h_offset, w_offset = (target_size - nh) // 2, (target_size - nw) // 2

  img96 = cv2.resize(ori_image, (nw, nh))

  img = 255 * np.ones((target_size, target_size, 3), dtype=np.uint8)
  img[h_offset : (h_offset + nh), w_offset : (w_offset + nw)] = img96

  font = cv2.FONT_HERSHEY_SIMPLEX
  fontScale = 0.6
  lineType = 1
  thickness = 2
  if add_bndbox:
    cv2.rectangle(
      img, (w_offset, h_offset), (w_offset + nw, h_offset + nh),
      (0, 0, 255), thickness=thickness
    )
  if isinstance(text, str) and len(text) > 0:
    fontColor = (50, 100, 50)
    loc_text = (int(w_offset + 5), int(h_offset + nh - 5))
    cv2.putText(img, text, loc_text, font,
                fontScale, fontColor,
                lineType,
                True)
  return img

