#实现照片的获取的函数
import cv2
def getpic():
    try:
        cam=cv2.VideoCapture(0)
    except:
        print("出错，请连接摄像机设备")
    else:
        success,img=cam.read()
        fn="d://temp.jpg"
        cv2.imwrite(fn, img)


import hashlib
def myhash(x):
    m=hashlib.md5()
    m.update(x.encode("utf-8"))
    q=m.hexdigest()
    y=int(q,16)
    y=y//(10**25)
    return y
#获取百度的API地址的函数
import sys
import json
import base64
import os

IS_PY3 = sys.version_info.major == 3
if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
    from urllib.parse import quote_plus
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
API_KEY = 'zQfhOGYCOuLPwPLckEm7p4P'
SECRET_KEY = 'NKHfW4LB5aZRkdIfEvgoS5KPXfEqnXg'
OCR_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
"""  TOKEN start """
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'
"""
    获取token
"""
def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    if (IS_PY3):
        post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print(err)
    if (IS_PY3):
        result_str = result_str.decode()


    result = json.loads(result_str)

    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not 'brain_all_scope' in result['scope'].split(' '):
            print ('please ensure has check the  ability')
            exit()
        return result['access_token']
    else:
        print ('please overwrite the correct API_KEY and SECRET_KEY')
        exit()


def read_file(image_path):
    f = None
    try:
        f = open(image_path, 'rb')
        return f.read()
    except:
        print('read image file fail')
        return None
    finally:
        if f:
            f.close()

def request(url, data):
    req = Request(url, data.encode('utf-8'))
    has_error = False
    try:
        f = urlopen(req)
        result_str = f.read()
        if (IS_PY3):
            result_str = result_str.decode()
        return result_str
    except  URLError as err:
        print(err)




#获取车牌信息的函数
def get_chepai():

    # 获取access token
    global API_KEY
    global SECRET_KEY
    global OCR_URL
    global TOKEN_URL
    API_KEY = 'zQfhOGYCOuLPwPLBckEm7p4P'
    SECRET_KEY = 'NKHfW4LB5aZRkdmIfEvgoS5KPXfEqnXg'
    OCR_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    """  TOKEN start """
    TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'
    token = fetch_token()

    # 拼接通用文字识别高精度url
    image_url = OCR_URL + "?access_token=" + token
    text = ""

    # 读取测试图片
    file_content = read_file(r'd:\temp.jpg')

    # 调用文字识别服务
    a = base64.b64encode(file_content)
    urlcode = urlencode({'image':a })
    result = request(image_url,urlcode )

    # 解析返回结果
    result_json = json.loads(result)
    for words_result in result_json["words_result"]:
        text = text + words_result["words"]
    #print(text)
    return text




#实现鉴定车的类型来判断是否是超长超高车，通过百度 API进行车辆识别，获取其宽，高和车型
#注意如果图片不完整会报错
import requests
def get_cartype():

    # 获取access token
    global API_KEY
    global SECRET_KEY
    global OCR_URL
    global TOKEN_URL
    API_KEY = '6YoZzlmVrUTKzZaZGa80ykAt'
    SECRET_KEY = 'ejoI6OGQN4s7XpoD27XdXSPTdxcFt9sc'
    OCR_URL = "https://aip.baidubce.com/rest/2.0/image-classify/v1/car"
    """  TOKEN start """
    TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'
    token = fetch_token()
    # 拼接通用文字识别高精度url
    image_url = OCR_URL + "?access_token=" + token
    # 读取测试图片
    file_content = read_file(r'd:\temp.jpg')

    # 调用文字识别服务
    a = base64.b64encode(file_content)
    urlcode = urlencode({'image':a })
    result = request(image_url,urlcode )
    # 解析返回结果
    result_json = json.loads(result)
    w=result_json['location_result']['width']
    h=result_json['location_result']['height']
    car_name=result_json['result'][0]['name']
    #print(w,h,car_name)
    #在摄像头在栏杆处的距离，投射在照片中宽高比大于1是大型车都符合的特征
    if h>0.9*w and h>400:
        print("此车辆为超高超长车辆")
    #print(w,h,car_name)
    return w,h,car_name
   
#实现智能停车场管理系统的系统功能
#要分别实现管理员接口以及车主（使用者）接口
import sqlite3
import datetime
#将每小时价格，停车场停车位数设定一个默认值，每次再从数据库里调取信息
p_ph=0.6 
place=300
#数据库的初始话以及预读取其基本信息
def c_database():
    db=sqlite3.connect("d:/test.db")
    cur=db.cursor()
    cur.execute("create table if not exists cars(id int primary key,y int,m int,d int,h int ,mi int )")
    cur.execute("create table if not exists resident(id int primary key,y int ,m int)")
    cur.execute("create table if not exists parkinglot(id interger primary key,price real,space int,nowcars int)")
    cur.execute("select price,space from parkinglot  ")
    x=cur.fetchone()
    if x!=None:
        global p_ph
        global place
        p_ph,place=x[0],x[1]
    elif x==None:
        cur.execute("insert into parkinglot values(1,0.6,300,0)")
    db.commit()
    db.close()
