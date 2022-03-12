import json
import base64
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.fmu.v20191213 import fmu_client, models

SecretID="AKIDHPHtEJ8h06wXrugBRRBfsoTs0rSmpb6K"
SecretKey="yg6G9l6AxTjriIbdOs51f3AzYqrb5JGw"

try:
    cred = credential.Credential(SecretID, SecretKey)
    httpProfile = HttpProfile()
    httpProfile.endpoint = "fmu.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = fmu_client.FmuClient(cred, "ap-shanghai", clientProfile)
    
    file=open("img//people//lip1.png",'rb')
    image=base64.b64encode(file.read())
    image_str=str(image)
    image_str=image_str[2:-1]
    req = models.TryLipstickPicRequest()
    params = {
        "Image": str(image_str),
        "LipColorInfos": [
            {
                "RGBA": {
                    "R": 230,
                    "G": 50,
                    "B": 0,
                    "A": 50
                }
            }
        ],
        "RspImgType": "base64"
    }
    req.from_json_string(json.dumps(params))

    resp = client.TryLipstickPic(req).to_json_string()
    resp=json.loads(resp)['ResultImage']
    result=base64.b64decode(resp)

    store_path='result//makeup//lip1.jpg'
    with open(store_path,'wb') as f:
        f.write(result)
    print('complete!')


except TencentCloudSDKException as err:
    print(err)