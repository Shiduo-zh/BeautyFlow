from email.errors import CharsetError
from hashlib import new
from urllib import response
import requests
import base64
import warnings;
warnings.simplefilter('ignore')

API_Key='iVifz1PCFkrp9sEiZB7_RPlIaJKu9LZZ'
API_Secret='HyKeFP4Yv36N4OfsAaJW0uIPIO1l5nLQ'

class face_change():
    def __init__(self,similar=99,path1=None,path2=None,img_name='result//merge.jpg'):
        self.img_path=path1
        self.target_path=path2
        self.detect_url='https://api-cn.faceplusplus.com/facepp/v3/detect'
        self.merge_url= "https://api-cn.faceplusplus.com/imagepp/v1/mergeface"
        self.data={ 'api_key':API_Key,
                    'api_secret':API_Secret,
                    'image_url':self.img_path,
                    'return_landmark':1}
        self.similarity=similar
        self.name=img_name
    
    #uploaded img by user
    def set_origin_path(self,newpath):
        self.img_path=newpath

    #target img style file path
    def set_target_path(self,newpath):
        self.target_path=newpath
    
    def find_face_feat(self,img_path):
        files={'image_file':open(img_path,'rb')}
        response=requests.post(self.detect_url,data=self.data,files=files)
        res_json=response.json()
        face_feat=res_json["faces"][0]['face_rectangle']
        return face_feat
    
    def change_face(self):
        origin_feat=self.find_face_feat(self.img_path)
        target_feat=self.find_face_feat(self.target_path)

        #4 params of a face shape,including height,width and position
        origin_face_rec=str(  str(origin_feat['top']) + ',' 
                            + str(origin_feat['left']) + ',' 
                            + str(origin_feat['width']) + ',' 
                            + str(origin_feat['height']))
        target_face_rec=str(  str(target_feat['top']) + ',' 
                            + str(target_feat['left']) + ',' 
                            + str(target_feat['width']) + ',' 
                            + str(target_feat['height']))
        
        ori_img=open(self.img_path,'rb')
        ori_img_base=base64.b64encode(ori_img.read())
        ori_img.close()

        tar_img=open(self.target_path,'rb')
        tar_img_base=base64.b64encode(tar_img.read())

        data = {'api_key': API_Key, 
                'api_secret': API_Secret, 
                'template_base64': ori_img_base,
                'template_rectangle': origin_face_rec, 
                'merge_base64': tar_img_base, 
                'merge_rectangele': target_face_rec,
                'merge_rate': self.similarity} 
        
        response=requests.post(self.merge_url,data=data).json()
        results=response['result']
        image=base64.b64decode(results)

        with open(self.name,'wb') as f:
            f.write(image)
        print("complete!")

if __name__=='__main__':
    file1='img//老番茄.jpeg'
    file2='img//夏洛克.jpeg'
    result_name='result//result1.jpg'
    operator=face_change(99,file1,file2,result_name)
    operator.change_face()


        
        
