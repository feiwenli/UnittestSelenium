### unittest框架搭建
- 适用于B/S模式的Web前端的UI自动化测试
#### 文件介绍
- api：存放接口的请求数据
- config：配置文件，内含日志和邮件的配置
- data：存放接口请求数据，UI脚本涉及到的校验页面的文案数据以及xpath文件
- driver：存放Windows系统中运行所需要的chromedriver等驱动文件
- log：脚本运行日志放在此处
- report：测试报告文件放在此处
- test：测试的case放在此处
- utils：自制工具类放在此处

#### 本框架所实现的功能
- pc端的cookie登录，h5端的免密登录
- 测试数据与代码分离，可同时适配多套环境
- 用HTMLTestRunner生成测试报告，并通过smtp邮件服务器发送邮件
- 日志模块
- 使用Chrome的模拟器模拟H5端页面

- 不断完善中。。。
