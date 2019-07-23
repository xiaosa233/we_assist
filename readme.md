# we_assist
------
爱看不看的Readme

Read this in yourway...emmm  :) 

------
你懂吧，我的意思是，它是wechat 的助手

一个基于 itchat 实现的小工具

声明：本工具纯粹出于个人兴趣及需要实现，不参与任何形式的商业行为。在符合微信规范的行为下帮助个人实现功能。

另外，监视好友信息不是一个友好的功能，用的时候心里要有数啊……

Email：li.xiaojian233@qq.com


依赖库：

1、itchat (`pip install itchat`)

2、PIL (`pip install pillow`)

3、python3.7 （must be >= 3.7）

------
## 教程：


1、分别运行 source/main.py 和 source/wakeup/wakeup_main.py 

2、扫码登录即可

3、在个人微信页面给你的文件传输助手发送帮助

4、退出程序，分别给上面两个进程输入0 ， 回车，等待一段时间以后，按 ctrl + c 终结。

（windows 下永远会有命令行显示，但是linux 下，wakeup 会在后台重启主程序，这个时候使用命令 `pgrep python` 检查pid， 使用命令 `kill -s 9 [pid]` 杀死相应进程即可）


## FAQ

1. 二维码乱码怎么办？

添加命令行参数 2 ，看起来应该是这样的

```
python main.py 2
```


2. 如果我想同时登录电脑版微信呢？

不能同时登录电脑版微信和web 版微信。当使用电脑版的微信时，直接登录电脑版微信即可，不会有任何的影响。

当想重启we_assist 服务时，参考教程，先退干净程序，然后按步骤重启即可。






------

#release note

V1.1 
1. 添加微信唤醒程序，可自动修复itchat 长时间连接问题

V1.0 
1. 监控头像的更改

2. 监控个性签名的更改

3. 监控昵称的更改


V1.1
1. 添加监控信息