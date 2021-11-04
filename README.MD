# 统计App性能参数 或执行Monkey测试脚本
#工程主入口runMonkey.py文件

## 1.GenerateReport 用于生成测试报告、读取Excel数据

## 2.HtmlParser 用于拼接生成测试报告的字符串

## 3.log 读取adb logcat中的数据，写入到log文件中
- 读取log,将crash、anr的问题单独写到文件中进行分析。
#4.perverifyChajianEnv 配置文件 定义测试的应用包

#5.pyxlswriter  在excel中生成折线图方法

#6.root  定义根路径

