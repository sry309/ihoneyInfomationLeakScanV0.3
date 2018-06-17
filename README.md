# ihoneyInfomationLeakScan v0.3 多进程批量网站信息泄露扫描工具

注意!
这个版本运行于 Python2.7，不支持 Python3。

只需要安装 hackhttp 第三方库

pip2.7 install hackhttp

ChanggeLog:

* [v0.1] requests库、多线程
* [v0.2] 版本中 requests 库运行时遇到某异常无法捕获并直接退出程序，使用 hackhttp 重写，此为测试版本。
* [v0.3] 版本中使用多线程效率太低，改为多进程、进程池，提高扫描效率



