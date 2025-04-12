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
接口请求地址: https://lambopro.net/send_msg
```

|字段名|参数值|
|-----|-----|
|session_id|${SystemSessionId}|
|phone_number|${SystemCalleeNumber}|
|chat_id|步骤一获取的ChatId|
|msg|推广文案|

###### 三、管理后台
1. 访问 https://lambopro.net/
2. 输入 步骤一获取的ChatId
3. 左侧有菜单
4. Message 查看收到的咨询信息
5. Browser 查看配置的浏览器情况

