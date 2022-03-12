from flask import Flask
from flask import request

from source.face_change import face_change
from source.opera_face.opera_face import opera_face
from source.makeup.testLipcolor import makeup
from source.animation.animate import animate
from source.aging.tencentapi import aging
from source.gender_change.gender_change import gender_change

app=Flask(__name__)

@app.route('/',methods=['/GET','/POST'])
def hello_world():
    return 'hello'


@app.route('/profile')
def get_porfile():
    return dict(id='1234',password='1234')

@app.route('/facechange')
def get_changeface():
    #abspath='D://学期文件夹//大三下//AI换脸项目//selective//'
    path1=request.args.get('path1','')
    path2=request.args.get("path2",'')
    img_name=request.args.get("imgname",'')
    operator=face_change(path1=path1,path2=path2,img_name=img_name)
    operator.change_face()
    return dict(path1=path1,path2=path2,result=img_name,state='success')

@app.route('/operaface')
def get_operaface():
    path=request.args.get('path','')
    name=request.args.get('name','')
    type=request.args.get('type','')
    operator=opera_face(path,type)
    operator.trans()
    operator.download(name)
    return dict(path=path,filename=name,masktype=type)

@app.route('/makeup')
def get_makeup():
    path=request.args.get('path','')
    name=request.args.get('name','')
    lipinfo=request.args.get('lipinfo','')
    operator=makeup(path,lipinfo,name)
    operator.testcolor()

    return dict(path=path,filename=name,lipinfo=lipinfo)

@app.route('/animate')
def get_animation():
    path=request.args.get('path','')
    name=request.args.get('name','')
    operator=animate(path,name)
    operator.transfer()

    return dict(path=path,name=name)

@app.route('/aging')
def get_aging():
    path=request.args.get('path','')
    name=request.args.get('name','')
    ageinfo=request.args.get('ageinfo','')
    operator=aging(path,name,ageinfo)
    operator.transfer()

    return dict(path=path,name=name,age=ageinfo)

@app.route('/gender')
def get_genderchange():
    path=request.args.get('path','')
    name=request.args.get('name','')
    operator=gender_change(path,name)
    operator.transfer()

    return dict(path=path,name=name)
