import numpy as np
import cv2
from numba import jit, prange

# affine operation，用于将贴图点映射到人脸点,得到变换矩阵M
def get_text_trans_matrix(x1, y1, x2, y2, x3, y3, tx1, ty1, tx2, ty2, tx3, ty3):
    '''
    src：原始图像中的三个点的坐标
    dst：变换后的这三个点对应的坐标
    M：根据三个对应点求出的仿射变换矩阵2X3
    '''
    # 放射变换
    return cv2.getAffineTransform( np.float32([ [tx1, ty1], [tx2, ty2], [tx3, ty3] ]), np.float32( [ [x1, y1], [x2, y2], [x3, y3] ]) ).flatten() 
    # 透视变换
    # return cv2.getPerspectiveTransform( np.float32([ [tx1, ty1], [tx2, ty2], [tx3, ty3] ]), np.float32( [ [x1, y1], [x2, y2], [x3, y3] ]) ).flatten()

@jit(nopython=True)
def sticker(srcData, width, height, stride, mask, maskWidth, maskHeight, maskStride, srcFacePoints, maskFacePoints, H):
    def CLIP3(x, a, b):
        return min(max(a,x), b)
    # 用于将贴图点映射到人脸点 
    for i in range(height):
    # for i in prange(height):
        for j in range(width):
            x = float(i)
            y = float(j)
            tx = (int)((H[0] * (x)+H[1] * (y)+H[2]) + 0.5)
            ty = (int)((H[3] * (x)+H[4] * (y)+H[5]) + 0.5)
            tx = CLIP3(tx, 0, maskHeight - 1)
            ty = CLIP3(ty, 0, maskWidth - 1)

            mr = int( mask[ int(tx), int(ty), 0 ] ) 
            mg = int( mask[ int(tx), int(ty), 1 ] ) 
            mb = int( mask[ int(tx), int(ty), 2 ] ) 
            alpha = int( mask[ int(tx), int(ty), 3 ] )  
            #if alpha!=0:
            #    print( '>>>', alpha )
            b = srcData[i, j, 0]
            g = srcData[i, j, 1]
            r = srcData[i, j, 2]        
            srcData[i, j, 0] =CLIP3((b * (255 - alpha) + mb * alpha) / 255, 0, 255)
            srcData[i, j, 1] =CLIP3((g * (255 - alpha) + mg * alpha) / 255, 0, 255)
            srcData[i, j, 2] =CLIP3((r * (255 - alpha) + mr * alpha) / 255, 0, 255)
    return srcData


# @jit(parallel=True,nogil=True)
# @njit(parallel=True,nogil=True)
def trent_sticker(srcData, width, height, stride, mask, maskWidth, maskHeight, maskStride, srcFacePoints, maskFacePoints, ratio):
    ret = 0
    H = get_text_trans_matrix( maskFacePoints[0], maskFacePoints[1],maskFacePoints[2],
                                maskFacePoints[3],maskFacePoints[4],maskFacePoints[5], 
                                srcFacePoints[0], srcFacePoints[1],srcFacePoints[2],
                                srcFacePoints[3],srcFacePoints[4],srcFacePoints[5] )
    srcData = sticker(srcData, width, height, stride, mask, maskWidth, maskHeight, maskStride, srcFacePoints, maskFacePoints, H)
    return srcData, ret 

# config of 15 pictures of opera faces
face_key_point = {
    "01": [ 958.0,599.0, 958.0,1083.0, 1516.0,838.0 ],
    "02": [ 182.0,155.0, 182.0,243.0, 290.0,199.0 ],
    "03": [ 249.0,224.0, 247.0,342.0, 392.0,247.0 ],
    "04": [ 232.0,136.0, 232.0,267.0, 378.0,200.0 ],
    "05": [ 241.0,189.0, 241.0,323.0, 405.0,253.0 ],
    "06": [ 237.0,159.0, 237.0,284.0, 381.0,213.0 ],
    "07": [ 256.0,219.0, 256.0,342.0, 405.0,281.0 ],
    "08": [ 217.0,185.0, 217.0,298.0, 356.0,243.0 ],
    "09": [ 391.0,223.0, 391.0,428.0, 652.0,324.0 ],
    "10": [ 197.0,203.0, 197.0,313.0, 329.0,249.0 ],
    "11": [ 153.0,98.0, 153.0,164.0, 232.0,129.0 ],
    "12": [ 248.0,216.0, 248.0,345.0, 402.0,280.0 ],
    "13": [ 264.0,177.0, 264.0,325.0, 459.0,252.0 ],
    "14": [ 290.0,171.0, 290.0,333.0, 478.0,250.0 ],
    "15": [ 154.0,105.0, 154.0,196.0, 271.0,149.0]
    }