#向数据库写入入库的车牌信息       
def w_database1(x):
    db=sqlite3.connect("d:/test.db")
    cur=db.cursor()
    nt=datetime.datetime.now()
    y,m,d,h,mi=nt.year,nt.month,nt.day,nt.hour,nt.minute
    cur.execute("select * from cars where id=?",(x,))
    q=cur.fetchone()
    if q==None:
        cur.execute("insert into cars values (?,?,?,?,?,?)",(x,y,m,d,h,mi))
    else:
        cur.execute("update cars set y=?,m=?,d=?,h=?,mi=? where id=?",(y,m,d,h,mi,x))
    db.commit()
    db.close()
#在管理员端写入或更新业主信息   
def w_database2(x,y,m):
    db=sqlite3.connect("d:/test.db")
    cur=db.cursor()
    cur.execute("select * from resident where id=?",(x,))
    q=cur.fetchone()
    if q==None:
        cur.execute("insert into resident values (?,?,?)",(x,y,m))
    else:
        cur.execute("update resident set y=?,m=? where id =?  ",(y,m,x))
    db.commit()
    db.close()
#读取数据库信息并且返回所停的时间和是否为业主车辆    
def get_carinfo(x):
    db=sqlite3.connect("d:/test.db")
    cur=db.cursor()
    hs=0
    isresedent=False
    cur.execute("select * from cars where id=? ",(x,))
    q=cur.fetchone()
    if q==None:
        print("无此车的入库信息")
    else:
        intime=datetime.datetime(q[1],q[2],q[3],q[4],q[5])
        dt=datetime.datetime.now()-intime
        hs=dt.seconds
        hs=hs/3600
        hs=round(hs,2)
        print("停放了",hs,"个小时")
    cur.execute("select y,m from resident where id=? ",(x,))
    p=cur.fetchone()
    if p==None:
        isresedent=False
    else:
        tm=datetime.datetime.now()
        rt=datetime.datetime(p[0], p[1],1)
        delt=rt-tm
        if(delt.days)>0:
            isresedent=True
    return hs,isresedent
#纯纯的交互系统   
def use_model():
    c_database()
    admin=False
    x=input("您是物管管理员吗（输入y）")
    if  x=='y' or x=='Y':
        admin=True
    if admin:
        while(1):
            admin_c=input("按下1选择修改停车场相关的信息，按下2选择修改注册用户车辆信息，按下3退出")
            if admin_c=="3":
                break
            elif admin_c=="1":
                pp,pl=input("输入每小时价格和车位").split()
                db=sqlite3.connect("d:/test.db")
                cur=db.cursor()
                cur.execute("update parkinglot set price=?,space=?",(pp,pl))
                global p_ph
                global place
                p_ph=pp
                place=pl
                db.commit()
                db.close()
            elif admin_c=="2":
                cp=input("输入车牌名")
                cp=myhash(cp)
                #print(cp)
                ye,mo=input("输入会员到期年份和月份").split()
                w_database2(cp,ye,mo)
 
    if not admin:
        ty=input("按1进，按2出")
        if ty=="1":
            db=sqlite3.connect("d:/test.db")
            cur=db.cursor()
            cur.execute("select nowcars,space  from parkinglot")
            nc=cur.fetchone()
            db.close()
            if (nc[1]-nc[0]>0 and nc[1]-nc[0]<10):
                print("车位紧张")
            print("还剩",nc[1]-nc[0],"个位置")
            if nc[0]<nc[1]:
                cc=nc[0]+1
                db=sqlite3.connect("d:/test.db")
                cur=db.cursor()
                cur.execute("update parkinglot set nowcars=?",(cc,))
                db.commit()
                db.close()
                getpic()
                w,h,car_name=get_cartype()
                chepai=get_chepai()
                print("尊敬的"+car_name+"车主"+"\n"+"车牌："+chepai)
                print("入库时间：",datetime.datetime.now())
                chepai=myhash(chepai)
                w_database1(chepai)
            else:
                print("车位不足")
             
        if ty=="2":
            getpic()
            chepai=get_chepai()
            print(chepai)
            chepai=myhash(chepai)
            #print(chepai)
            hs,isresedent=get_carinfo(chepai)
            if isresedent:
                print("尊敬的会员用您无需缴费")
            else:
                print("请缴纳",round(hs*p_ph,2),"元的停车费")
            db=sqlite3.connect("d:/test.db")
            cur=db.cursor()
            cur.execute("select nowcars from parkinglot")
            nc=cur.fetchone()
            cur.execute("update parkinglot set nowcars=?",(nc[0]-1,))
            db.commit()
            db.close()
            
            
while True:
    use_model()
    x=input("是否继续进行，输入y")
    if x=='y' or x=='Y':
        pass
    else:
        break
