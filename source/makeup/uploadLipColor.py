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

def upload2cloud(img_path):
    file=open(img_path,'rb')
    image=str(base64.b64encode(file.read()))[2:-1]
    cred = credential.Credential(SecretID, SecretKey)
    httpProfile = HttpProfile()
    httpProfile.endpoint = "fmu.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = fmu_client.FmuClient(cred, "ap-shanghai", clientProfile)

    req = models.CreateModelRequest()
    params = {
        "LUTFile": image
    }
    req.from_json_string(json.dumps(params))

    resp = client.CreateModel(req).to_json_string()
    modelid=json.load(resp)['ModelId']
    return modelid

if __name__=='__main__':
    import sys,os
    
    ids=dict()
    path='..//..//img//colorcard'
    dir=os.listdir(path)
    for file in dir:
        ids[file]=upload2cloud(path+'//'+file)
    with open('color//models.txt','wb') as f:
        for (name,id) in zip(ids.keys(),ids.values()):
            f.write(name+':'+id+'\n')

           
