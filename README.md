# 安装chromedriver

> https://sites.google.com/a/chromium.org/chromedriver/
> http://chromedriver.storage.googleapis.com/index.html

# 安装phantomjs

> http://phantomjs.org/download.html

# Chrome插件逻辑

![chrome_extension_logic](https://raw.githubusercontent.com/Everley1993/MiShare/master/files/chrome_extension_logic.jpeg)

## chrome启动事件

> http://stackoverflow.com/questions/9598467/google-chrome-extensions-launch-event

## chrome定时器

> https://developer.chrome.com/extensions/alarms

## chrome遍历标签页

> http://stackoverflow.com/questions/5409242/chrome-extension-iterate-through-all-tabs
> https://developer.chrome.com/extensions/tabs

# 协议

## 会话

在cookie中的session_id保存会话ID来标识一个会话

## 返回码

| Code | Description                      |
|------|----------------------------------|
| 0    | 成功                             |
| -100 | 会话过期，需要重新登录           |
| -101 | 账号或密码错误                   |
| -102 | 贡献值不足                       |
| -103 | 账号正在使用中，不能重复兑换     |
| -104 | 同一个网站只能兑换一个账号       |
| -105 | 需要输入验证码                   |
| -106 | 账号无效                         |
| -107 | 并没有在使用该账号               |
| -108 | 该账号不是你共享的，无法修改信息 |
| -109 | 账号到达最大共享人数，无法兑换 |

## 注册(时间不允许的话不实现)

略

## 登录

```
url:      	/login
method:     POST
parameters:
| Key      | Type   | Mandatory | Description |
|----------|--------|-----------|-------------|
| username | string | Y         | 用户名      |
| password | string | N         | 密码(md5)   |
response:
{
	"c": 0,
	"nickname": 			"xxx",			// 昵称
	"portrait": 			"http://xxx",	// 头像链接
	"contribution_value": 	100				// 贡献值
}
possible error code: -101
登陆成功时会设置cookie，保存会话ID
```

## 获取网站列表

```
url:    	/site_list
methord: 	GET
parameters:
| Key      | Type   | Mandatory | Description |
|----------|--------|-----------|-------------|
response:
{
	"c": 0,
	"sites": [
		{
			"site_id": 		100,								// 网站ID
			"site_title": 	"爱奇艺",							// 网站标题
			"site_url": 	"http://http://www.iqiyi.com/",		// 网站URL
			"site_icon": 	"http://xxx"						// 网站图标
		},
		...
	]
}
possible error code: -100
```

## 获取网站账号列表

```
url:    	/account_list/<site_id>
methord: 	GET
parameters:
| Key      | Type   | Mandatory | Description |
|----------|--------|-----------|-------------|
response:
{
	"c": 0,
	"accounts": [
		{
			"account_id": 					100,			// 账号ID
			"account_owner_nickname": 		"小明湖畔",		// 账号拥有者昵称
			"account_owner_portrait": 		"http://xxx",   // 账号拥有者头像链接
			"vip_expire_date": 				"2016-12-12",	// 会员过期时间
			"max_concurrency_user": 		5,				// 最大同时使用人数
			"cur_concurrency_user": 		1,				// 当前使用人数
			"contribution_value_per_hour":	25,				// 每小时需要多少贡献值
			"status": 						1				// 账号状态 0: 未使用 1: 正在使用中
		},
		...
	]
}
possible error code: -100
```

## 获取我共享的账号列表

```
url: 		/my_sharing_account_list
method:		GET
parameters:
| Key      | Type   | Mandatory | Description |
|----------|--------|-----------|-------------|
response:
{
	"c": 0,
	"accounts": [
		{
			"account_id": 					100,			// 账号ID
			"account_username": 			"abc123456",	// 账号用户名
			"vip_expire_date": 				"2016-12-12",	// 会员过期时间
			"max_concurrency_user": 		5,				// 最大同时使用人数
			"cur_concurrency_user": 		1,				// 当前使用人数
			"contribution_value_per_hour": 	25,				// 每小时需要多少贡献值
			"status": 						1				// 账号状态 0: 账号无效 1: 账号有效
		},
		...
	]
}
possible error code: -100
```

## 获取我正在使用的账号列表

```
url: 		/my_renting_account_list
method:		GET
parameters:
| Key      | Type   | Mandatory | Description |
|----------|--------|-----------|-------------|
response:
{
	"c": 0,
	"accounts": [
		{
			"account_id": 100,			            // 账号ID
            "domain": "www.iqiyi.com",              // 上报监控的域名
            "report_interval": 900,                 // 上报监控的时间间隔(单位秒)
            "cookies": [                            // cookie
                {
                    "domain": 	".iqiyi.com",
                    "name":   	"c241315581245",
                    "value":  	"1473183603954",
                    "path":   	"/",
                    "expire": 	1480959604,
                    "httpOnly": false,
                    "secure": 	false
                },
                ...
            ]
		},
		...
	]
}
possible error code: -100
```

## 添加共享账号

```
url: 		/add_account
method:		POST
parameters:
| Key               | Type   | Mandatory | Description                                                                                    |
|-------------------|--------|-----------|------------------------------------------------------------------------------------------------|
| username          | string | Y         | 用户名                                                                                         |
| password          | string | Y         | 密码                                                                                           |
| verification_code | string | N         | 验证码，第一次点击添加共享账号时，若返回信息表明需要验证码，则下需要填上验证码后再发送一次请求 |

response:
{
	"c": 0
}
{
	"c": -105,
	"verification_code_base64": "xxxxx"		// 验证码图片的base64编码字符串
}
possible error code: -100, -105, -106
```

## 修改/激活 共享账号(时间不够不做)

```
url: 		/modify_account
method:	 	POST
parameters:
| Key               | Type   | Mandatory | Description                                                                                      |
|-------------------|--------|-----------|--------------------------------------------------------------------------------------------------|
| account_id        | int    | Y         | 账号ID                                                                                           |
| password          | string | Y         | 账号ID                                                                                           |
| verification_code | string | N         | 验证码，第一次点击兑换时此字段可为空，若返回信息表明需要验证码，则需要填上验证码后再发送一次请求 |
response:
{
	"c": 0,
    "vip_expire_date": 				"2016-12-12",	// 会员过期时间
    "max_concurrency_user": 		5,				// 最大同时使用人数
    "cur_concurrency_user": 		1,				// 当前使用人数
    "contribution_value_per_hour": 	25,				// 每小时需要多少贡献值
}
{
	"c": -105,
	"verification_code_base64": "xxxxx"		// 验证码图片的base64编码字符串
}
possible error code: -100, -105, -106


## 兑换账号

```
url: 		/rent_account
method:	 	POST
parameters:
| Key               | Type   | Mandatory | Description                                                                                      |
|-------------------|--------|-----------|--------------------------------------------------------------------------------------------------|
| account_id        | int    | Y         | 账号ID                                                                                           |
| verification_code | string | Y         | 验证码，第一次点击兑换时此字段可为空，若返回信息表明需要验证码，则需要填上验证码后再发送一次请求 |
response:
{
	"c": 0,
    "account_id": 100,          // 兑换的账号ID
    "domain": "www.iqiyi.com",  // 上报监控的域名
    "report_interval": 900,     // 上报监控的时间间隔(单位秒)
	"cookies": [
		{
			"domain": 	".iqiyi.com",
			"name":   	"c241315581245",
			"value":  	"1473183603954",
			"path":   	"/",
			"expire": 	1480959604,
			"httpOnly": false,
			"secure": 	false
		},
		...
	]
}
{
	"c": -105,
	"verification_code_base64": "xxxxx"		// 验证码图片的base64编码字符串
}
possible error code: -100, -104, -105, -106, -109
```

## 停止使用账号

```
url: 		/stop_renting_account
method:	 	POST
parameters:
| Key        | Type | Mandatory | Description |
|------------|------|-----------|-------------|
| account_id | int  | Y         | 账号ID      |
response:
{
	"c": 0
}
possible error code: -100, -107
```

## 上报账号状态

```
url: 		/report_renting_account
method:	 	POST
parameters:
| Key        | Type                 | Mandatory | Description                                          |
|------------|----------------------|-----------|------------------------------------------------------|
| account_id | int                  | Y         | 账号ID                                               |
| in_use     | bool("true"/"false") | Y         | 是否正在使用，即打开的标签页中是否有该账号监控的域名 |
response:
{
	"c": 0,
    "contribution_value": 100,  // 剩余贡献值
    "event": 0 | 1 | 2,         // 0: 不执行任何操作, 1: cookie续命, 2: 停止使用该账号，删除cookie, 关闭相关便签
    "cookies": [                // event = 1 时，返回的新cookie
        {
            "domain": 	".iqiyi.com",
            "name":   	"c241315581245",
            "value":  	"1473183603954",
            "path":   	"/",
            "expire": 	1480959604,
            "httpOnly": false,
            "secure": 	false
        },
        ...
    ]
}
possible error code: -100
```
