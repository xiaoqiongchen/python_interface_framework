import requests
import json
from Config import StaticVars
import hashlib
import re
from Util.Log import *

"""
data = json.dumps({'userid': 4, "token": "89f288757f4d0693c99b007855fc075e", 'articleId': 4, 'title': 'about port', 'content': 'code code'}) #
r = requests.put('http://39.106.41.11:8080/update/', data = data)

r = requests.get('http://39.106.41.11:8080/getBlogContent/' + str(articleId))
"""

def api_request(url,request_method,request_content):
    #此函数封装了get请求、post和put请求的方法
    headers = {'content-type':'application/json'}
    if request_method=="get":
        try:
            if isinstance(request_content,dict):
                info("请求的接口地址是：%s" %url)
                info("请求的数据是：%s" %request_content)
                r=requests.get(url, params=request_content,headers=headers)
            else:
                r=requests.get(url+str(request_content),headers=headers)
                info("请求的接口地址是：%s" % r.url)
                info("请求的数据是：%s" % request_content)

        except Exception as e:
            info("get 方法请求发生异常：请求的 url 是 %s,请求的内容是%s\n发生的异常信息如下：%s" %(url,request_content,e))
            r = None
        return r
    elif request_method=="post":
        try:
            if isinstance(request_content,dict):
                info("请求的接口地址是：%s" %url)
                info("请求的数据是：%s" %json.dumps(request_content))
                r = requests.post(url, data=json.dumps(request_content),headers=headers)
            else:
                raise ValueError
        except ValueError as e:
            info("post 方法请求发生异常：请求的 url 是 %s,请求的内容是%s\n发生的异常信息如下：%s" % (url, request_content, "请求参数不是字典类型"))
            r = None
        except Exception as e:
            info("post 方法请求发生异常：请求的 url 是 %s,请求的内容是%s\n发生的异常信息如下：%s" %(url,request_content,e))
            r= None
        return r
    elif request_method=="put":
        try:
            if isinstance(request_content,dict):
                info("请求的接口地址是：%s" %url)
                info("请求的数据是：%s" %json.dumps(request_content))
                r = requests.put(url, data=json.dumps(request_content),headers=headers)
            else:
                raise ValueError
        except ValueError as e:
            info("put 方法请求发生异常：请求的 url 是 %s,请求的内容是%s\n发生的异常信息如下：%s" % (url, request_content, "请求参数不是字典类型"))
            r = None
        except Exception as e:
            info("put 方法请求发生异常：请求的 url 是 %s,请求的内容是%s\n发生的异常信息如下：%s" %(url,request_content,e))
            r= None
        return r

if __name__ == "__main__":
    username = "wulaoshi"+str(StaticVars.get_unique_number_value("unique_num1"))
    r=api_request("http://39.106.41.11:8080/register/","post",{"username":username, "password":"123456789abc","email":"sed@qq.com"})
    if r is not None:
        print(r.text)
        userid = int(re.search(r'userid": (\d+)', r.text).group(1))
    else:
        print("注册请求发生异常")

    m5 = hashlib.md5()
    m5.update('123456789abc'.encode("utf-8"))
    pwd = m5.hexdigest()
    print(pwd)

    r = api_request("http://39.106.41.11:8080/login/", "post",
                    {"username": username, "password": pwd})
    if r is not None:
        print(r.text)
    else:
        print("登录请求发生异常")

    token = re.search(r'token": "(\w+)',r.text).group(1)
    print(token)

    r = api_request("http://39.106.41.11:8080/create/", "post",
                    {'userid': userid, 'token': token, 'title': "mysql ",
                     'content': 'mysql learn'})
    if r is not None:
        print(r.text)
    else:
        print("发布博客请求发生异常")

    r = api_request("http://39.106.41.11:8080/getBlogsOfUser/", "post",
                    {'userid': userid, 'token': token})
    print({"userid": userid, "token": token})
    if r is not None:
        print(r.text)
    else:
        print("获取所有博客的内容请求发生异常")

    articleId = re.search(r'articleId": (\d+)', r.text).group(1)
    print(articleId)

    r = api_request("http://39.106.41.11:8080/getBlogContent/","get",articleId)
    if r is not None:
        print(r.text)
    else:
        print("获取单篇博客内容请求发生异常")
    assert "mysql learn" in r.text

