---
title: python上传APK至fir.im
date: 2018-08-18 23:26:19
categories: python3
tags: fir
---



# Fir文档
发布应用操作分两步，

* 获取上传凭证
* 上传文件

## 获取上传凭证

### API

**发布应用获取上传凭证**

> **POST** [http://api.fir.im/apps](javascript:void(0))

### 参数列表

| 名称      | 类型   | 必填 | 说明                                 |
| --------- | ------ | ---- | ------------------------------------ |
| type      | String | 是   | ios 或者 android（发布新应用时必填） |
| bundle_id | String | 是   | App 的 bundleId（发布新应用时必填）  |
| api_token | String | 是   | 长度为 32, 用户在 fir 的 api_token   |


## 上传文件

### API

将 ICON 和安装包文件分别上传到上一步操作中获取到的 `cert.icon` 和 `cert.binary` 中的 `upload_url`

> **POST** upload_url

### 参数列表

| 名称           | 类型   | 必填 | 说明                                                        |
| -------------- | ------ | ---- | ----------------------------------------------------------- |
| key            | String | 是   | 七牛上传 key                                                |
| token          | String | 是   | 七牛上传 token                                              |
| file           | File   | 是   | 安装包文件                                                  |
| x:name         | String | 是   | 应用名称（上传 ICON 时不需要）                              |
| x:version      | String | 是   | 版本号（上传 ICON 时不需要）                                |
| x:build        | String | 是   | Build 号（上传 ICON 时不需要）                              |
| x:release_type | String | 否   | 打包类型，只针对 iOS (Adhoc, Inhouse)（上传 ICON 时不需要） |
| x:changelog    | String | 否   | 更新日志（上传 ICON 时不需要）                              |


# Python3脚本
```
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import json
import os
import sys

split = '-' * 20

proxies = {
    'http': '127.0.0.1:8899',
    'https': '127.0.0.1:8899',
}


def print_split(s):
    print(split + '[ ' + s + ' ]' + split)


# 必填项，可以通过命令行参数传入

# fir 的token 和包信息
APP_INFO = {
    'api_token': '04d3c6e1dc9b65977be388be3801asfdafsdasfd7',
    'applicationId': 'com.xxx.yyy',
    'versionName': '1.2.3',
    'versionCode': '90',
    'changelog': '暂无提交log'
}


# 必填项，可以通过命令行参数传入

def init_app_info():
    if len(sys.argv) > 1:
        print_split('获取到传递过来的参数')
        print(str(sys.argv))
        APP_INFO['api_token'] = sys.argv[1]
        APP_INFO['applicationId'] = sys.argv[2]
        APP_INFO['versionName'] = sys.argv[3]
        APP_INFO['versionCode'] = sys.argv[4]
    if len(sys.argv) > 4:
        APP_INFO['changelog'] = sys.argv[5]


# 获取 fir 的上传凭证
def get_cert():
    print_split('发起获取上传凭证请求')
    data = {'type': 'android', 'bundle_id': APP_INFO['applicationId'],
            'api_token': APP_INFO['api_token']}
    print(data)
    req = requests.post(url='http://api.fir.im/apps', data=data)
    cert_resp = req.content
    print_split('获取到 fir 响应')
    print(str(cert_resp))
    return cert_resp


# 遍历目录获取到 最后一次修改的apk文件（认为是需要上传的文件）
def get_last_modify_apk():
    print_split('遍历获取 Apk')
    # 遍历拿到最后一次修改的路径
    last_m_time = 100
    last_apk_path = ''
    for (root, dirs, files) in os.walk('../'):
        for item in files:
            if os.path.splitext(item)[1] == '.apk':
                abs_path = os.path.join(root, item)
                print('检测到apk文件：' + abs_path)
                if os.path.getmtime(abs_path) > last_m_time:
                    last_m_time = os.path.getmtime(abs_path)
                    last_apk_path = abs_path
    print_split('获取到最后一次修改的 apk文件路径')
    print(last_apk_path)
    return last_apk_path


# 上传到fir
def upload_fir(binary, path):
    # 拿到相应的token
    cert_key = binary['key']
    cert_token = binary['token']
    cert_upload_url = binary['upload_url']

    print_split('上传 Apk')
    file = {'file': open(path, 'rb')}
    param = {
        "key": cert_key,
        "token": cert_token,
        'x:build': APP_INFO['versionCode'],
        "x:name": '  ',
        "x:changelog": APP_INFO['changelog']
    }
    requests.packages.urllib3.disable_warnings()
    req = requests.post(cert_upload_url,files=file, data=param, verify=False)

    print(req.content)


if __name__ == '__main__':
    init_app_info()
    cert_resp2 = get_cert()

    # 拿到cert实体
    cert_json = json.loads(cert_resp2)
    binary_dirt = cert_json['cert']['binary']

    apk_path = get_last_modify_apk()

    upload_fir(binary_dirt, apk_path)

```


# Gradle 脚本

```

复制下面的代码到 app/build.gradle 

task uploadFir {
//    dependsOn 'assembleRelease'  (这个是可选的，标识是否构建最新Release版本)
    doLast {

        def apiToken = "04d3c6e1dc9b65977be388be38asfdasdfasdf"
        def appId = project.android.defaultConfig.applicationId
        def versionName = project.android.defaultConfig.versionName
        def versionCode = project.android.defaultConfig.versionCode
        def changeLog = "填写更新日志"

        // 执行Python脚本
        def process = "python3 fir.py ${apiToken} ${appId} ${versionName} ${versionCode} ${changeLog}".execute()

        ByteArrayOutputStream result = new ByteArrayOutputStream()
        def inputStream = process.getInputStream()
        byte[] buffer = new byte[1024]
        int length
        while ((length = inputStream.read(buffer)) != -1) {
            result.write(buffer, 0, length)
        }
        println(result.toString("UTF-8"))
    }
}
```

在 终端 执行  gradle uploadFir

运行结果

```

> Task :app:uploadFir 
--------------------[ 获取到传递过来的参数 ]--------------------
['fir.py', '04d3c6e1dc9b65977be388be3801c9c7', 'com.xxxx', '4.3.0', '150', '填写更新日志']
--------------------[ 发起获取上传凭证请求 ]--------------------
{'type': 'android', 'bundle_id': 'com.yoinsapp', 'api_token': '04d3c6e1dc9b65977be388be3801c9c7'}
--------------------[ 获取到 fir 响应 ]--------------------
b'{"id":"5af3a2e2959d693a4c99861a","type":"android","short":"ysandroid","app_user_id":"596c3640ca87a843e100000e","storage":"qiniu","form_method":"POST","cert":{"icon":{"key":"79993a222dfe8e55b8d6058f397dd52904901b9b","token":"这个值很长","upload_url":"https://upload.qbox.me","custom_headers":{},"custom_callback_data":{"original_key":"3957ad13cc2794e206f610f57f7e8507ec551808"}},"binary":{"key":"3cbed5d72486957b245ba81e7d1f9389f4f038df.apk","token":"这个值很长","upload_url":"https://upload.qbox.me","custom_headers":{}},"mqc":{"total":5,"used":0,"is_mqc_availabled":true},"support":"qiniu","prefix":"x:"}}'
--------------------[ 遍历获取 Apk ]--------------------
检测到apk文件：../XXXX/app/build/outputs/apk/release/app-release-unsigned.apk
检测到apk文件：../XXXX/app/build/outputs/apk/debug/app-debug.apk
检测到apk文件：../YYYYl/app/release/125.apk
检测到apk文件：../YYYY/app/build/outputs/apk/release/150.apk
检测到apk文件：../YYYY/app/build/outputs/apk/debug/150.apk
--------------------[ 获取到最后一次修改的 apk文件路径 ]--------------------
../YYYY/app/build/outputs/apk/release/150.apk
--------------------[ 上传 Apk ]--------------------
b'{"download_url":"https://pro-app-qn.fir.im/XXXXX.apk?e=1529662797\\u0026token=SSSSSS-T:js8wDCbtYglY5rf4YBHPofIL-PU=","is_completed":true,"release_id":"5b2cbf3c959d6926ef0420ca"}'


BUILD SUCCESSFUL in 42s
1 actionable task: 1 executed


```