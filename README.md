# RiskByPass User Guide / RiskByPass 使用指南

## 📞 How to contact us

If you have any questions, please contact us via https://riskbypass.com/contact

## 📞 如何联系我们

如果你有任何问题，请通过 https://riskbypass.com/contact 联系我们

## 🚩How can I get a free API key?

Go to https://riskbypass.com/dashboard and register an account, your will get 60000 free credits.

## 🚩如何获取免费API Key？

访问官网 https://riskbypass.com/dashboard 并注册账号，注册成功后将赠送 60000 积分。

## 🔍 How to Detect What Anti-Bot System a Site Uses  

If you're not sure what anti-bot system the target website uses, follow these steps:

1. Open your browser and visit the target website  
2. Copy the script from `checkRisk.js`  
3. Open Developer Tools (F12), paste the code and run it  
4. Check the output — if it shows `"Yes"` for any item, that risk control system is in use

If the `checkRisk.js` script is not working, check those fields in the request header and cookie:

`_abck` `bm_sz` `sbsd` `sec_cpt` => Akamai

`cf_bm` `cf_clearance` => Cloudflare

`reese84` `x-d-token` `incap_ses` => Incapsula reese84

`x-kpsdk-ct` `x-kpsdk-cd` `KP_UIDz` => Kasada

`aws-waf-token` => AWS

`_px2 _px3 _pxhd _pxde` => PerimeterX

`datadome` => Datadome

`x-?????-a` `x-?????-b` `x-?????-z` `x-?????-a0` => shape F5

## 🔍 我的目标网站使用了什么风控？

如果你不知道目标网站使用了什么风控产品，可以按照以下步骤检测：

1. 打开浏览器，访问目标网站  
2. 复制项目中的 `checkRisk.js` 脚本  
3. 打开开发者工具（F12），粘贴并运行代码  
4. 查看输出，若出现 "Yes"，即表示该网站启用了相应的风控产品

如果`checkRisk.js`脚本没有打印任何内容，请检查你想要绕过的请求是否必须包含以下字段(请求头以及cookie中)才能发起请求:

`_abck` `bm_sz` `sbsd` `sec_cpt` => Akamai

`cf_bm` `cf_clearance` => Cloudflare

`reese84` `x-d-token` `incap_ses` => Incapsula reese84

`x-kpsdk-ct` `x-kpsdk-cd` `KP_UIDz` => Kasada

`aws-waf-token` => AWS

`_px2 _px3 _pxhd _pxde` => PerimeterX

`datadome` => Datadome

`x-?????-a` `x-?????-b` `x-?????-z` `x-?????-a0` => shape F5

## 🔑 How to Get an API Key

Go to https://riskbypass.com/dashboard and register an account.  
Once registered, your personal API key will be shown on the dashboard.

  
## 🔑 api key在哪里获得？

访问官网 https://riskbypass.com/dashboard 并注册账号，注册成功后将在后台页面看到专属的 API Key。


## 💰 How to Get Credits

- New accounts receive **60000 free credits**  
- Recharge price: **$1 (USDT) = 60,000 credits**  
- To top up, please contact us via https://riskbypass.com/contact

  
## 💰 如何获取积分？

- 新注册账号将赠送 **60000 积分**  
- 充值价格：**1 美元（USDT） = 60000 积分**  
- 充值请通过 https://riskbypass.com/contact 联系我们


## 🧪 How to Use the API via Code

Check the `test_demo` folder in this repository for usage examples and code samples.

## 🧪 如何使用代码请求？

请参考本项目中的 `test_demo` 文件夹，其中包含 API 的调用示例与用法说明。

---

📌 For business integration or custom support, feel free to reach out.  
📌 如需商业集成或定制服务，请联系我们。
