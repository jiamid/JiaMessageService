# JiaMessageService

# 操作步骤
###### 一、获取ChatId
1. 打开TG，https://t.me/TcccMsgBot
2. 点击 Start 或者发送命令 /start
3. 点击 ChatId或手动复制ChatId
###### 二、配置API Call
1. 到Tccc后台配置电话接听按键等规则
2. 配置用户按键触发API Call
```
接口请求地址: http://43.160.195.19/send_msg
```

|字段名|参数值|
|-----|-----|
|session_id|${SystemSessionId}|
|phone_number|${SystemCalleeNumber}|
|chat_id|步骤一获取的ChatId|
|msg|推广文案|

###### 三、管理后台
1. 查看消息 http://43.160.195.19/message
2. 管理浏览器 http://43.160.195.19/browser

