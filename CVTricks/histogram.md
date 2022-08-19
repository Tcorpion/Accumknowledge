### 2D-histogram 
形如数据size = (n, 2) 的 np.array, 2D-histogram结果是一个类似灰度图
```Python
import matplotlib.pyplot as plt

def get_2d_histogram(datas):
    """
    Args:
        datas (np.array), with shape (n, 2)
    
    Return:
        H, 
        xedges, 
        yedges
    """
    bins_x = 10 
    bins_y = 20
    H, xedges, yedges = np.histogram2d(datas[:, 0], datas[:, 1], (bins_x, bins_y))
    # H = cv2.rotate(H, cv2.ROTATE_180)
    print(H.shape, type(H))
    plt.figure(figsize=(10, 5))
    plt.imshow(H)
    plt.colorbar() 
    plt.show()
```
