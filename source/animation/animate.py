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

class animate():
    def __init__(self,path=None,name=None,is_global=False):
        self.img_path=path
        self.api_url="ft.tencentcloudapi.com"
        self.filename=name
        self.file=open(self.img_path,'rb')
        image=str(base64.b64encode(self.file.read()))[2:-1]
        self.params={
            "Image":str(image),
            "RspImgType": "base64",
            "DisableGlobalEffect":str(is_global)
        }
        
    def transfer(self):
        cred = credential.Credential(SecretID, SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = self.api_url

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = ft_client.FtClient(cred, "ap-shanghai", clientProfile)

        req = models.FaceCartoonPicRequest()
        req.from_json_string(json.dumps(self.params))
        resp = client.FaceCartoonPic(req).to_json_string()

        # resp = client.TryLipstickPic(req).to_json_string()
        resp=json.loads(resp)['ResultImage']
        result=base64.b64decode(resp)

        with open(self.filename,'wb') as f:
            f.write(result)
        print('complete!')

if __name__=='__main__':
    img_path='img//people//lip1.png'
    store_path='result//animation//example1.jpg'
    operator=animate(img_path,store_path)
    operator.transfer()
