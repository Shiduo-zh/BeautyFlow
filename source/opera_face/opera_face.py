import sys


import cv2
import numpy as np
from PIL import Image
from source.opera_face.model import MTCNN
from source.opera_face.utils import *


class opera_face():
    def __init__(self,path,type='01'):
        self.img=path
        self.face_type=type
        self.mtcnn= MTCNN('./pb/mtcnn.pb')
    
    def trans(self):
        """
        face detection and affine transformation
        """
        
        mask_id = self.face_type
        mask_img = Image.open("./img/mask/{}.png".format(mask_id))    
        mask_array = np.array(mask_img) 

        # height and width of opera mask img
        mask_h, mask_w, mask_c = mask_array.shape 

        try:

            openfile_name = self.img
            img = cv2.imread(openfile_name)
            #height and width of uploaded img by users
            h, w, c = img.shape
            bbox, scores, landmarks = self.mtcnn.detect(img)
          
            for box, pts in zip(bbox, landmarks):
                faceInfos = np.array( [ 1, box[1], box[0], box[3] - box[1], box[2] - box[0], pts[5], pts[0], pts[6], pts[1], pts[7], pts[2], pts[8], pts[3], pts[9], pts[4] ] )

            srcFacePoints = np.array( [faceInfos[6], faceInfos[5], faceInfos[8], faceInfos[7], (faceInfos[12]+faceInfos[14])/2.0, (faceInfos[11] + faceInfos[13])/2.0 ] ) 
            #print ('srcFacePoints:', srcFacePoints) 
            maskFacePoints = np.array(face_key_point[mask_id]) 
            #print ('maskFacePoints:', maskFacePoints)
            srcData, ret  = trent_sticker( img, w, h, 3, mask_array, mask_w, mask_h, 4, srcFacePoints, maskFacePoints, 100 ) 
            # print ( 'time >>>>', time.time() - start_time )
            img_mask = np.array(srcData, dtype=np.uint8) 
            # cv2.imwrite('res.jpg', img_mask)
            # bytesPerLine = c * w

            cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)
            self.save_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        except Exception as e:
            print(e)
    
    def download(self,filename):
        """
        download the file to the device(servers in wechat app or mobile app)
        """
        
        filename='./result/opera/'+filename+'.jpg'
        cv2.imwrite(filename,self.save_img)

if __name__=='__main__':
    filepath='./img/tomato.png'
    savename='opera05'
    mask_type="05"
    operator=opera_face(filepath,mask_type)
    operator.trans()
    operator.download(savename)

    
    
        