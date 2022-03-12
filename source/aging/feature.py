from email.errors import CharsetError
from hashlib import new
from urllib import response
import requests
import base64
import warnings;
warnings.simplefilter('ignore')

API_Key='iVifz1PCFkrp9sEiZB7_RPlIaJKu9LZZ'
API_Secret='HyKeFP4Yv36N4OfsAaJW0uIPIO1l5nLQ'

def get_feat(img_path,similarity):
    detect_url='https://api-cn.faceplusplus.com/facepp/v3/detect'
    data={'api_key':API_Key,
          'api_secret':API_Secret,
          'image_url':img_path,
          'return_landmark':1}
    file={'image_file':open(img_path,'rb')}
    response=requests.post(detect_url,data=data,files=file)
    res_json=response.json()
    face_rec=res_json["faces"][0]['face_rectangle']
    feat_landmark=res_json["faces"][0]['landmark']
    return face_rec,feat_landmark
