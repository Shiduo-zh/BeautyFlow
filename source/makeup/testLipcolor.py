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
from tencentcloud.fmu.v20191213 import fmu_client, models


SecretID="AKIDHPHtEJ8h06wXrugBRRBfsoTs0rSmpb6K"
SecretKey="yg6G9l6AxTjriIbdOs51f3AzYqrb5JGw"

def get_string_to_sign(method, endpoint, params):
    s = method + endpoint + "/?"
    query_str=''
    for k in sorted(params):
        if(k!='LipColorInfos'):
            query_str+='&'+k+'='+str(params[k])
        else:
            query_str+='&'+params[k]
    return s + query_str

def sign_str(key, s, method):
    hmac_str = hmac.new(key.encode("utf8"), s.encode("utf8"), method).digest()
    return base64.b64encode(hmac_str)

def lipinfo_str(lipinfo):
    s=""
    for index in range(len(lipinfo)):
        R="LipColorInfos."+str(index)+".RGBA.R="+str(lipinfo[index]["RGBA"]["R"])
        G="LipColorInfos."+str(index)+".RGBA.R="+str(lipinfo[index]["RGBA"]["G"])
        B="LipColorInfos."+str(index)+".RGBA.R="+str(lipinfo[index]["RGBA"]["B"])
        A="LipColorInfos."+str(index)+".RGBA.R="+str(lipinfo[index]["RGBA"]["A"])
        s=s+R+'&'+G+'&'+B+'&'+A
    return s

class makeup():
    def __init__(self,path=None,lipinfos=None,img_name='result//makeup//result.jpg'):
        self.img_path=path
        self.lipinfos=lipinfos
        self.file=open(self.img_path,'rb')
        image=str(base64.b64encode(self.file.read()))[2:-1]
        
    #     self.params = {
    #     "Image": str(image),
    #     "LipColorInfos": [
    #         {
    #             "RGBA": {
    #                 "R": int(self.lipinfos[0]),
    #                 "G": int(self.lipinfos[1]),
    #                 "B": int(self.lipinfos[2]),
    #                 "A": int(self.lipinfos[3])
    #             }
    #         }
    #     ],
    #     "RspImgType": "base64"
    # }
        self.params={
            "Image": str(image),
            "RspImgType": "base64",
            "LipColorInfos":[
                {
                    "ModelId":lipinfos
                }
            ]
        }
        self.api_url='fmu.tencentcloudapi.com'
        self.name=img_name
    
    def testcolor(self):
       
        
        cred = credential.Credential(SecretID, SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "fmu.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = fmu_client.FmuClient(cred, "ap-shanghai", clientProfile)
        req = models.TryLipstickPicRequest()
        req.from_json_string(json.dumps(self.params))

        resp = client.TryLipstickPic(req).to_json_string()
        resp=json.loads(resp)['ResultImage']
        result=base64.b64decode(resp)

        with open(self.name,'wb') as f:
            f.write(result)
        print('complete!')
    
    def api(self):
        cred = credential.Credential(SecretID, SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "fmu.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = fmu_client.FmuClient(cred, "ap-shanghai", clientProfile)

        req = models.TryLipstickPicRequest()
        params = self.param
        req.from_json_string(json.dumps(params))

        resp = client.TryLipstickPic(req)
        print(resp.to_json_string())

if __name__=='__main__':
    img_path='..//img//people//lip1.png'
    store_path='..//result//makeup//lip2.jpg'
    lipinfos=[{
        "RGBA":{
            "R":230,
            "G":50,
            "B":0,
            "A":50
            }
        }]
    operator=makeup(img_path,lipinfos,store_path)
    operator.testcolor()

