# 安装chromedriver

> https://sites.google.com/a/chromium.org/chromedriver/
> http://chromedriver.storage.googleapis.com/index.html

# 安装phantomjs

> http://phantomjs.org/download.html
# 协议

## 会话

在cookie中的session_id保存会话ID来标识一个会话

## 返回码

| Code | Description                  |
|------|------------------------------|
| 0    | 成功                         |
| -100 | 会话过期，需要重新登录       |
| -101 | 账号或密码错误               |
| -102 | 贡献值不足                   |
| -103 | 账号正在使用中，不能重复兑换 |
| -104 | 需要输入验证码               |

## 注册(时间不允许的话不实现)

略

## 登录

```
url:      	/login
method:     POST
parameters:
| Key      | Type   | Description |
|----------|--------|-------------|
| username | string | 用户名      |
| password | string | 密码        |
response:
{
	"c": 0,
	"nickname": 			"xxx",			// 昵称
	"portrait": 			"http://xxx",	// 头像链接
	"contribution_value": 	100				// 贡献值
}
登陆成功时会设置cookie，保存会话ID
```

## 获取网站列表

```
url:    	/site_list
methord: 	GET
parameters:
| Key        | Type   | Description |
|------------|--------|-------------|
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
```

## 获取网站账号列表

```
url:    	/account_list/<site_id>
methord: 	GET
parameters:
| Key        | Type   | Description |
|------------|--------|-------------|
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
```

## 获取我拥有的账号(时间不允许的话不实现)

```
url: 		/my_account_list
method:		GET
parameters:
| Key        | Type   | Description |
|------------|--------|-------------|
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
```

## 添加我拥有的账号(时间不允许的话不实现)

略

## 兑换账号使用权

```
url: 		/rent_account
method:	 	POST
parameters:
| Key               | Type   | Description                                                                                |
|-------------------|--------|--------------------------------------------------------------------------------------------|
| account_id        | int    | 账号ID                                                                                     |
| hour              | int    | 兑换多少小时                                                                               |
| verification_code | string | 验证码，第一次点击兑换时此字段可为空，若返回信息表明需要验证码，则下一次兑换需要填上验证码 |
response:
{
	"c": 0,
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
	"c": -104,
	"verification_code_base64": "xxxxx"		// 验证码图片的base64编码字符串
}
```
