import requests
import numpy as np
import base64
import time
import random
import hashlib
import hmac
import json
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.ft.v20200304 import ft_client, models

SecretID="AKIDHPHtEJ8h06wXrugBRRBfsoTs0rSmpb6K"
SecretKey="yg6G9l6AxTjriIbdOs51f3AzYqrb5JGw"

API_Key='iVifz1PCFkrp9sEiZB7_RPlIaJKu9LZZ'
API_Secret='HyKeFP4Yv36N4OfsAaJW0uIPIO1l5nLQ'

class gender_change():
    def __init__(self,path=None,name=None):
        self.img_path=path
        self.api_url="ft.tencentcloudapi.com"
        self.detect_url='https://api-cn.faceplusplus.com/facepp/v3/detect'
        self.filename=name
        self.file=open(self.img_path,'rb')
        self.gender=self.judge_gender()
        image=str(base64.b64encode(self.file.read()))[2:-1]
        self.params={
            "Image":str(image),
            "RspImgType": "base64",
            "GenderInfos": [
            {
                "Gender": self.gender
            }
        ]
        }
    
    def judge_gender(self):
        data={ 'api_key':API_Key,
               'api_secret':API_Secret,
               'image_url':self.img_path,
               'return_attributes':'gender'}
        files={'image_file':self.file}
        response=requests.post(self.detect_url,data=data,files=files)
        res_json=response.json()
        gender=res_json["faces"][0]['attributes']['gender']
        if(gender=='Male'):
            return 0
        else:
            return 1


    def transfer(self):
        cred = credential.Credential(SecretID, SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = self.api_url

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = ft_client.FtClient(cred, "ap-shanghai", clientProfile)

        req = models.SwapGenderPicRequest()
        req.from_json_string(json.dumps(self.params))
        resp = client.SwapGenderPic(req).to_json_string()

        # resp = client.TryLipstickPic(req).to_json_string()
        resp=json.loads(resp)['ResultImage']
        result=base64.b64decode(resp)

        with open(self.filename,'wb') as f:
            f.write(result)
        print('complete!')

if __name__=='__main__':
    img_path='img//people//lip1.png'
    store_path='result//gender//example1.jpg'
    operator=gender_change(img_path,store_path)
    operator.transfer()

